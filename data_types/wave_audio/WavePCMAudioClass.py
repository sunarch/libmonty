
class WavePCMAudioClass(object):

    # format source: http://soundfile.sapp.org/doc/WaveFormat/
    # The Canonical WAVE PCM Soundfile Format

    def __init__(self, argNumChannels=1, argSampleRate=44100, argBitsPerSample=16):

        print("Initializing WavePCMAudioClass object...", end="")

        self.set_NumChannels(argNumChannels)
        self.set_SampleRate(argSampleRate)
        self.set_BitsPerSample(argBitsPerSample)

        print("done.")

        print("Number of channels:  " + str(self.get_NumChannels()))
        print("Sample Rate:         " + str(self.get_SampleRate()) + " Hz")
        print("Bits per Sample:     " + str(self.get_BitsPerSample()))
        print("Sample Format:       " + str(self.get_SampleFormat()))

    # ================================================================ #

    # The canonical WAVE format starts with the RIFF header:

    # ---------------------------------------------------------------- #
    # ChunkID

    # Offset: 0, Size: 4, Endian: big
    # Contains the letters "RIFF" in ASCII form
    # (0x52494646 big-endian form)
    __ChunkID = b"RIFF"

    # ---------------------------------------------------------------- #
    # ChunkSize

    # Offset: 4, Size: 4, Endian: little
    # 36 + SubChunk2Size, or more precisely:
    # 4 + (8 + SubChunk1Size) + (8 + SubChunk2Size)
    # This is the size of the rest of the chunk following this number.
    # This is the size of the entire file in bytes minus 8 bytes for the
    # two fields not included in this count: ChunkID and ChunkSize.
    __ChunkSize = b'\x00\x00\x00\x00'
    __ChunkSizeInt = 0

    def __encode_ChunkSize(self):
        self.__ChunkSize = int(self.__ChunkSizeInt).to_bytes(4, byteorder='little', signed=False)

    def update_ChunkSize(self):
        self.__ChunkSizeInt = 36 + self.get_Subchunk2Size()
        self.__encode_ChunkSize()

    def get_ChunkSize(self):
        self.update_ChunkSize()
        return self.__ChunkSizeInt

    # ---------------------------------------------------------------- #
    # Format

    # Offset: 8, Size: 4, Endian: big
    # Contains the letters "WAVE"
    # (0x57415645 big-endian form)
    __Format = b"WAVE"

    # ---------------------------------------------------------------- #

    # The "WAVE" format consists of two subchunks: "fmt " and "data":

    # ================================================================ #

    # The "fmt " subchunk describes the sound data's format:

    # ---------------------------------------------------------------- #
    # Subchunk1ID

    # Offset: 12, Size: 4, Endian: big
    # Contains the letters "fmt "
    # (0x666d7420 big-endian form)
    __Subchunk1ID = b"fmt "

    # ---------------------------------------------------------------- #
    # Subchunk1Size

    # Offset: 16, Size: 4, Endian: little
    # 16 for PCM.  This is the size of the
    # rest of the Subchunk which follows this number.
    __Subchunk1Size = int(16).to_bytes(4, byteorder='little', signed=False)
    __Subchunk1SizeInt = 16

    # ---------------------------------------------------------------- #
    # AudioFormat

    # Offset: 20, Size: 2, Endian: little
    # PCM = 1 (i.e. Linear quantization)
    # Values other than 1 indicate some form of compression.
    __AudioFormat = int(1).to_bytes(2, byteorder='little', signed=False)

    # ---------------------------------------------------------------- #
    # NumChannels

    # Offset: 22, Size: 2, Endian: little
    # Mono = 1, Stereo = 2, etc.
    __NumChannels = b'\x00\x00'
    __NumChannelsInt = 0

    def __encode_NumChannels(self):
        self.__NumChannels = int(self.__NumChannelsInt).to_bytes(2, byteorder='little', signed=False)

    def set_NumChannels(self, argInt):
        if argInt < 1:
            raise ValueError("Channel count can't be lower than 1")
        elif argInt > 8:
            raise ValueError("Channel count can't be higher than 8")
        else:
            self.__NumChannelsInt = argInt

        self.__encode_NumChannels()
        self.update_ByteRate()
        self.update_BlockAlign()

    def get_NumChannels(self):
        return self.__NumChannelsInt

    # ---------------------------------------------------------------- #
    # SampleRate

    # Offset: 24, Size: 4, Endian: little
    # 8000, 44100, etc.
    __SampleRate = b'\x00\x00\x00\x00'
    __SampleRateInt = 0

    def __encode_SampleRate(self):
        self.__SampleRate = int(self.__SampleRateInt).to_bytes(4, byteorder='little', signed=False)

    def set_SampleRate(self, argInt):
        if argInt < 8000:
            raise ValueError("Channel count can't be lower than 8 KHz")
        elif argInt > 96000:
            raise ValueError("Channel count can't be higher than 96 KHz")
        else:
            self.__SampleRateInt = argInt

        self.__encode_SampleRate()
        self.update_ByteRate()

    def get_SampleRate(self):
        return self.__SampleRateInt

    # ---------------------------------------------------------------- #
    # ByteRate

    # Offset: 28, Size: 4, Endian: little
    # == SampleRate * NumChannels * BitsPerSample/8
    __ByteRate = b'\x00\x00\x00\x00'
    __ByteRateInt = 0

    def __encode_ByteRate(self):
        self.__ByteRate = int(self.__ByteRateInt).to_bytes(4, byteorder='little', signed=False)

    def update_ByteRate(self):
        self.__ByteRateInt = self.get_SampleRate() * self.get_NumChannels() * self.get_BitsPerSample() / 8
        self.__encode_ByteRate()

    def get_ByteRate(self):
        return self.__ByteRateInt

    # ---------------------------------------------------------------- #
    # BlockAlign

    # Offset: 32, Size: 2, Endian: little
    # == NumChannels * BitsPerSample/8
    # The number of bytes for one sample including all channels.
    # I wonder what happens when this number isn't an integer?
    __BlockAlign = b'\x00\x00'
    __BlockAlignInt = 0

    def __encode_BlockAlign(self):
        self.__BlockAlign = int(self.__BlockAlignInt).to_bytes(2, byteorder='little', signed=False)

    def update_BlockAlign(self):
        self.__BlockAlignInt = self.get_NumChannels() * self.get_BitsPerSample() / 8
        self.__encode_BlockAlign()

    def get_BlockAlign(self):
        return self.__BlockAlignInt

    # ---------------------------------------------------------------- #
    # BitsPerSample

    # Offset: 34, Size: 2, Endian: little
    # 8 bits = 8, 16 bits = 16, etc.
    __BitsPerSample = b'\x00\x00'
    __BitsPerSampleInt = 0

    __SampleFormat = "U16_LE"

    __MinSampleValue = 0
    __MaxSampleValue = 1

    def __encode_BitsPerSample(self):
        self.__BitsPerSample = int(self.__BitsPerSampleInt).to_bytes(2, byteorder='little', signed=False)

    def set_BitsPerSample(self, argInt):
        if argInt == 8:
            self.__BitsPerSampleInt = 8
        elif argInt == 16:
            self.__BitsPerSampleInt = 16
        elif argInt == 24:
            self.__BitsPerSampleInt = 24
        elif argInt == 32:
            self.__BitsPerSampleInt = 32
        else:
            raise ValueError("Bits per Sample: 8, 16, 24 or 32")

        self.__encode_BitsPerSample()
        self.update_ByteRate()
        self.update_BlockAlign()
        self.update_SampleFormat()
        self.update_MaxSampleValue()

    def get_BitsPerSample(self):
        return self.__BitsPerSampleInt

    def isSampleTypeSigned(self):
        return False

    def get_SampleEndianness(self):
        return "little"

    def get_SampleEndianShort(self):
        return "LE"

    def update_SampleFormat(self):
        localBitsPerSampleInt = self.get_BitsPerSample()
        self.__SampleFormat = "U" + str(localBitsPerSampleInt)

        if localBitsPerSampleInt > 8:
            self.__SampleFormat += "_" + self.get_SampleEndianShort()

    def get_SampleFormat(self):
        return self.__SampleFormat

    def get_MinSampleValue(self):
        return self.__MinSampleValue

    def update_MaxSampleValue(self):
        self.__MaxSampleValue = pow(2, self.get_BitsPerSample()) - 1

    def get_MaxSampleValue(self):
        return self.__MaxSampleValue

    # ---------------------------------------------------------------- #

    # Offset: ---, Size: 2, Endian: little
    # if PCM, then doesn't exist
    # ExtraParamSize

    # Offset: ---, Size: X, Endian: little
    # space for extra parameters
    # ExtraParams

    # ================================================================ #

    # The "data" subchunk contains the size of the data and the actual sound:

    # ---------------------------------------------------------------- #
    # Subchunk2ID

    # Offset: 36, Size: 4, Endian: big
    # Contains the letters "data"
    # (0x64617461 big-endian form)
    __Subchunk2ID = b"data"

    # ---------------------------------------------------------------- #
    # Subchunk2Size

    # Offset: 40, Size: 4, Endian: little
    # == NumSamples * NumChannels * BitsPerSample/8
    # This is the number of bytes in the data.
    # You can also think of this as the size
    # of the read of the subchunk following this number.
    __Subchunk2Size = b'\x00\x00\x00\x00'
    __Subchunk2SizeInt = 0

    def __encode_Subchunk2Size(self):
        self.__Subchunk2Size = int(self.__Subchunk2SizeInt).to_bytes(4, byteorder='little', signed=False)

    def update_Subchunk2Size(self):
        self.__Subchunk2SizeInt = len(self.get_Data())
        self.__encode_Subchunk2Size()

    def get_Subchunk2Size(self):
        self.update_Subchunk2Size()
        return self.__Subchunk2SizeInt

    # ---------------------------------------------------------------- #
    # Data

    # Offset: 44, Size: *, Endian: little
    # The actual sound data.
    __Data = bytes()
    __DataBytearray = bytearray()

    def __encode_Data(self):
        self.__Data = bytes(self.__DataBytearray)

    def __extend_Data(self, argBytearray):
        self.__DataBytearray.extend(argBytearray)

    # convert DataBytearray to inmutable bytes in Data and update sizes
    def update_Data(self):
        self.__encode_Data()
        self.update_ChunkSize()

    def get_Data(self):
        return self.__DataBytearray

    def add_sample(self, argIntList):
        # argIntList: one integer per channel in this sample
        print("Adding sample " + str(argIntList))

        if len(argIntList) != self.get_NumChannels():
            raise ValueError("More values in current sample than channels available")

        BytesPerSample = int(self.get_BitsPerSample() / 8)

        for i in range(len(argIntList)):

            if argIntList[i] < self.get_MinSampleValue():
                raise ValueError("A value inside the sample is too low")

            if argIntList[i] > self.get_MaxSampleValue():
                raise ValueError("A value inside the sample is too high")

            samplePartBytes = int(argIntList[i]).to_bytes(BytesPerSample, byteorder='little', signed=False)
            self.__extend_Data(bytearray(samplePartBytes))

    # ================================================================ #
    # OTHER

    def writeToFile(self, argFileName="output.wav"):

        self.update_Data()

        print("WRITING AUDIO DATA TO FILE")

        print("Number of channels:  " + str(self.get_NumChannels()))
        print("Sample Rate:         " + str(self.get_SampleRate()) + " Hz")
        print("Bits per Sample:     " + str(self.get_BitsPerSample()))
        print("Sample Format:       " + str(self.get_SampleFormat()))

        print("Opening file '" + argFileName + "' for writing...", end="")

        f = open(argFileName, 'wb')

        print("done.")

        print("Writing RIFF header...", end="")

        f.write(self.__ChunkID)         # size:  4 Bytes
        f.write(self.__ChunkSize)       # size:  4 Bytes
        f.write(self.__Format)          # size:  4 Bytes

        print("done.")

        print("Writing 'fmt ' subchunk...", end="")

        f.write(self.__Subchunk1ID)     # size:  4 Bytes
        f.write(self.__Subchunk1Size)   # size:  4 Bytes
        f.write(self.__AudioFormat)     # size: 2 Bytes
        f.write(self.__NumChannels)     # size: 2 Bytes
        f.write(self.__SampleRate)      # size:  4 Bytes
        f.write(self.__ByteRate)        # size:  4 Bytes
        f.write(self.__BlockAlign)      # size: 2 Bytes
        f.write(self.__BitsPerSample)   # size: 2 Bytes

        print("done.")

        print("Writing 'data' subchunk...", end="")

        f.write(self.__Subchunk2ID)     # size:  4 Bytes
        f.write(self.__Subchunk2Size)   # size:  4 Bytes
        f.write(self.__Data)            # size: * Bytes

        print("done.")

        print("Closing file...", end="")

        f.close()

        print("done.")
