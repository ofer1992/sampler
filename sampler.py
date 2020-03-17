import pyaudio
import wave
import numpy as np
from scipy.io.wavfile import read

class Sample:

    def __init__(self, a, fs):
        """
        we assume mono
        a - array of signal
        fs - sample rate, Hz
        """
        assert(len(a.shape) == 1) # accepting only mono
        self.a = a
        self.fs = fs

    def num_samples(self):
        return self.a.size

    def length(self):
        return self.a.size / fs

    def width(self):
        return self.a.dtype.alignment

    def channels(self):
        return 1 # TODO: mono for now

    def extract(self, start, end):
        return Sample(self.a[start*fs: end*fs], fs)

    def chunkify(self, chunk_size):
        # assume mono
        padded = np.concatenate((self.a, np.array((chunk_size - self.a.size % chunk_size) * [0], dtype=self.a.dtype)))
        assert(padded.dtype == self.a.dtype)
        return padded.reshape(padded.size // chunk_size, chunk_size)

def stretch(sample, factor):
    """
    returns streched sample of length factor*sample.length()
    pitch will be affected
    TODO probably a better algorithm to interpolate stuff
    """
    xp = np.arange(0, sample.num_samples())
    x = np.arange(0, sample.num_samples(), factor)
    stretched = np.interp(x, xp, sample.a)
    stretched = np.array(stretched, dtype=sample.a.dtype)
    return Sample(stretched, sample.fs)

def play_sample(sample):
    p = pyaudio.PyAudio()
    # Play the sound by writing the audio data to the stream
    chunk = 1024  
    stream = p.open(format = p.get_format_from_width(sample.width()),
                    channels = sample.channels(),
                    rate = sample.fs,
                    output = True)
    for c in sample.chunkify(chunk):
        stream.write(c.tobytes())
    stream.close()
    p.terminate()
        
# filename = "C:\\Users\\gil\\Documents\\music projects\\heaven\heaven_choir_mono.wav"

# Open the sound file 
def open_file(fp):
    fs, wf_np = read(fp)
    print("opening")
    return Sample(wf_np, fs)
    # play_sample(stretch(sample.extract(100,120), 1.5))

# Close and terminate the playAudio
