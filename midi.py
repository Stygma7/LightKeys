import os
import mido
import strip
import json
from enum import Enum

LEFT_PEDAL = 67
MIDDLE_PEDAL = 66
RIGHT_PEDAL = 64

class PianoMode(Enum):
	PLAY = 0
	CHANGE_RGB = 1
	CHANGE_W = 2
	CHANGE_BRIGHTNESS = 3

pianoMode = PianoMode.PLAY
midi_port = None

dir_path = os.path.dirname(os.path.realpath(__file__))
settings_file = dir_path + "/public/settings.json"

def TryConnectToMidi():
    try:
        global midi_port   
        midi_port = mido.open_input('USB MIDI Interface:USB MIDI Interface MIDI 1 20:0')
    except Exception as e:
        print(e)
        exit(1)

def ListenToMidi():
    TryConnectToMidi()
    GetPreviousSettings()

    print("Listening to midi...")

    try:
        while True:
            for msg in midi_port.iter_pending():
                # print(msg)
                if(pianoMode == PianoMode.PLAY):
                    HandlePlayMode(msg)
                elif(pianoMode == PianoMode.CHANGE_RGB):
                    HandleChangeRGBMode(msg)
                elif(pianoMode == PianoMode.CHANGE_BRIGHTNESS):
                    HandleChangeBrightnessMode(msg)
    except KeyboardInterrupt:
        midi_port.close()
        exit(0)
    except Exception as e:
        print(e)
        midi_port.close()
        exit(1)

def GetPreviousSettings():
    file = open(settings_file, "r")
    settings = json.load(file)
    # print("Get previous settings")
    # print(settings)
    file.close()
    
    strip.SetColor(strip.HexToColor(settings["colorRGB"]))
    strip.SetBrightness(settings["brightness"])
    # date_modif = os.stat(json_file_name)[8]

def ChangeMode(mode):
    if(mode == PianoMode.PLAY):
        strip.ColorWipeFromCenter(strip.Color(0, 0, 0))
    elif(mode == PianoMode.CHANGE_RGB):
        strip.PreviewColorRGB()
    elif(mode == PianoMode.CHANGE_W):
        strip.RainbowFromLeft()
    elif(mode == PianoMode.CHANGE_BRIGHTNESS):
        strip.PreviewBrightness()

    global pianoMode
    # print("mode", pianoMode.name, "->", mode.name)
    pianoMode = mode

def HandlePlayMode(msg):                
    # Notes
    if (msg.type == 'note_on'):
        strip.NoteOn(msg.note)
    if (msg.type == 'note_off'):
        strip.NoteOff(msg.note)

    # Control change
    if(msg.type == 'control_change'):
        if(msg.control == LEFT_PEDAL and msg.value == 127):
            ChangeMode(PianoMode.CHANGE_RGB)

def HandleChangeRGBMode(msg):
    # Notes
    note_preview = 0
    if (msg.type == 'note_on'):
        strip.PreviewColorON(msg.note)
    if (msg.type == 'note_off'):
        strip.PreviewColorOFF()

    # Control change
    if(msg.type == 'control_change'):
        if(msg.control == RIGHT_PEDAL and msg.value == 127):
            strip.ApplyPreviewColor()
            SaveParamToSettings("colorRGB", strip.ColorToHex(strip.PreviewColor))
            ChangeMode(PianoMode.PLAY)
        if(msg.control == LEFT_PEDAL and msg.value == 127):
            ChangeMode(PianoMode.CHANGE_BRIGHTNESS)
            
def HandleChangeBrightnessMode(msg):
    # Notes
    if (msg.type == 'note_on'):
        brightness = strip.NoteToBrightness(msg.note)
        strip.SetBrightness(brightness)
        SaveParamToSettings("brightness", brightness)

    # Control change
    if(msg.type == 'control_change'):
        if(msg.control == RIGHT_PEDAL and msg.value == 127):
            ChangeMode(PianoMode.PLAY)
        if(msg.control == LEFT_PEDAL and msg.value == 127):
            ChangeMode(PianoMode.PLAY)

def SaveParamToSettings(key, value):
    with open(settings_file, "r+") as file:
        settings = json.load(file)
        settings[key] = value
        file.seek(0)
        file.write(json.dumps(settings))
        file.truncate()