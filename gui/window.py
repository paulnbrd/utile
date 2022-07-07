from PyQt6 import QtCore, QtWidgets, QtGui
from typing import Any

from gui.modules.YoutubeDownloader import YoutubeDownloader


class Window(QtWidgets.QMainWindow):
    def __init__(self, *args: Any, **kwds: Any) -> Any:
        super().__init__(*args, **kwds)

        self.setWindowTitle("Paulinux Corp CLI GUI")
        self.resize(600, 500)

        # SETUP
        self.central_layout = QtWidgets.QVBoxLayout()
        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

        # SELECT MODULE BUTTONS
        self.button_panel_container = QtWidgets.QWidget()
        self.button_panel = QtWidgets.QHBoxLayout()
        self.button_panel_container.setLayout(self.button_panel)

        self.yt_downloader_select_button = QtWidgets.QPushButton()
        self.yt_downloader_select_button.setText("Youtube Downloader")
        self.yt_downloader_select_button.clicked.connect(
            lambda: self.select_module("youtube_downloader"))
        self.button_panel.addWidget(self.yt_downloader_select_button)

        self.select_convert_image = QtWidgets.QPushButton()
        self.select_convert_image.setText("Conversion d'image")
        self.select_convert_image.setDisabled(True)
        self.button_panel.addWidget(self.select_convert_image)

        self.central_layout.addWidget(self.button_panel_container)

        self.close_module_button = QtWidgets.QPushButton("Retour")
        self.close_module_button.clicked.connect(
            lambda: self.select_module(None))
        self.close_module_button.hide()
        self.central_layout.addWidget(self.close_module_button)

        # MODULES

        self.modules_layout = QtWidgets.QVBoxLayout()
        self.central_layout.addLayout(self.modules_layout)

        self.youtube_downloader = YoutubeDownloader()
        self.youtube_downloader.hide()
        self.modules_layout.addWidget(self.youtube_downloader)

        # SHOW
        self.show()

    def select_module(self, module_name: str):
        if module_name == "youtube_downloader":
            self.button_panel_container.hide()
            self.close_module_button.show()
            self.youtube_downloader.show()
            self.youtube_downloader.text_input.setFocus()
        else:
            self.button_panel_container.show()
            self.close_module_button.hide()
            self.youtube_downloader.hide()
