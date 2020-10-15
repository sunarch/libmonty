# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


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
