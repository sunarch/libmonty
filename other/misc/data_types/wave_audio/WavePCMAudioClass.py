#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


class WavePCMAudioClass:

    # format source: http://soundfile.sapp.org/doc/WaveFormat/
    # The Canonical WAVE PCM Soundfile Format

    def __init__(self, arg_num_channels=1, arg_sample_rate=44100, arg_bits_per_sample=16):

        print('Initializing WavePCMAudioClass object...')

        self.set_num_channels(arg_num_channels)
        self.set_sample_rate(arg_sample_rate)
        self.set_bits_per_sample(arg_bits_per_sample)

        print('... done.')

        print('Number of channels:  ', str(self.get_num_channels()))
        print('Sample Rate:         ', str(self.get_sample_rate()) + ' Hz')
        print('Bits per Sample:     ', str(self.get_bits_per_sample()))
        print('Sample Format:       ', str(self.get_sample_format()))

    ############################################################################
    # The canonical WAVE format starts with the RIFF header: ###################

    # ChunkID ##################################################################

    # Offset: 0, Size: 4, Endian: big
    # Contains the letters 'RIFF' in ASCII form
    # (0x52494646 big-endian form)
    _chunk_id = b'RIFF'

    # ChunkSize ################################################################

    # Offset: 4, Size: 4, Endian: little
    # 36 + SubChunk2Size, or more precisely:
    # 4 + (8 + SubChunk1Size) + (8 + SubChunk2Size)
    # This is the size of the rest of the chunk following this number.
    # This is the size of the entire file in bytes minus 8 bytes for the
    # two fields not included in this count: ChunkID and ChunkSize.
    _chunk_size = b'\x00\x00\x00\x00'
    _chunk_size_int = 0

    def _encode_chunk_size(self):
        self._chunk_size = int(self._chunk_size_int).to_bytes(4, byteorder='little', signed=False)

    def update_chunk_size(self):
        self._chunk_size_int = 36 + self.get_subchunk_2_size()
        self._encode_chunk_size()

    def get_chunk_size(self):
        self.update_chunk_size()
        return self._chunk_size_int

    # Format ###################################################################

    # Offset: 8, Size: 4, Endian: big
    # Contains the letters 'WAVE'
    # (0x57415645 big-endian form)
    _format = b'WAVE'

    ############################################################################
    # The 'WAVE' format consists of two subchunks: 'fmt ' and 'data': ##########

    ############################################################################
    # The 'fmt ' subchunk describes the sound data's format: ###################

    # Subchunk1ID ##############################################################

    # Offset: 12, Size: 4, Endian: big
    # Contains the letters 'fmt '
    # (0x666d7420 big-endian form)
    _subchunk_1_id = b'fmt '

    # Subchunk1Size ############################################################

    # Offset: 16, Size: 4, Endian: little
    # 16 for PCM.  This is the size of the
    # rest of the Subchunk which follows this number.
    _subchunk_1_size = int(16).to_bytes(4, byteorder='little', signed=False)
    _subchunk_1_size_int = 16

    # AudioFormat ##############################################################

    # Offset: 20, Size: 2, Endian: little
    # PCM = 1 (i.e. Linear quantization)
    # Values other than 1 indicate some form of compression.
    _audio_format = int(1).to_bytes(2, byteorder='little', signed=False)

    # NumChannels ##############################################################

    # Offset: 22, Size: 2, Endian: little
    # Mono = 1, Stereo = 2, etc.
    _num_channels = b'\x00\x00'
    _num_channels_int = 0

    def _encode_num_channels(self):
        self._num_channels = int(self._num_channels_int).to_bytes(2, byteorder='little', signed=False)

    def set_num_channels(self, arg_int):
        if arg_int < 1:
            raise ValueError('Channel count can\'t be lower than 1')
        elif arg_int > 8:
            raise ValueError('Channel count can\'t be higher than 8')
        else:
            self._num_channels_int = arg_int

        self._encode_num_channels()
        self.update_byte_rate()
        self.update_block_align()

    def get_num_channels(self):
        return self._num_channels_int

    # SampleRate ###############################################################

    # Offset: 24, Size: 4, Endian: little
    # 8000, 44100, etc.
    _sample_rate = b'\x00\x00\x00\x00'
    _sample_rate_int = 0

    def __encode_sample_rate(self):
        self._sample_rate = int(self._sample_rate_int).to_bytes(4, byteorder='little', signed=False)

    def set_sample_rate(self, arg_int):
        if arg_int < 8000:
            raise ValueError('Channel count can\'t be lower than 8 KHz')
        elif arg_int > 96000:
            raise ValueError('Channel count can\'t be higher than 96 KHz')
        else:
            self._sample_rate_int = arg_int

        self.__encode_sample_rate()
        self.update_byte_rate()

    def get_sample_rate(self):
        return self._sample_rate_int

    # ByteRate #################################################################

    # Offset: 28, Size: 4, Endian: little
    # == SampleRate * NumChannels * BitsPerSample/8
    __byte_rate = b'\x00\x00\x00\x00'
    _byte_rate_int = 0

    def _encode_byte_rate(self):
        self.__byte_rate = int(self._byte_rate_int).to_bytes(4, byteorder='little', signed=False)

    def update_byte_rate(self):
        self._byte_rate_int = self.get_sample_rate() * self.get_num_channels() * self.get_bits_per_sample() / 8
        self._encode_byte_rate()

    def get_byte_rate(self):
        return self._byte_rate_int

    # BlockAlign ###############################################################

    # Offset: 32, Size: 2, Endian: little
    # == NumChannels * BitsPerSample/8
    # The number of bytes for one sample including all channels.
    # I wonder what happens when this number isn't an integer?
    _block_align = b'\x00\x00'
    _block_align_int = 0

    def __encode_block_align(self):
        self._block_align = int(self._block_align_int).to_bytes(2, byteorder='little', signed=False)

    def update_block_align(self):
        self._block_align_int = self.get_num_channels() * self.get_bits_per_sample() / 8
        self.__encode_block_align()

    def get_block_align(self):
        return self._block_align_int

    # BitsPerSample ############################################################

    # Offset: 34, Size: 2, Endian: little
    # 8 bits = 8, 16 bits = 16, etc.
    _bits_per_sample = b'\x00\x00'
    _bits_per_sample_int = 0

    _sample_format = 'U16_LE'

    _min_sample_value = 0
    _max_sample_value = 1

    def __encode_bits_per_sample(self):
        self._bits_per_sample = int(self._bits_per_sample_int).to_bytes(2, byteorder='little', signed=False)

    def set_bits_per_sample(self, arg_int):
        if arg_int == 8:
            self._bits_per_sample_int = 8
        elif arg_int == 16:
            self._bits_per_sample_int = 16
        elif arg_int == 24:
            self._bits_per_sample_int = 24
        elif arg_int == 32:
            self._bits_per_sample_int = 32
        else:
            raise ValueError('Bits per Sample: 8, 16, 24 or 32')

        self.__encode_bits_per_sample()
        self.update_byte_rate()
        self.update_block_align()
        self.update_sample_format()
        self.update_max_sample_value()

    def get_bits_per_sample(self):
        return self._bits_per_sample_int

    @staticmethod
    def is_sample_type_signed():
        return False

    @staticmethod
    def get_sample_endianness():
        return 'little'

    @staticmethod
    def get_sample_endian_short():
        return 'LE'

    def update_sample_format(self):
        local_bits_per_sample_int = self.get_bits_per_sample()
        self._sample_format = 'U' + str(local_bits_per_sample_int)

        if local_bits_per_sample_int > 8:
            self._sample_format += '_' + self.get_sample_endian_short()

    def get_sample_format(self):
        return self._sample_format

    def get_min_sample_value(self):
        return self._min_sample_value

    def update_max_sample_value(self):
        self._max_sample_value = pow(2, self.get_bits_per_sample()) - 1

    def get_max_sample_value(self):
        return self._max_sample_value

    ############################################################################

    # Offset: ---, Size: 2, Endian: little
    # if PCM, then doesn't exist
    # ExtraParamSize

    # Offset: ---, Size: X, Endian: little
    # space for extra parameters
    # ExtraParams

    ############################################################################
    # The 'data' subchunk contains the size of the data and the actual sound: ##

    # Subchunk2ID ##############################################################

    # Offset: 36, Size: 4, Endian: big
    # Contains the letters 'data'
    # (0x64617461 big-endian form)
    _subchunk_2_id = b'data'

    # Subchunk2Size ############################################################

    # Offset: 40, Size: 4, Endian: little
    # == NumSamples * NumChannels * BitsPerSample/8
    # This is the number of bytes in the data.
    # You can also think of this as the size
    # of the read of the subchunk following this number.
    _subchunk_2_size = b'\x00\x00\x00\x00'
    _subchunk_2_size_int = 0

    def _encode_subchunk_2_size(self):
        self._subchunk_2_size = int(self._subchunk_2_size_int).to_bytes(4, byteorder='little', signed=False)

    def update_subchunk_2_size(self):
        self._subchunk_2_size_int = len(self.get_data())
        self._encode_subchunk_2_size()

    def get_subchunk_2_size(self):
        self.update_subchunk_2_size()
        return self._subchunk_2_size_int

    # Data #####################################################################

    # Offset: 44, Size: *, Endian: little
    # The actual sound data.
    _data = bytes()
    _data_bytearray = bytearray()

    def _encode_data(self):
        self._data = bytes(self._data_bytearray)

    def _extend_data(self, arg_bytearray):
        self._data_bytearray.extend(arg_bytearray)

    # convert DataBytearray to inmutable bytes in Data and update sizes
    def update_data(self):
        self._encode_data()
        self.update_chunk_size()

    def get_data(self):
        return self._data_bytearray

    def add_sample(self, arg_int_list):
        # argIntList: one integer per channel in this sample
        print('Adding sample ', str(arg_int_list))

        if len(arg_int_list) != self.get_num_channels():
            raise ValueError('More values in current sample than channels available')

        bytes_per_sample = int(self.get_bits_per_sample() / 8)

        for i in range(len(arg_int_list)):

            if arg_int_list[i] < self.get_min_sample_value():
                raise ValueError('A value inside the sample is too low')

            if arg_int_list[i] > self.get_max_sample_value():
                raise ValueError('A value inside the sample is too high')

            sample_part_bytes = int(arg_int_list[i]).to_bytes(bytes_per_sample, byteorder='little', signed=False)
            self._extend_data(bytearray(sample_part_bytes))

    # OTHER ####################################################################

    def write_to_file(self, arg_file_name='output.wav'):

        self.update_data()

        print('WRITING AUDIO DATA TO FILE')

        print('Number of channels:  ', str(self.get_num_channels()))
        print('Sample Rate:         ', str(self.get_sample_rate()), ' Hz')
        print('Bits per Sample:     ', str(self.get_bits_per_sample()))
        print('Sample Format:       ', str(self.get_sample_format()))

        print('Opening file \'', arg_file_name, '\' for writing...', end='')

        f = open(arg_file_name, 'wb')

        print('... done.')

        print('Writing RIFF header...', end='')

        f.write(self._chunk_id)         # size:  4 Bytes
        f.write(self._chunk_size)       # size:  4 Bytes
        f.write(self._format)          # size:  4 Bytes

        print('... done.')

        print('Writing \'fmt \' subchunk...', end='')

        f.write(self._subchunk_1_id)     # size:  4 Bytes
        f.write(self._subchunk_1_size)   # size:  4 Bytes
        f.write(self._audio_format)     # size: 2 Bytes
        f.write(self._num_channels)     # size: 2 Bytes
        f.write(self._sample_rate)      # size:  4 Bytes
        f.write(self.__byte_rate)        # size:  4 Bytes
        f.write(self._block_align)      # size: 2 Bytes
        f.write(self._bits_per_sample)   # size: 2 Bytes

        print('... done.')

        print('Writing \'data\' subchunk...', end='')

        f.write(self._subchunk_2_id)     # size:  4 Bytes
        f.write(self._subchunk_2_size)   # size:  4 Bytes
        f.write(self._data)            # size: * Bytes

        print('... done.')

        print('Closing file...', end='')

        f.close()

        print('... done.')

    # END ######################################################################
