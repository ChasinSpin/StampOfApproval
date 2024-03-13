# IMPORTANT: GT-U7 uses the GPS/GLONASS/QZSS Ublox Protocol:  https://content.u-blox.com/sites/default/files/products/documents/u-blox6-GPS-GLONASS-QZSS-V14_ReceiverDescrProtSpec_%28GPS.G6-SW-12013%29_Public.pdf

import os
import time
import board
import busio
import storage
import digitalio
from state import State

class Gps():

	BAUD_RATE			= 9600
	MAX_NMEA_MSG_SIZE		= 82
	UBX_PAYLOAD_MAX			= 65535
	COLD_START_FNAME		= '/coldstart.txt'

	INPUT_NMEA			= 0
	INPUT_UBX			= 1

	# Set polarity = falling edge at top of second, gridUtcGps = UTC, LED 100ms on, 900ms off, PPS Interval = 1 sec
	CFG_TP5_PAYLOAD_MODE_MONITOR	= b'\x00\x00\x00\x00\x32\x00\x00\x00\x40\x42\x0F\x00\x40\x42\x0F\x00\x00\x00\x00\x00\xA0\x86\x01\x00\x00\x00\x00\x00\x77\x00\x00\x00'

	# Set polarity = rising edge at top of second, gridUtcGps = UTC, LED 900ms on, 100ms off, PPS Interval = 1 sec
	CFG_TP5_PAYLOAD_MODE_FLASHER_1S	= b'\x00\x00\x00\x00\x32\x00\x00\x00\x40\x42\x0F\x00\x40\x42\x0F\x00\x00\x00\x00\x00\xA0\x86\x01\x00\x00\x00\x00\x00\x37\x00\x00\x00'

	# Set polarity = falling edge at top of second, gridUtcGps = UTC, LED 6s on, 4s off, PPS Interval = 10 sec
	CFG_TP5_PAYLOAD_MODE_TIMING_10S	= b'\x00\x00\x00\x00\x32\x00\x00\x00\x80\x96\x98\x00\x80\x96\x98\x00\x00\x00\x00\x00\x80\x8D\x5B\x00\x00\x00\x00\x00\x77\x00\x00\x00'

	# Timing mode states
	TSTATE_WAIT_START		= 0    # No output, waiting for user to start
	TSTATE_WAIT_GAP			= 1    # Waiting for minimum 5 sec gap in 10s pulses
	TSTATE_WAIT_PULSE		= 2    # Pulse is scheduled, waiting for pulse
	TSTATE_WAIT_ACTIVE		= 3    # Wait for pulse to be active
	TSTATE_WAIT_FINISHED		= 4    # Wait for pulse to finish
	TSTATE_PULSE_COMPLETE		= 5    # Pulse has been complete, waiting to return to 

	# Flasher States
	FSTATE_WAIT_NEXT_FLASH_TIME	= 0    # No output, waiting for the next scheduled flash time
	FSTATE_WAIT_ACTIVE		= 1    # Wait for pulse to be active
	FSTATE_WAIT_FINISHED		= 2    # Wait for pulse to finish

	# opMode
	OPMODE_TIMING			= 0
	OPMODE_FLASHER			= 1


	def __init__(self, flasherTimes):
		self.uart = busio.UART(board.TX, board.RX, baudrate = self.BAUD_RATE, receiver_buffer_size=1024)
		self.nmeaBuffer = []
		self.ubxBuffer	= []
		self.previousInputChar = None
		self.firstValidSentance = True
		self.ppsLastReceived = -1.0
		self.ppsPulseActive = False
		self.inputType = self.INPUT_NMEA
		self.setPpsDelta(1.0)
		self.modeTiming = False
		self.modeTimingState = self.TSTATE_WAIT_START
		self.modeLocation = False
		self.flasherTimes = flasherTimes
		self.flasherState = self.FSTATE_WAIT_NEXT_FLASH_TIME
		self.flasher1Sec = False

		self.opMode = self.OPMODE_FLASHER if self.flasherTimes is not None else self.OPMODE_TIMING

		# Setup gate pin to gate the LED output
		self.gatePin = digitalio.DigitalInOut(board.D6)
		self.gatePin.direction = digitalio.Direction.OUTPUT
		self.setGatePinActive(True)

		# GPS Data updates are double buffered
		# GPS Data fields we monitor (intermediate values)
		self.latitude = -1000
		self.longitude = -1000
		self.altitude = -1000
		self.numSatellites = -1
		self.fix = -1
		self.pdop = -1.0
		self.hdop = -1.0
		self.vdop = -1.0
		self.hour = -1
		self.min = -1
		self.sec = -1
		self.subsec = -1
		self.day = -1
		self.mon = -1
		self.year = -1
		self.leapSecondsDefault = True
		self.leapSeconds = -10000
		self.pulseTime = None
		
		# The final GPS data in the double buffer
		self.data = None

		# Initial state
		self.state = State.NO_GPS
	
		# Look for coldstart file, and queue a cold start and delete file if it exists
		try:
			fp = open(self.COLD_START_FNAME, 'r')
			fp.close()
			self.coldStart = True
			
			# Delete file
			storage.remount("/", readonly = False)
			os.remove(self.COLD_START_FNAME)
			storage.remount("/", readonly = True)	# computer is unable to access drive for write whilst circuit python has it open for write, so return to prior

		except OSError:
			self.coldStart = False

		self.__flushUartIncoming()
			

	def __hexCharToDec(self, ch):
		""" Converts a hex single character to a number """
		ch = ord(ch)
		if ch >= ord('0') and ch <= ord('9'):
			return ch - ord('0')
		elif ch >= ord('A') and ch <= ord('F'):
			return ch - ord('A') + 10
		return 0


	def __isValidChecksum(self, nmea):
		""" Returns true if the nmea checksum is valid """
		xor = 0

		# Calculate xor checksum not including $ or *
		checksumDelimIndex = -1
		for i in range(1, len(nmea)):
			if nmea[i] == '*':
				break
			xor ^= ord(nmea[i])

		if i + 2 >= len(nmea):
			return False

		i += 1	# Skip * to first hex character

		checksum = self.__hexCharToDec(nmea[i]) << 4	# Read first hex character
		checksum |= self.__hexCharToDec(nmea[i+1])	# Read second hex character

		if checksum == xor:
			return True
		return False


	
	def __fletcher_cksum(self, buf):
		# Calculates the 8 bit fletcher cksum for UBX packets and returns the values as an array
		ck_a = 0
		ck_b = 0
	
		for i in range(2, len(buf)):
			ck_a += buf[i]
			ck_b += ck_a

		return [ck_a & 0xFF, ck_b & 0xFF]


	def __sendUBXMsg(self, classId, messageId, payload):
		""" Sends a UBX message """

		payloadLen = len(payload)

		if payloadLen > self.UBX_PAYLOAD_MAX:
			print('Error: sendUBXMsg: len too large. Transmission aborted')
			return

		# Setup the header
		buf = bytearray(b'\xB5\x62')
		buf.append(classId)
		buf.append(messageId)
		buf.append(payloadLen & 0xFF)
		buf.append(payloadLen >> 8)

		# Copy the payload in
		for i in range(0, payloadLen):
			buf.append(payload[i])

		# Calculate checksum
		cksum = self.__fletcher_cksum(buf)
		buf.append(cksum[0])
		buf.append(cksum[1])

		self.uart.write(buf)


	def __updateGpsState(self):
		if self.data is None or self.firstValidSentance:
			self.state = State.NO_GPS
			return

		if self.data['numSatellites'] <= 0:
			self.state = State.NO_SIGNAL
			return

		# ACQUIRING_NO_PPS goes here	
		ppsDelta = time.monotonic() - self.ppsLastReceived
		if self.ppsLastReceived != -1 and self.ppsDeltaTooLong >= 0.0 and ppsDelta > self.ppsDeltaTooLong:
			self.state = State.ACQUIRING_NO_PPS
			return

		if self.data['leapSecondsDefault']:
			self.state = State.WAITING_FOR_LEAPS
			return

		if self.data['fix'] == 3 and self.data['pdop'] < 3.0 and self.data['hdop'] < 3.0 and self.data['vdop'] < 3.0 and self.data['numSatellites'] >= 6:
			self.state = State.GOOD_FIX
		else:
			self.state = State.POOR_FIX


	def __gpsMessageSetup(self):
		"""
			Disables GPGSV, GPVTG, GPGLL, GPRMC as we don't need the information as it's duplicate, it's many lines and takes up a lot of CPU resources
			Enables PUBX,04 time message (which includes leap seconds)
		"""

		# Disable messages we don't need
		self.uart.write(bytes('$PUBX,40,GSV,0,0,0,0*59\r\n', 'ascii'))
		self.uart.write(bytes('$PUBX,40,VTG,0,0,0,0*5E\r\n', 'ascii'))
		self.uart.write(bytes('$PUBX,40,GLL,0,0,0,0*5C\r\n', 'ascii'))

		# Enable PUBX,04 time messages at 1 second intervals
		# Reference CFG-MSG Set Message Rate: https://content.u-blox.com/sites/default/files/products/documents/u-blox6-GPS-GLONASS-QZSS-V14_ReceiverDescrProtSpec_%28GPS.G6-SW-12013%29_Public.pdf
		self.process()
		self.__sendUBXMsg(0x06, 0x01, b'\xF1\x04\x01')
		self.process()

		self.__sendUBXMsg(0x0A, 0x04, b'')
		self.process()

		# Disable SBAS for better timing (no longer supported according the documentation, but just in case
		self.__sendUBXMsg(0x06, 0x16, b'\x00\x00\x00\x00\x00\x00\x00\x00')
		self.process()

		# Disable SBAS/GLONASS/QZSS
		self.__sendUBXMsg(0x06, 0x3E, b'\x00\x16\x16\x04\x00\x04\xFF\x00\x01\x00\x00\x00\x01\x01\x03\x00\x00\x00\x00\x00\x05\x00\x03\x00\x00\x00\x00\x00\x06\x08\xFF\x00\x00\x00\x00\x00')
		self.process()

		# Configure the PPS pulse
		if   self.opMode == self.OPMODE_FLASHER:
			self.setPpsDelta(10.0)
			self.__sendUBXMsg(0x06, 0x31, self.CFG_TP5_PAYLOAD_MODE_TIMING_10S)
		else:
			self.setPpsDelta(1.0)
			self.__sendUBXMsg(0x06, 0x31, self.CFG_TP5_PAYLOAD_MODE_MONITOR)
		self.process()



	def __convertDegreesMinutesToDegrees(self, str, direction):
		"""
			Converts dddmm.mmmmm or ddmm.mmmmm to decimal degrees multiplied by 10000000
			Returns the decimal degrees or 0 in case of error
			Note: Position 0,0 is in the atlantic ocean, so no chance of conflict with the location
		"""

		try:	
			periodPos = str.index('.')
			periodPos -= 2
	
			deg = str[0:periodPos]
			#print('Deg:', deg)
			min = float(str[periodPos:])
			#print('Min: %0.5f' % min)
			min /= 60.0
			#print('Min60:', min)

			ret = deg + '.' + ('%0.6f' % min).split('.')[1]

			# Add sign
			if direction == 'W' or direction == 'S':
				ret = '-' + ret
		
			return ret
	
		except:
			return '0.0'


	def __gpsProcessNmeaSentance(self, nmea):
		""" Process valid NMEA sentances. """

		#print(nmea)

		fields = nmea.split(',')

		if nmea.startswith('$GPGGA'):
			"""
				$GPGGA,152253.00,5706.42309,N,11012.80644,W,1,08,1.08,1132.0,M,-17.5,M,,
				GGA is in the deault WGS84 datum
				2 = latitude ddmm.mmmmmm
				3 = N or S
				4 = longitude dddmm.mmmmm
				5 = E or W
				7 = Number of satellite used for fix (00-12)
				9 = Altitude in m (above MSL)
			"""

			self.latitude = self.__convertDegreesMinutesToDegrees(fields[2], fields[3])
			self.longitude = self.__convertDegreesMinutesToDegrees(fields[4], fields[5])
			try:
				self.altitude = float(fields[9])
			except:
				self.altitude = -1000.0
			
			self.numSatellites = int(fields[7])

		elif nmea.startswith('$GPGSA'):
			"""
				$GPGSA,A,3,17,24,19,25,03,06,12,11,,,,,2.01,1.08,1.70
				2 = Navigation Mode (1 = Fix not available, 2 = 2D Fix, 3 = 3D Fix)
				15 = Position dilution of precision(PDOP)
				16 = Horizontal dilution of precision(HDOP)
				17 = Vertical dilution of precision(VDOP)
			"""
			self.fix = int(fields[2])
			self.pdop = float(fields[15])
			self.hdop = float(fields[16])
			self.vdop = float(fields[17])

		elif nmea.startswith('$PUBX,04,'):
			"""
				$PUBX,04,152253.00,270623,228172.99,2268,18,341699,401.278,21
				1 = Message ID (must be 04 for time)
				2 = Time hhmmss.ss
				3 = Date ddmmyy
				6 = Leap seconds (D = firmware default value)
			"""
			tm = fields[2]
			self.hour = int(tm[0:2])
			self.min = int(tm[2:4])
			self.sec = int(tm[4:6])
			self.subsec = int(tm[7:9])

			dt = fields[3]
			self.day = int(dt[0:2])
			self.mon = int(dt[2:4])
			self.year = int(dt[4:6])

			leaps = fields[6]
			if len(leaps) >= 1:
				self.leapSecondsDefault = True if leaps[-1] == 'D' else False
				if self.leapSecondsDefault:
					leaps = leaps[0:-1]
				self.leapSeconds = int(leaps)

			self.data = { 'numSatellites': self.numSatellites, 'fix': self.fix, 'pdop': self.pdop, 'hdop': self.hdop, 'vdop': self.vdop, 'hour': self.hour, 'min': self.min, 'sec': self.sec, 'subsec': self.subsec, 'day': self.day, 'mon': self.mon, 'year': self.year, 'leapSecondsDefault': self.leapSecondsDefault, 'leapSeconds': self.leapSeconds, 'latitude': self.latitude, 'longitude': self.longitude, 'altitude': '%0.1f' % self.altitude }
			self.__updateGpsState()
			if self.opMode == self.OPMODE_FLASHER:
				self.__updateFlasherState()
			elif self.opMode == self.OPMODE_TIMING:
				if self.modeTiming:
					self.__updateTimingState()
 

	def __ordsToString(self, buf):
		""" Converts a null terminated array of ordinals into a string """
		chrs = []
		for i in range(len(buf)):
			if buf[i] == 0x00:
				break
			chrs.append(chr(buf[i]))
			
		return ''.join(chrs)


	def __processUBXInput(self, och):
		""" Process UBX input """
		self.ubxBuffer.append(och)

		# If we have at least 6 bytes, extract payload length
		payloadLen = None
		if len(self.ubxBuffer) >= 6:
			payloadLen = self.ubxBuffer[5] * 256 + self.ubxBuffer[4]

		ubxReady = False
		ubxCorrupt = False

		# Do we have a complete packet?
		if payloadLen is not None and len(self.ubxBuffer) >= 4 + payloadLen + 2 + 2:
			# Validate checksum
			cksum = self.__fletcher_cksum(self.ubxBuffer[0:-2])
			if cksum[0] != self.ubxBuffer[-2] or cksum[1] != self.ubxBuffer[-1]:
				ubxCorrupt = True
			else:
				ubxReady = True

		# Does the buffer contain a NMEA terminator, in which case the ubx packet was malformed
		if len(self.ubxBuffer) >= 3:
			for i in range(1,len(self.ubxBuffer)-1):
				if self.ubxBuffer[i-1] == ord('\r') and self.ubxBuffer[i] == ord('\n') and self.ubxBuffer[i+1] == ord('$'):
					ubxCorrupt = True

		if ubxReady or ubxCorrupt:
			if ubxReady:
				print('UBX Rx:', end='')	
				if self.ubxBuffer[2] == 0x05 and self.ubxBuffer[3] == 0x00:
					print(' NAK: class=0x%02X msg=0x%02X' % (self.ubxBuffer[6], self.ubxBuffer[7]))
				elif self.ubxBuffer[2] == 0x05 and self.ubxBuffer[3] == 0x01:
					print(' ACK: class=0x%02X msg=0x%02X' % (self.ubxBuffer[6], self.ubxBuffer[7]))
				elif self.ubxBuffer[2] == 0x0A and self.ubxBuffer[3] == 0x04:
					swVersion = self.__ordsToString(self.ubxBuffer[6:36])
					hwVersion = self.__ordsToString(self.ubxBuffer[36:46])
					romVersion = self.__ordsToString(self.ubxBuffer[46:76])
					extension = self.__ordsToString(self.ubxBuffer[76:106])
					print(' MON-VER: swVersion=%s hwVersion=%s romVersion=%s extension=%s' % (swVersion, hwVersion, romVersion, extension))
				else:
					print(' class=0x%02X msg=0x%02X payload=' % (self.ubxBuffer[6], self.ubxBuffer[7]), end='')

					for i in range(6, len(self.ubxBuffer)-2):
						c = self.ubxBuffer[i]
						print('0x%02X ' % c, end='')
					print('')

			if ubxCorrupt:
				print('Error: Read UBX Packet is corrupt')

			self.ubxBuffer = []
			self.nmeaBuffer = []	
			self.inputType = self.INPUT_NMEA


	def __processNmeaInput(self, ch):
		""" Processes NMEA input characters """
		self.nmeaBuffer.append(ch)

		if len(self.nmeaBuffer) > self.MAX_NMEA_MSG_SIZE:
			print('Error: NMEA Buffer Overflow:', self.nmeaBuffer)
			self.nmeaBuffer = []

		if len(self.nmeaBuffer) < 2:
			return
		elif self.nmeaBuffer[-2] == '\r' and self.nmeaBuffer[-1] == '\n':
			# End of nmea sentance, remove \r\n
			del self.nmeaBuffer[-2:]
			nmeaSentance = ''.join(self.nmeaBuffer)
			self.nmeaBuffer = []

			# Process the nmea sentance
			if len(nmeaSentance) > 6 and nmeaSentance[0] == '$' and self.__isValidChecksum(nmeaSentance):
				nmeaSentance = nmeaSentance[:-3] 	# Remove checksum
				self.__gpsProcessNmeaSentance(nmeaSentance)
				
				if self.firstValidSentance:
					if self.coldStart:
						# If we have a cold start, lets to that and try again
						self.coldStart = False
						self.coldStartReset()
					else:
						self.firstValidSentance = False
						self.__gpsMessageSetup()
			else:
				print('Error: Corrupt NMEA Sentance (missing $ or invalid checksum):', nmeaSentance)


	def process(self):
		""" Processes all waiting GPS messages """

		while True:
			# Read GPS character
			if self.uart.in_waiting == 0:
				break

			och = self.uart.read(1)[0]
			ch = chr(och)

			#print('0x%02X ' % och, end='')

			"""
				Detect UBX messages
				Because they start with 2 bytes (0xB5 0x62) and we are reading 1 byte at time,
				we monitor for both bytes and if found, switch to UBX input state, otherwise place the bytes
				back for NMEA processing.
			"""
			if och == 0xB5:
				self.previousInputChar = och 
				continue
			elif self.previousInputChar is not None and self.previousInputChar == 0xB5 and och == 0x62:
				self.__processUBXInput(self.previousInputChar)
				self.previousInputChar = None
				self.inputType = self.INPUT_UBX
			elif self.inputType == self.INPUT_UBX:
				pass
			else:
				if self.previousInputChar is not None:
					self.__processNmeaInput(chr(self.previousInputChar))
					self.previousInputChar = None
				self.inputType = self.INPUT_NMEA

			if self.inputType == self.INPUT_NMEA:
				self.__processNmeaInput(ch)
			elif self.inputType == self.INPUT_UBX:
				self.__processUBXInput(och)


	def coldStartReset(self):
		self.__sendUBXMsg(0x06, 0x04, b'\xFF\xFF\x00\x00')


	def ppsActive(self):
		#print('ppsActive')
		self.ppsLastReceived = time.monotonic()
		self.ppsPulseActive = True


	def ppsInactive(self):
		#print('ppsInActive')
		self.ppsPulseActive = False


	def __flushUartIncoming(self):
		count = self.uart.in_waiting
		self.uart.read(count)
		count = self.uart.in_waiting
		self.uart.read(count)


	def setPpsDelta(self, ppsInterval):
		self.ppsDeltaTooLong = ppsInterval - 0.1


	def setGatePinActive(self, active):
		if active:
			self.gatePin.value = False
		else:
			self.gatePin.value = True


	def buttonD1Pressed(self, force_leave_timing_mode):
		if   self.opMode == self.OPMODE_FLASHER:
			if self.flasher1Sec: 
				self.flasher1Sec = False
				self.__sendUBXMsg(0x06, 0x31, self.CFG_TP5_PAYLOAD_MODE_TIMING_10S)
				self.setPpsDelta(10.0)
				self.setGatePinActive(False)
			else:
				self.flasher1Sec = True
				self.__sendUBXMsg(0x06, 0x31, self.CFG_TP5_PAYLOAD_MODE_FLASHER_1S)
				self.setPpsDelta(1.0)
				self.setGatePinActive(True)
		elif self.opMode == self.OPMODE_TIMING:
			if self.modeTiming:
				if self.modeTimingState == self.TSTATE_WAIT_START and not force_leave_timing_mode:
					self.modeTimingState = self.TSTATE_WAIT_GAP
				else:
					self.modeTiming = False
					self.setGatePinActive(True)
					#print('Timing Monitor')
					self.__sendUBXMsg(0x06, 0x31, self.CFG_TP5_PAYLOAD_MODE_MONITOR)
					self.setPpsDelta(1.0)
					self.modeTimingState = self.TSTATE_WAIT_START
			else:
				self.modeTiming = True
				self.buttonD2Pressed(True)
				#print('Timing off')
				self.__sendUBXMsg(0x06, 0x31, self.CFG_TP5_PAYLOAD_MODE_TIMING_10S)
				self.setPpsDelta(10.0)
				self.modeTimingState = self.TSTATE_WAIT_START


	def buttonD2Pressed(self, force_leave_location_mode):
		# Applies to flasher and timing modes
		if self.modeLocation or force_leave_location_mode:
			self.modeLocation = False
		else:
			self.modeLocation = True


	def __updateTimingState(self):
		if self.state != State.GOOD_FIX:
			self.buttonD1Pressed(True)
			self.buttonD2Pressed(True)
			return

		if   self.modeTimingState == self.TSTATE_WAIT_START:
			# In this state, flasher output is disabled
			self.setGatePinActive(False)

		elif self.modeTimingState == self.TSTATE_WAIT_GAP:
			# In this state, flasher output is disabled
			deltaTen = self.sec % 10
			self.setGatePinActive(False)
			if deltaTen >=2 and deltaTen < 6:
				self.modeTimingState = self.TSTATE_WAIT_PULSE

		elif self.modeTimingState == self.TSTATE_WAIT_PULSE:
			# In this state, wait till 2 seconds before flash and enable flasher output
			deltaTen = self.sec % 10
			if deltaTen >=8:
				self.modeTimingState = self.TSTATE_WAIT_ACTIVE
				self.setGatePinActive(True)

		elif self.modeTimingState == self.TSTATE_WAIT_ACTIVE:
			# In this state, wait for flash to occur
			if self.ppsPulseActive:
				self.modeTimingState = self.TSTATE_WAIT_FINISHED
				self.pulseTime = { 'hour': self.hour, 'min': self.min, 'sec': self.sec, 'day': self.day, 'mon': self.mon, 'year': self.year }

		elif self.modeTimingState == self.TSTATE_WAIT_FINISHED:
			# In this state, wait for end of flash to occur and disable flasher output
			if not self.ppsPulseActive:
				self.modeTimingState = self.TSTATE_PULSE_COMPLETE
				self.setGatePinActive(False)

		elif self.modeTimingState == self.TSTATE_PULSE_COMPLETE:
			pass


	def __matchGpsToFlasherTimer(self):
		""" Returns True if the GPS time matches one of the flasher times """
		for tm in self.flasherTimes:
			if self.data['hour'] == tm['advanceHour'] and self.data['min'] == tm['advanceMin'] and self.data['sec'] == tm['advanceSec']:
				return True
		return False


	def __updateFlasherState(self):
		if self.state != State.GOOD_FIX:
			self.buttonD2Pressed(True)

		if self.flasher1Sec: 
			self.setGatePinActive(True)
			self.flasherState = self.FSTATE_WAIT_NEXT_FLASH_TIME
			return

		if self.flasherState == self.FSTATE_WAIT_NEXT_FLASH_TIME:
			# In this state, flasher output is disabled
			deltaTen = self.sec % 10
			self.setGatePinActive(False)
			if self.__matchGpsToFlasherTimer():
				self.flasherState = self.FSTATE_WAIT_ACTIVE
				self.setGatePinActive(True)

		elif self.flasherState == self.FSTATE_WAIT_ACTIVE:
			# In this state, wait for flash to occur
			if self.ppsPulseActive:
				self.flasherState = self.FSTATE_WAIT_FINISHED
				self.pulseTime = { 'hour': self.hour, 'min': self.min, 'sec': self.sec, 'day': self.day, 'mon': self.mon, 'year': self.year }

		elif self.flasherState == self.FSTATE_WAIT_FINISHED:
			# In this state, wait for end of flash to occur and disable flasher output
			if not self.ppsPulseActive:
				self.flasherState = self.FSTATE_WAIT_NEXT_FLASH_TIME
				self.setGatePinActive(False)
