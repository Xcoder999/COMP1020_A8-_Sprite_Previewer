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
        self.label_slider = QLabel(f"Frame per second: {self.fps}")
        self.label_slider.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.slider = QSlider(Qt.Orientation.Vertical)
        self.slider.setMinimum(1)
        self.slider.setMaximum(30)
        self.slider.setValue(self.fps)
        self.slider.setInvertedAppearance(True)
        self.slider.valueChanged.connect(self.on_fps_changed)

        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")

        self.start_button.clicked.connect(self.start)
        self.stop_button.clicked.connect(self.stop)

        self.animation_start = False
        self.animation_stop = True

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
        slider_layout = QVBoxLayout()
        slider_layout.addWidget(self.label_slider)
        slider_layout.addWidget(self.slider)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.label_chr)
        main_layout.addLayout(slider_layout)
        main_layout.addLayout(button_layout)

        frame.setLayout(main_layout)
        self.setCentralWidget(frame)

    def start(self):
        print("Starting")
        self.animation_start = True
        self.animation_stop = False
    def stop(self):
        print("Stopping")
        self.animation_stop = True
        self.animation_start = False

    def next_frame(self):
        if self.animation_start == True and self.animation_stop == False:
            self.current_frame = (self.current_frame + 1) % self.num_frames
            self.label_chr.setPixmap(self.frames[self.current_frame])
        else:
            self.current_frame = (self.current_frame + 0) % self.num_frames
            self.label_chr.setPixmap(self.frames[self.current_frame])

    def on_fps_changed(self, value):
        self.fps = value
        self.label_slider.setText(f"Frame per second: {value}")
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
