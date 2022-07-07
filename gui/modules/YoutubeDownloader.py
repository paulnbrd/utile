from PyQt6 import QtCore, QtGui, QtWidgets
from gui.modules.ConsoleOutput import ConsoleOutput


class YoutubeDownloader(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.text_input = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.text_input)

        self.download_button = QtWidgets.QPushButton("Download")
        self.download_button.clicked.connect(self.download)
        self.layout.addWidget(self.download_button)

        self.audio_only_checkbox = QtWidgets.QCheckBox(self)
        self.layout.addWidget(self.audio_only_checkbox)

        self.console_output = ConsoleOutput()
        self.layout.addWidget(self.console_output)

    def disable_all(self):
        self.text_input.setDisabled(True)
        self.download_button.setDisabled(True)
        self.audio_only_checkbox.setDisabled(True)

    def enable_all(self):
        self.text_input.setDisabled(False)
        self.download_button.setDisabled(False)
        self.audio_only_checkbox.setDisabled(False)

    def download(self):
        url = self.text_input.text()
        if url == "":
            return
        self.disable_all()
        self.console_output.on_finished = lambda: self.enable_all()
        if self.audio_only_checkbox.isChecked():
            self.console_output.run(
                ["youtube", url, "--onlyaudio"])
        else:
            self.console_output.run(
                ["youtube", url])
