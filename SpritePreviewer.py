#COMP1020_A8-_Sprite_Previewer
import math

from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

# This function loads a series of sprite images stored in a folder with a
# consistent naming pattern: sprite_# or sprite_##. It returns a list of the images.
def load_sprite(sprite_folder_name, number_of_frames):
    frames = []
    padding = math.ceil(math.log(number_of_frames - 1, 10))
    for frame in range(number_of_frames):
        folder_and_file_name = sprite_folder_name + "/sprite_" + str(frame).rjust(padding, '0') + ".png"
        frames.append(QPixmap(folder_and_file_name))

    return frames

class SpritePreview(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sprite Animation Preview")
        # This loads the provided sprite and would need to be changed for your own.
        self.num_frames = 21
        self.frames = load_sprite('spriteImages',self.num_frames)
        self.current_frame = 0
        self.fps = 1

        self.label_chr = QLabel()
        self.label_chr.setPixmap(self.frames[0])
        self.label_chr.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_chr.setScaledContents(True)
        self.label_chr.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        # Add any other instance variables needed to track information as the program
        # runs here
        self.label_FPS = QLabel("Frame per second")
        self.label_FPS.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.fps_label = QLabel("0")
        self.fps_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.slider = QSlider(Qt.Orientation.Vertical)
        self.slider.setMinimum(1)
        self.slider.setMaximum(100)
        self.slider.setValue(self.fps)
        self.slider.setInvertedAppearance(True)
        self.slider.setTickPosition(QSlider.TickPosition.TicksRight)
        self.slider.setTickInterval(10)
        self.slider.valueChanged.connect(self.on_fps_changed)

        self.start_and_stop_button = QPushButton("Start")
        self.start_and_stop_button.clicked.connect(self.start_and_stop)

        self.animation_play = False

        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)
        self.timer.start(1000 // self.fps)

        # Make the GUI in the setupUI method
        self.setupUI()


    def setupUI(self):
        # An application needs a central widget - often a QFrame
        frame = QFrame()

        # Add a lot of code here to make layouts, more QFrame or QWidgets, and
        # the other components of the program.
        # Create needed connections between the UI components and slot methods
        # you define in this class.
        fps_layout = QHBoxLayout()
        fps_layout.addWidget(self.label_FPS)
        fps_layout.addWidget(self.fps_label)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_and_stop_button)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.label_chr)
        main_layout.addWidget(self.slider)
        main_layout.addLayout(fps_layout)
        main_layout.addLayout(button_layout)

        frame.setLayout(main_layout)
        self.setCentralWidget(frame)

    def start_and_stop(self):
        if self.animation_play:
            self.timer.stop()
            self.animation_play = False
            self.start_and_stop_button.setText("Start")
        else:
            self.fps = self.slider.value()
            self.timer.start(1000//self.fps)
            self.animation_play = True
            self.start_and_stop_button.setText("Stop")


    def next_frame(self):
        if self.animation_play:
            self.current_frame = (self.current_frame + 1) % self.num_frames
            self.label_chr.setPixmap(self.frames[self.current_frame])
        else:
            self.current_frame = (self.current_frame + 0) % self.num_frames
            self.label_chr.setPixmap(self.frames[self.current_frame])

    def on_fps_changed(self, value):
        self.fps = value
        self.fps_label.setText(str(value))
        self.timer.start(1000 // value)

    # You will need methods in the class to act as slots to connect to signals


def main():
    app = QApplication([])
    # Create our custom application
    window = SpritePreview()
    # And show it
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
