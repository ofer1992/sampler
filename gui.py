from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys, os
import sampler
import pyqtgraph as pg
import numpy as np
from waveform import WaveForm

class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        self.fn(*self.args, **self.kwargs)

class PlayerWidget(QWidget):

    def __init__(self, *args, **kwargs):
        super(PlayerWidget, self).__init__(*args, **kwargs)
        self.player = sampler.Player()
        layout = QHBoxLayout()
        play = QPushButton("Play")
        play.clicked.connect(self.player.play)
        pause = QPushButton("Pause")
        pause.clicked.connect(self.player.pause)
        stop = QPushButton("stop")
        stop.clicked.connect(self.player.stop)
        self.sec = QLabel('00:00:00')
        layout.addWidget(play)
        layout.addWidget(pause)
        layout.addWidget(stop)
        layout.addWidget(self.sec)

        self.setLayout(layout)

        self.loaded_sample = None
        self.loop = False
        self.clock = QTimer(self)
        self.clock.start(200)
        self.clock.timeout.connect(self.tick)

    def load(self, sample):
        self.player.load(sample)

    def time(self):
        return self.player.time()

    def tick(self):
        self.player.tick()
        import time
        secs = self.player.time()
        self.sec.setText(f"{time.strftime('%H:%M', time.gmtime(secs))}:{secs%60:.3f}")


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.loaded_sample = None
        window = QWidget()
        self.setCentralWidget(window)
        layout = QVBoxLayout()
        self.filename = QLabel('Hello World!')

        file_btn = QPushButton("Choose File")
        file_btn.clicked.connect(self.getfile)
        layout.addWidget(file_btn)
        self.player = PlayerWidget()
        layout.addWidget(self.player)
        layout.addWidget(self.filename)
        window.setLayout(layout)

        # self.wave_form = WaveForm()
        # self.wave_form.set_parent(layout)
        self.show()

    def getfile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            sys.path[0], "Audio files (*.wav)")
        self.loaded_sample = sampler.open_file(fname[0])
        self.player.load(self.loaded_sample)
        self.filename.setText(os.path.basename(fname[0]))
        # self.wave_form.plot(self.loaded_sample.extract(0, 0.5))

    """
    def playfile(self):
        # TODO hangs program
        if self.loaded_sample is None:
            return
        self.play_sample(self.loaded_sample, False)


    def play_sample(self, sample, loop=False):
        def f():
            if sample is None:
                return
            sampler.play_sample(sample)
            if loop:
                f()
        worker = Worker(f)
        self.threadpool.start(worker)
    """




app = QApplication([])
window = MainWindow()
app.exec_()
