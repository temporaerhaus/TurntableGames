import pygame
import pygame.midi as midi

midi.init()

deviceID = midi.get_default_input_id()

print(midi.get_device_info(deviceID))

device = midi.Input(deviceID, 128)

pygame.init()
while True:
    if device.poll():
        for midiEvent in device.read(128):
            print(midiEvent)


print()
