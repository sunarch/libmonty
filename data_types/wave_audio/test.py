#!/usr/bin/env python3

from WavePCMAudioClass import WavePCMAudioClass

a = WavePCMAudioClass()

#print("Sample Format:" + a.get_SampleFormat())

print("")
input("Press enter to create sawtooth samples")
print("")

for i1 in range(0, 10):
    for i in range(0, 65536):
        a.add_sample([i])

print("")
input("Press enter to write to file")
print("")

a.writeToFile()
