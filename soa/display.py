import time
import board
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label
from displayio import Group
from state import State



class Display():

	LINES_Y = [20, 50, 80, 110]
	
	def __init__(self, version, flasherTimes):
		self.systemDisplay = board.DISPLAY
		self.font = bitmap_font.load_font("fonts/Helvetica-Bold-16.bdf")

		group = Group()

		ppsGroup = Group()
		ppsGroup.append(self.__makeTextArea('PPS', 0xFFFFFF, 205, self.LINES_Y[3]))
		ppsGroup.hidden = True

		mainDisplayGroup = Group()
		mainDisplayGroup.append(self.__makeTextArea('Stamp Of Approval', 0xFF00FF, 0, self.LINES_Y[0]))
		mainDisplayGroup.append(self.__makeTextArea('Version: %s' % version, 0xFF00FF, 0, self.LINES_Y[2]))
		mainDisplayGroup.append(self.__makeTextArea('Author: @ChasinSpin', 0xFF00FF, 0, self.LINES_Y[3]))

		group.append(ppsGroup)
		group.append(mainDisplayGroup)

		self.systemDisplay.root_group = group

		time.sleep(2)

		if flasherTimes is not None:
			mainDisplayGroup = Group()

			if len(flasherTimes) == 0:
				mainDisplayGroup.append(self.__makeTextArea('flasher.txt is corrupt', 0xFF0000, 0, self.LINES_Y[0]))
				mainDisplayGroup.append(self.__makeTextArea('fix and restart !', 0xFF0000, 0, self.LINES_Y[1]))
				group[1] = mainDisplayGroup
				self.systemDisplay.root_group = group
				while True:
					pass
			else:
				for i in range(0,4):
					mainDisplayGroup.append(self.__makeTextArea('Flasher Time: %02d:%02d:%02d%s' % (flasherTimes[i]['hour'], flasherTimes[i]['min'], flasherTimes[i]['sec'], '...' if i == 3 else ''), 0xFFFF00, 0, self.LINES_Y[i]))

			group[1] = mainDisplayGroup
			self.systemDisplay.root_group = group

			time.sleep(3)
		else:
			mainDisplayGroup = Group()
			mainDisplayGroup.append(self.__makeTextArea('Buttons:', 0xFF00FF, 0, self.LINES_Y[0]))
			mainDisplayGroup.append(self.__makeTextArea('  <D1> Timing Mode', 0xFF00FF, 0, self.LINES_Y[2]))
			mainDisplayGroup.append(self.__makeTextArea('  <D2> Location Mode', 0xFF00FF, 0, self.LINES_Y[3]))
			group[1] = mainDisplayGroup
			self.systemDisplay.root_group = group
			time.sleep(1)


	def __makeTextArea(self, text, color, x, y):
		text_area = label.Label(self.font, text=text, color=color)
		text_area.x = x
		text_area.y = y
		return text_area


	def updateDisplayForState(self, gps):
		mainDisplayGroup = Group()
		
		if   gps.state == State.NO_GPS:
			mainDisplayGroup.append(self.__makeTextArea('Status: No GPS', 0xFF00FF, 0, self.LINES_Y[0]))
		elif gps.state == State.NO_SIGNAL:
			mainDisplayGroup.append(self.__makeTextArea('Status: No Signal', 0xFF0000, 0, self.LINES_Y[0]))
		elif gps.state == State.ACQUIRING_NO_PPS:
			mainDisplayGroup.append(self.__makeTextArea('Status: Acquirring (no PPS)', 0xFF0000, 0, self.LINES_Y[0]))
			color = 0x666666
			mainDisplayGroup.append(self.__makeTextArea('# Satellites: %d' % (gps.data['numSatellites']), color, 0, self.LINES_Y[1]))
		elif gps.state == State.WAITING_FOR_LEAPS:
			mainDisplayGroup.append(self.__makeTextArea('Status: Waiting For Leap Sec', 0xFF0000, 0, self.LINES_Y[0]))
			color = 0x666666
			mainDisplayGroup.append(self.__makeTextArea('# Satellites: %d' % (gps.data['numSatellites']), color, 0, self.LINES_Y[1]))
		elif gps.state == State.POOR_FIX:
			mainDisplayGroup.append(self.__makeTextArea('Status: Poor Fix', 0xFF0000, 0, self.LINES_Y[0]))
			color = 0x666666
			mainDisplayGroup.append(self.__makeTextArea('# Satellites: %d Leaps: %d' % (gps.data['numSatellites'], gps.data['leapSeconds']), color, 0, self.LINES_Y[1]))
			mainDisplayGroup.append(self.__makeTextArea('DOP(P,H,V) %0.1f,%0.1f,%0.1f' % (gps.data['pdop'], gps.data['hdop'], gps.data['vdop']), color, 0, self.LINES_Y[2]))
			mainDisplayGroup.append(self.__makeTextArea('UTC: 20%02d-%02d-%02d %02d:%02d:%02d' % (gps.data['year'], gps.data['mon'], gps.data['day'], gps.data['hour'], gps.data['min'], gps.data['sec']), color, 0, self.LINES_Y[3]))
		elif gps.state == State.GOOD_FIX:
			mainDisplayGroup.append(self.__makeTextArea('Status: Good Fix', 0x00FF00, 0, self.LINES_Y[0]))
			color = 0xFFFFFF
			
			if gps.modeTiming:
				if   gps.modeTimingState == gps.TSTATE_WAIT_START:
					mainDisplayGroup.append(self.__makeTextArea('LED Off, press <D1>', color, 0, self.LINES_Y[1]))
					mainDisplayGroup.append(self.__makeTextArea('to start timing', color, 0, self.LINES_Y[2]))
				elif gps.modeTimingState == gps.TSTATE_WAIT_GAP:
					mainDisplayGroup.append(self.__makeTextArea('Waiting until timing,', color, 0, self.LINES_Y[1]))
					mainDisplayGroup.append(self.__makeTextArea('gap available...', color, 0, self.LINES_Y[2]))
				elif gps.modeTimingState == gps.TSTATE_WAIT_PULSE:
					mainDisplayGroup.append(self.__makeTextArea('Pulse scheduled, please', color, 0, self.LINES_Y[1]))
					mainDisplayGroup.append(self.__makeTextArea('wait...', color, 0, self.LINES_Y[2]))
				elif gps.modeTimingState == gps.TSTATE_WAIT_ACTIVE:
					mainDisplayGroup.append(self.__makeTextArea('Pulse scheduled, please', color, 0, self.LINES_Y[1]))
					mainDisplayGroup.append(self.__makeTextArea('wait...', color, 0, self.LINES_Y[2]))
				elif gps.modeTimingState == gps.TSTATE_WAIT_FINISHED:
					mainDisplayGroup.append(self.__makeTextArea('Pulse active, please', color, 0, self.LINES_Y[1]))
					mainDisplayGroup.append(self.__makeTextArea('wait...', color, 0, self.LINES_Y[2]))
				elif gps.modeTimingState == gps.TSTATE_PULSE_COMPLETE:
					mainDisplayGroup.append(self.__makeTextArea('Pulse done, it\'s time was', color, 0, self.LINES_Y[1]))
					mainDisplayGroup.append(self.__makeTextArea('UTC: 20%02d-%02d-%02d %02d:%02d:%02d' % (gps.pulseTime['year'], gps.pulseTime['mon'], gps.pulseTime['day'], gps.pulseTime['hour'], gps.pulseTime['min'], gps.pulseTime['sec']), 0x00FFFF, 0, self.LINES_Y[2]))
			elif gps.modeLocation:
				mainDisplayGroup.append(self.__makeTextArea('Lat ' + gps.data['latitude'] + '  Alt ' + gps.data['altitude'] + 'm', color, 0, self.LINES_Y[1]))
				mainDisplayGroup.append(self.__makeTextArea('Lon ' + gps.data['longitude'], color, 0, self.LINES_Y[2]))
			else:
				mainDisplayGroup.append(self.__makeTextArea('# Satellites: %d Leaps: %d' % (gps.data['numSatellites'], gps.data['leapSeconds']), color, 0, self.LINES_Y[1]))
				mainDisplayGroup.append(self.__makeTextArea('DOP(P,H,V) %0.1f,%0.1f,%0.1f' % (gps.data['pdop'], gps.data['hdop'], gps.data['vdop']), color, 0, self.LINES_Y[2]))

			if gps.modeTiming and gps.modeTimingState == gps.TSTATE_PULSE_COMPLETE:
				mainDisplayGroup.append(self.__makeTextArea('Press <D1> to continue', color, 0, self.LINES_Y[3]))
			else:
				mainDisplayGroup.append(self.__makeTextArea('UTC: 20%02d-%02d-%02d %02d:%02d:%02d' % (gps.data['year'], gps.data['mon'], gps.data['day'], gps.data['hour'], gps.data['min'], gps.data['sec']), color, 0, self.LINES_Y[3]))

		self.systemDisplay.root_group[1] = mainDisplayGroup


	def ppsDisplay(self, disp):
		if disp:
			self.systemDisplay.root_group[0].hidden = False
		else:
			self.systemDisplay.root_group[0].hidden = True
