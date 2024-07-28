from rpi_ws281x import Color, PixelStrip, ws

# LED strip configuration:
LED_COUNT      = 177     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_BRIGHTNESS = 100
LED_STRIP      = ws.SK6812_STRIP_RGBW

# Create PixelStrip object with appropriate configuration.
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
strip.begin()

OnColor = Color(0, 255, 0, 0)
OffColor = Color(0, 0, 0, 0)

def GetLedFromNote(note):
    #Led la plus à gauche à allumer pour la première octave (en partant du la le plus grave)
    tab_leds = (0,  3,  4,  7,  9,  10, 13, 14, 17, 19, 20, 23)
    #position des notes noires (en partant du la)
    noire = {1, 4, 6, 9, 11}

    octave = (note-21) // 12
    num_note = (note-21)%12

    if(num_note in noire):
        number = 2
    # last note
    elif(note == 108):
        number = 4
    else:
        number = 3

    # ajout d'un offset pour ajuster l'allumage des leds par rapport aux notes
    if(note > 93 or note == 84):
        offset = -2
    elif(note > 57):
        offset = -1
    else:
        offset = 0

    num_led = tab_leds[num_note] + octave * 24 + offset

    return num_led, number

def NoteOn(note):
    led, number = GetLedFromNote(note)
    for i in range(led, led+number):
        strip.setPixelColor(i, OnColor)
    strip.show()

def NoteOff(note):
    led, number = GetLedFromNote(note)
    for i in range(led, led+number):
        strip.setPixelColor(i, OffColor)
    strip.show()

def SetColor(color):
    OnColor = color

def Wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	fact = 255 / 59
	if pos < 59:
		return Color(int(pos * fact), int(255 - pos * fact), 0)
	elif pos < 118:
		pos -= 59
		return Color(int(255 - pos * fact), 0, int(pos * fact))
	else:
		pos -= 118
		return Color(0, int(pos * fact), int(255 - pos * fact))

def ColorWipeFromSides(color):
    for i in range(int(strip.numPixels()/2) +1):
        strip.setPixelColor(i, color)
        strip.setPixelColor(strip.numPixels() - i, color)
        strip.show()
        	
def RainbowFromCenter():
	for i in range(int(strip.numPixels()/2) +1):
		strip.setPixelColor(int(strip.numPixels()/2) + i, Wheel(int(strip.numPixels()/2) + i))
		strip.setPixelColor(int(strip.numPixels()/2) - i, Wheel(int(strip.numPixels()/2) - i))
		strip.show()