#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""Wave PCM audio
"""

# import: requirements
from tqdm import tqdm


class WavePCMAudio:
    """Wave PCM audio"""

    DEFAULT_NUM_CHANNELS: int = 1
    DEFAULT_SAMPLE_RATE: int = 44100
    DEFAULT_BITS_PER_SAMPLE: int = 16

    # format source: http://soundfile.sapp.org/doc/WaveFormat/
    # The Canonical WAVE PCM Soundfile Format

    def __init__(self,
                 num_channels: int = DEFAULT_NUM_CHANNELS,
                 sample_rate: int = DEFAULT_SAMPLE_RATE,
                 bits_per_sample: int = DEFAULT_BITS_PER_SAMPLE) -> None:
        """Initialize"""

        print('Initializing WavePCMAudioClass object ...', end='')

        # init instance variables
        self._num_channels = self.DEFAULT_NUM_CHANNELS
        self._sample_rate = self.DEFAULT_SAMPLE_RATE
        self._bits_per_sample = self.DEFAULT_BITS_PER_SAMPLE
        self._data = bytearray()

        # init values from arguments
        self.num_channels = num_channels
        self.sample_rate = sample_rate
        self.bits_per_sample = bits_per_sample

        print(' done.')

        self.print_format_info()

    ############################################################################
    # The canonical WAVE format starts with the RIFF header: ###################

    # ChunkID ##################################################################

    # Offset: 0, Size: 4, Endian: big
    # Contains the letters 'RIFF' in ASCII form
    # (0x52494646 big-endian form)

    @property
    def chunk_id(self) -> str:
        """Chunk ID"""

        return 'RIFF'

    @property
    def chunk_id_bytes(self) -> bytes:
        """Chunk ID bytes"""

        return bytes(self.chunk_id, encoding='ASCII')

    # ChunkSize ################################################################

    # Offset: 4, Size: 4, Endian: little
    # 36 + SubChunk2Size, or more precisely:
    # 4 + (8 + SubChunk1Size) + (8 + SubChunk2Size)
    # This is the size of the rest of the chunk following this number.
    # This is the size of the entire file in bytes minus 8 bytes for the
    # two fields not included in this count: ChunkID and ChunkSize.

    @property
    def chunk_size(self) -> int:
        """Chunk size"""

        return 36 + self.subchunk_2_size

    @property
    def chunk_size_bytes(self) -> bytes:
        """Chunk size bytes"""

        return self.chunk_size.to_bytes(4, byteorder='little', signed=False)

    # Format ###################################################################

    # Offset: 8, Size: 4, Endian: big
    # Contains the letters 'WAVE'
    # (0x57415645 big-endian form)

    @property
    def format(self) -> str:
        """Format"""

        return 'WAVE'

    @property
    def format_bytes(self) -> bytes:
        """Format bytes"""

        return bytes(self.format, encoding='ASCII')

    ############################################################################
    # The 'WAVE' format consists of two subchunks: 'fmt ' and 'data': ##########

    ############################################################################
    # The 'fmt ' subchunk describes the sound data's format: ###################

    # Subchunk1ID ##############################################################

    # Offset: 12, Size: 4, Endian: big
    # Contains the letters 'fmt '
    # (0x666d7420 big-endian form)

    @property
    def subchunk_1_id(self) -> str:
        """Subchunk 1 ID"""

        return 'fmt '

    @property
    def subchunk_1_id_bytes(self) -> bytes:
        """Subchunk 1 ID bytes"""

        return bytes(self.subchunk_1_id, encoding='ASCII')

    # Subchunk1Size ############################################################

    # Offset: 16, Size: 4, Endian: little
    # 16 for PCM.
    # This is the size of the rest of the Subchunk which follows this number.

    @property
    def subchunk_1_size(self) -> int:
        """Subchunk 1 size"""

        return 16

    @property
    def subchunk_1_size_bytes(self) -> bytes:
        """Subchunk 1 size bytes"""

        return self.subchunk_1_size.to_bytes(4, byteorder='little', signed=False)

    # AudioFormat ##############################################################

    # Offset: 20, Size: 2, Endian: little
    # PCM = 1 (i.e. Linear quantization)
    # Values other than 1 indicate some form of compression.

    @property
    def audio_format(self) -> int:
        """Audio format"""

        return 1

    @property
    def audio_format_bytes(self) -> bytes:
        """Audio format bytes"""

        return self.audio_format.to_bytes(2, byteorder='little', signed=False)

    # NumChannels ##############################################################

    # Offset: 22, Size: 2, Endian: little
    # Mono = 1, Stereo = 2, etc.

    @property
    def num_channels(self) -> int:
        """Num channels"""

        return self._num_channels

    @num_channels.setter
    def num_channels(self, new_value: int) -> None:
        """Set num channels"""

        if new_value < 1:
            raise ValueError('Channel count can\'t be lower than 1')
        if new_value > 8:
            raise ValueError('Channel count can\'t be higher than 8')

        self._num_channels = new_value

    @property
    def num_channels_bytes(self) -> bytes:
        """Num channels - bytes"""

        return self.num_channels.to_bytes(2, byteorder='little', signed=False)

    # SampleRate ###############################################################

    # Offset: 24, Size: 4, Endian: little
    # 8000, 44100, etc.

    @property
    def sample_rate(self) -> int:
        """Sample rate"""

        return self._sample_rate

    @sample_rate.setter
    def sample_rate(self, new_value: int) -> None:
        """Set - sample rate"""

        if new_value < 8000:
            raise ValueError('Sample rate can\'t be lower than 8 KHz')
        if new_value > 96000:
            raise ValueError('Sample rate can\'t be higher than 96 KHz')

        self._sample_rate = new_value

    @property
    def sample_rate_bytes(self) -> bytes:
        """Sample rate bytes"""

        return self.sample_rate.to_bytes(4, byteorder='little', signed=False)

    # ByteRate #################################################################

    # Offset: 28, Size: 4, Endian: little
    # == SampleRate * NumChannels * BitsPerSample/8

    @property
    def byte_rate(self) -> int:
        """Byte rate"""

        return int(self.sample_rate * self.num_channels * self.bits_per_sample / 8)

    @property
    def byte_rate_bytes(self) -> bytes:
        """Byte rate bytes"""

        return self.byte_rate.to_bytes(4, byteorder='little', signed=False)

    # BlockAlign ###############################################################

    # Offset: 32, Size: 2, Endian: little
    # == NumChannels * BitsPerSample/8
    # The number of bytes for one sample including all channels.
    # I wonder what happens when this number isn't an integer?

    @property
    def block_align(self) -> int:
        """Block align"""

        return int(self.num_channels * self.bits_per_sample / 8)

    @property
    def block_align_bytes(self) -> bytes:
        """Block align bytes"""

        return self.block_align.to_bytes(2, byteorder='little', signed=False)

    # BitsPerSample ############################################################

    # Offset: 34, Size: 2, Endian: little
    # 8 bits = 8, 16 bits = 16, etc.

    @property
    def bits_per_sample(self) -> int:
        """Bits per sample"""

        return self._bits_per_sample

    @bits_per_sample.setter
    def bits_per_sample(self, new_value: int) -> None:
        """Bits per sample"""

        if new_value in {8, 16, 24, 32}:
            self._bits_per_sample = new_value
        else:
            raise ValueError('Valid values for Bits per Sample: 8, 16, 24 or 32')

    @property
    def bits_per_sample_bytes(self) -> bytes:
        """Bits per sample bytes"""

        return self.bits_per_sample.to_bytes(2, byteorder='little', signed=False)

    ######################################

    @property
    def is_sample_format_signed(self) -> bool:
        """Is sample format signed?"""

        return False

    @property
    def sample_format_signed(self) -> str:
        """Sample format signed"""

        return 'S' if self.is_sample_format_signed else 'U'

    @property
    def is_sample_format_big_endian(self) -> bool:
        """Is sample format big endian"""

        return False

    @property
    def sample_format_endian(self) -> str:
        """Sample format endian"""

        return 'BE' if self.is_sample_format_big_endian else 'LE'

    @property
    def sample_format(self) -> str:
        """Sample format"""

        sample_format: str = f'{self.sample_format_signed}{self.bits_per_sample}'

        if self.bits_per_sample > 8:
            sample_format += f'_{self.sample_format_endian}'

        return sample_format

    ######################################

    @property
    def min_sample_value(self) -> int:
        """Min sample value"""

        return 0

    @property
    def max_sample_value(self) -> int:
        """Max sample value"""

        return pow(2, self.bits_per_sample) - 1

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

    @property
    def subchunk_2_id(self) -> str:
        """Subchunk 2 ID"""

        return 'data'

    @property
    def subchunk_2_id_bytes(self) -> bytes:
        """Subchunk 2 ID bytes"""

        return bytes(self.subchunk_2_id, encoding='ASCII')

    # Subchunk2Size ############################################################

    # Offset: 40, Size: 4, Endian: little
    # == NumSamples * NumChannels * BitsPerSample/8
    # This is the number of bytes in the data.
    # You can also think of this as the size
    # of the read of the subchunk following this number.

    @property
    def subchunk_2_size(self) -> int:
        """Subchunk 2 size"""

        return len(self.data)

    @property
    def subchunk_2_size_bytes(self) -> bytes:
        """Subchunk 2 size bytes"""

        return self.subchunk_2_size.to_bytes(4, byteorder='little', signed=False)

    # Data #####################################################################

    # Offset: 44, Size: *, Endian: little
    # The actual sound data.

    @property
    def data(self) -> bytearray:
        """Data"""

        return self._data

    def add_sample(self, channel_values: list[int], mono_to_all: bool = False) -> None:
        """Add sample"""

        print('Adding sample ', str(channel_values))

        if len(channel_values) > self.num_channels:
            raise ValueError('More values in current sample than channels available')

        if len(channel_values) < self.num_channels:
            if len(channel_values) == 1 and mono_to_all:
                channel_values.extend([channel_values[0]] * (self.num_channels - 1))
            else:
                raise ValueError('Less values in current sample than channels available')

        bytes_per_sample = int(self.bits_per_sample / 8)

        for item in channel_values:

            if item < self.min_sample_value:
                raise ValueError('A value inside the sample is too low')

            if item > self.max_sample_value:
                raise ValueError('A value inside the sample is too high')

            sample_part_bytes: bytes = item.to_bytes(bytes_per_sample, byteorder='little', signed=False)
            self._data.extend(bytearray(sample_part_bytes))

    # OTHER ####################################################################

    def print_format_info(self) -> None:
        """Print format info"""

        print('Number of channels:  ', str(self.num_channels))
        print('Sample Rate:         ', str(self.sample_rate) + ' Hz')
        print('Bits per Sample:     ', str(self.bits_per_sample))
        print('Sample Format:       ', str(self.sample_format))

    def write_to_file(self, arg_file_name='output.wav') -> None:
        """Write to file"""

        print('')
        print('WRITING AUDIO DATA TO FILE')

        self.print_format_info()

        print('File name:           ', arg_file_name)

        with open(arg_file_name, 'wb') as fh_wav:

            print('Writing RIFF header ...', end='')

            fh_wav.write(self.chunk_id_bytes)
            fh_wav.write(self.chunk_size_bytes)
            fh_wav.write(self.format_bytes)

            print(' done.')

            print('Writing "fmt " subchunk ...', end='')

            fh_wav.write(self.subchunk_1_id_bytes)
            fh_wav.write(self.subchunk_1_size_bytes)
            fh_wav.write(self.audio_format_bytes)
            fh_wav.write(self.num_channels_bytes)
            fh_wav.write(self.sample_rate_bytes)
            fh_wav.write(self.byte_rate_bytes)
            fh_wav.write(self.block_align_bytes)
            fh_wav.write(self.bits_per_sample_bytes)

            print(' done.')

            print('Writing "data" subchunk.')

            fh_wav.write(self.subchunk_2_id_bytes)
            fh_wav.write(self.subchunk_2_size_bytes)
            for byte in tqdm(self._data):
                fh_wav.write(bytes([byte]))

        print('Finished writing file.')

    # END ######################################################################
