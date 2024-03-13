import board
import digitalio
from gps import Gps
from state import State
from display import Display
from adafruit_debouncer import Debouncer


version = '1.0.0'

FLASHER_FNAME = '/flasher.txt'



def loadFlasherFile():
	# Load the FLASHER_FNAME if it exists
	try:
		ret = []

		with open(FLASHER_FNAME, "r") as fp:
			for line in fp:
				tm = line.strip()
				tm = tm.split(':')
				if len(tm) != 3:
					return []
				for field in tm:
					if len(field) != 2 or not field.isdigit():
						return []

				hour = int(tm[0])
				min = int(tm[1])
				sec = int(tm[2])

				if hour < 0 or hour >= 24 or min < 0 or min >= 60 or sec < 0 or sec >= 60:
					return []

				if sec not in [0, 10, 20, 30, 40, 50]:
					return []

				advanceHour = hour
				advanceMin = min
				advanceSec = sec

				# Move advance 1 second into the past so it's easier to process, as the gps is always 1 second after pps
				advanceSec -= 1
				if advanceSec < 0:
					advanceSec += 60
					advanceMin -= 1
					if advanceMin < 0:
						advanceMin += 60
						advanceHour -= 1
						if advanceHour < 0:
							advanceHour += 24

				flash = { 'hour': hour, 'min': min, 'sec': sec, 'advanceHour': advanceHour, 'advanceMin': advanceMin, 'advanceSec': advanceSec }
				ret.append(flash)

		return ret

	except OSError:
		return None


# MAIN

# Setup pps, gps, display
pps			= digitalio.DigitalInOut(board.D5)

modePin			= digitalio.DigitalInOut(board.D1)
modePin.direction	= digitalio.Direction.INPUT
modePin.pull		= digitalio.Pull.DOWN
mode			= Debouncer(modePin)

locationPin		= digitalio.DigitalInOut(board.D2)
locationPin.direction	= digitalio.Direction.INPUT
locationPin.pull	= digitalio.Pull.DOWN
location		= Debouncer(locationPin)

flasherTimes = loadFlasherFile()
print('Flasher Times:', flasherTimes)

lastPpsState		= pps.value
display			= Display(version, flasherTimes)
gps			= Gps(flasherTimes)
lastModeTiming		= gps.modeTiming



while True:
	mode.update()		# Update the mode pin debouncer
	location.update()	# Update the location pin debouncer

	# Check PPS state and update TFT display, and GPS for lost PPS's
	ppsState = pps.value
	if ppsState != lastPpsState:
		if ppsState == True:
			gps.ppsActive()
		else:
			gps.ppsInactive()
		if gps.state != State.NO_GPS and gps.state != State.NO_SIGNAL and gps.state != State.ACQUIRING_NO_PPS:
			display.ppsDisplay(ppsState)
		lastPpsState = ppsState

	lastModeTiming = gps.modeTiming

	# Check D1 button and change mode
	if mode.rose:
		gps.buttonD1Pressed(False)

	# Check D2 button and toggle to location display
	if location.rose:
		gps.buttonD2Pressed(False)

	# Process gps data
	gpsData = gps.process()
	if gps.data is not None:
		# Update the display
		display.updateDisplayForState(gps)

		print(gps.data)
		gps.data = None
