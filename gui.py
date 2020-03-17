from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QFileDialog
import sys, os
import sampler

loaded_sample = None
app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
label = QLabel('Hello World!')
def getfile():
    global loaded_sample, label # TODO globals suck
    fname = QFileDialog.getOpenFileName(window, 'Open file', 
        sys.path[0],"Audio files (*.wav)")
    loaded_sample = sampler.open_file(fname[0])
    label.setText(os.path.basename(fname[0]))

def playfile():
    global loaded_sample # TODO globals suck
    # TODO hangs program
    if loaded_sample is None:
        return
    sampler.play_sample(loaded_sample)

file_btn = QPushButton("Choose File")
file_btn.clicked.connect(getfile)
layout.addWidget(file_btn)
play_btn = QPushButton("Play")
play_btn.clicked.connect(playfile)
layout.addWidget(play_btn)
window.setLayout(layout)
layout.addWidget(label)
window.show()
app.exec_()