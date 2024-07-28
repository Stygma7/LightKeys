import os
import mido
import strip
from enum import Enum

class PianoMode(Enum):
	PLAY = 0
	CHANGE_RGB = 1
	CHANGE_W = 2
	CHANGE_BRIGHTNESS = 3

def GetPreviousSettings():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    json_file_name = dir_path + "/public/settings.json"
    date_modif = os.stat(json_file_name)[8]

def ConnectToMidi():
    try:
        return mido.open_input('USB MIDI Interface:USB MIDI Interface MIDI 1 20:0')
    except Exception as e:
        print(e)
        exit(1)

def ChangeMode(mode):
    if(mode == PianoMode.PLAY):
        strip.ColorWipeFromSides(strip.Color(0, 0, 0))
    elif(mode == PianoMode.CHANGE_RGB):
        strip.RainbowFromCenter()

    print("mode :", mode.name)
    
    global pianoMode
    pianoMode = mode

def HandleMidiMessages(midi_port):
    while True:
        for msg in midi_port.iter_pending():
            # print(msg)
            if(pianoMode == PianoMode.PLAY):
                HandlePlayMode(msg)
            elif(pianoMode == PianoMode.CHANGE_RGB):
                
                print(msg)
                # Notes
                if (msg.type == 'note_on'):
                    strip.SetColor(strip.Wheel(msg.note))

                # Control change
                if(msg.type == 'control_change'):
                    if(msg.control == 67 and msg.value == 127):
                        ChangeMode(PianoMode.PLAY)

def HandlePlayMode(msg):                
    # Notes
    if (msg.type == 'note_on'):
        strip.NoteOn(msg.note)
    if (msg.type == 'note_off'):
        strip.NoteOff(msg.note)

    # Control change
    if(msg.type == 'control_change'):
        if(msg.control == 67 and msg.value == 127):
            ChangeMode(PianoMode.CHANGE_RGB)

def Run():
    # GetPreviousSettings()
    midi_port = ConnectToMidi()
    print("LightKeys Started")

    HandleMidiMessages(midi_port)

pianoMode = PianoMode.PLAY
Run()