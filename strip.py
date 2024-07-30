from rpi_ws281x import Color, PixelStrip, ws # type: ignore

# LED strip configuration:
LED_COUNT      = 177     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_BRIGHTNESS = 100
LED_STRIP      = ws.SK6812_STRIP_RGBW

LOWEST_NOTE = 21
HIGHEST_NOTE = 21 + 87

# Create PixelStrip object with appropriate configuration.
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
strip.begin()

PreviewColor = Color(0, 0, 0, 0)
OnColor = Color(0, 255, 0, 0)
OffColor = Color(0, 0, 0, 0)

def GetLedFromNote(note):
    #Led la plus à gauche à allumer pour la première octave (en partant du la le plus grave)
    tab_leds = (0,  3,  4,  7,  9,  10, 13, 14, 17, 19, 20, 23)
    #position des notes noires (en partant du la)
    noire = {1, 4, 6, 9, 11}

    octave = (note - LOWEST_NOTE) // 12
    num_note = (note - LOWEST_NOTE) % 12

    if(num_note in noire):
        number = 2
    elif(note == HIGHEST_NOTE):
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

def HexToColor(hex_color):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return Color(rgb[1], rgb[0], rgb[2])

def ColorToHex(color):
    g = (color >> 16) & 0xFF
    r = (color >> 8) & 0xFF
    b = color & 0xFF
    hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
    return hex_color

def SetColor(color):
    global OnColor
    OnColor = color

def SetBrightness(brightness):
    strip.setBrightness(int(brightness))
    strip.show()

def NoteToBrightness(note):
    return (note - LOWEST_NOTE) * 255 // 88

def NoteToColor(note):
    led = GetLedFromNote(note)[0]
    return Wheel(led)

def SetColorFromRainbow(note):
    led = GetLedFromNote(note)[0]
    SetColor(Wheel(led))

def Wheel(pos):
	# Generate rainbow colors across 0-255 positions.
    LED_DIV3 = LED_COUNT/3
    fact = 255 / LED_DIV3
    if pos < LED_DIV3:
        return Color(int(pos * fact), int(255 - pos * fact), 0)
    elif pos < LED_DIV3 * 2:
        pos -= LED_DIV3
        return Color(int(255 - pos * fact), 0, int(pos * fact))
    else:
        pos -= LED_DIV3 * 2
        return Color(0, int(pos * fact), int(255 - pos * fact))

def PreviewColorON(note):
    led = GetLedFromNote(note)[0]
    global PreviewColor
    PreviewColor = Wheel(led)
    for i in range(LED_COUNT):
        strip.setPixelColor(i, PreviewColor)
    strip.show()

def PreviewColorOFF():
    for note in range(LOWEST_NOTE, HIGHEST_NOTE +1):
        num_leds, number = GetLedFromNote(note)
        color = Wheel(num_leds)
        for leds in range(number):
            strip.setPixelColor(num_leds + leds, color)
    strip.show()

def PreviewColorRGB():
    for note in range(LOWEST_NOTE, HIGHEST_NOTE +1):
        num_leds, number = GetLedFromNote(note)
        color = Wheel(num_leds)
        for leds in range(number):
            strip.setPixelColor(num_leds + leds, color)
        strip.show()

def ApplyPreviewColor():
    global OnColor
    OnColor = PreviewColor

def PreviewBrightness():
    ColorWipeFromCenter(OnColor)

def ColorWipeFromSides(color):
    for i in range(int(LED_COUNT/2) +1):
        strip.setPixelColor(i, color)
        strip.setPixelColor(LED_COUNT - i, color)
        strip.show()

def ColorWipeFromCenter(color):
	for i in range(int(LED_COUNT/2) +1):
		strip.setPixelColor(int(LED_COUNT/2) + i, color)
		strip.setPixelColor(int(LED_COUNT/2) - i, color)
		strip.show()

def RainbowFromLeft():
    for note in range(LOWEST_NOTE, HIGHEST_NOTE):
        num_leds, number = GetLedFromNote(note)
        color = Wheel(num_leds)
        for leds in range(number):
            strip.setPixelColor(num_leds + leds, color)
        strip.show()

def RainbowFromCenter():
	for i in range(int(LED_COUNT/2) +1):
		strip.setPixelColor(int(LED_COUNT/2) + i, Wheel(int(LED_COUNT/2) + i))
		strip.setPixelColor(int(LED_COUNT/2) - i, Wheel(int(LED_COUNT/2) - i))
		strip.show()