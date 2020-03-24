import pyaudio
import wave
import numpy as np
from scipy.io.wavfile import read
from pyglet.media.codecs.base import StreamingSource, StaticSource, AudioFormat, AudioData
from pyglet.media.codecs import MediaDecoder
import pyglet.media

class Sample:

    def __init__(self, a, params):
        """
        we assume mono
        a - array of signal
        params - following wave.getparams(). we ignore nframes though and calculate directly from array
        """
        assert(len(a.shape) == 1) # accepting only mono
        self.a = a
        self.nchannels, self.sampwidth, self.fs, tmp, self.comptype, self.compname = params
        #nchannels, sampwidth, framerate, nframes, comptype, compname = self._file.getparams()

    def nframes(self):
        return self.a.size

    def length(self):
        return self.a.size / self.fs

    def width(self):
        return self.sampwidth
        # return self.a.dtype.alignment

    def channels(self):
        return self.nchannels # TODO: mono for now

    def data(self):
        return self.a.copy()

    def extract(self, start, end):
        return Sample(self.a[int(start*self.fs): int(end*self.fs)], self.get_params())

    def chunkify(self, chunk_size):
        # assume mono
        padded = np.concatenate((self.a, np.array((chunk_size - self.a.size % chunk_size) * [0], dtype=self.a.dtype)))
        assert(padded.dtype == self.a.dtype)
        return padded.reshape(padded.size // chunk_size, chunk_size)

    def get_params(self):
        return self.channels(), self.width(), self.fs, self.nframes(), self.comptype, self.compname


class SampleSource(StreamingSource):
    def __init__(self, filename, file=None):

        self._file = file.data()

        nchannels, sampwidth, framerate, nframes, comptype, compname = file.get_params()

        self.audio_format = AudioFormat(channels=nchannels, sample_size=sampwidth * 8, sample_rate=framerate)

        self._bytes_per_frame = nchannels * sampwidth
        self._duration = nframes / framerate
        self._duration_per_frame = self._duration / nframes
        self._num_frames = nframes
        self.pos = 0

    def __del__(self):
        pass

    def get_audio_data(self, num_bytes, compensation_time=0.0):
        num_frames = max(1, num_bytes // self._bytes_per_frame)

        if self.pos >= self._file.size:
            return None
        data = self._file[self.pos:self.pos+num_frames].tobytes()
        self.pos += num_frames

        timestamp = self.pos / self.audio_format.sample_rate
        duration = num_frames / self.audio_format.sample_rate
        return AudioData(data, len(data), timestamp, duration, [])

    def seek(self, timestamp):
        pass # I don't think it's important as Source would become static source automatically
        timestamp = max(0.0, min(timestamp, self._duration))
        self.pos = int(timestamp / self._duration_per_frame)


class SampleDecoder(MediaDecoder):

    def get_file_extensions(self):
        return []

    def decode(self, file, filename, streaming=True):
        return StaticSource(SampleSource(filename, file))

class Player:

    def __init__(self):
        self.player = pyglet.media.Player()

    def load(self, sample):
        source = pyglet.media.load('', file=sample, decoder=SampleDecoder())
        self.player.pause()
        self.player.next_source()
        self.player.queue(source)

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.pause()
        self.player.seek(0)

    def time(self):
        return self.player.time

    @staticmethod
    def tick():
        pyglet.clock.tick()

def stretch(sample, factor):
    """
    returns streched sample of length factor*sample.length()
    pitch will be affected
    TODO probably a better algorithm to interpolate stuff
    """
    xp = np.arange(0, sample.nframes())
    x = np.arange(0, sample.nframes(), factor)
    stretched = np.interp(x, xp, sample.a)
    stretched = np.array(stretched, dtype=sample.a.dtype)
    return Sample(stretched, sample.fs)

def play_sample(sample):
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(sample.width()),
                   channels=sample.channels(),
                   rate=sample.fs,
                   output=True)
        # Play the sound by writing the audio data to the stream
    chunk = 1024
    for c in sample.chunkify(chunk):
        stream.write(c.tobytes())
    stream.close()
    p.terminate() # TODO how to handle safely?

# filename = "C:\\Users\\gil\\Documents\\music projects\\heaven\heaven_choir_mono.wav"

# Open the sound file 
def open_file(fp):
    import wave
    with wave.open(fp) as tmp:
        params = tmp.getparams()
    fs, wf_np = read(fp)
    print("opening")
    return Sample(wf_np, params)
    # play_sample(stretch(sample.extract(100,120), 1.5))


# Close and terminate the playAudio
