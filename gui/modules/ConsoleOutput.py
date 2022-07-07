from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtCore import QProcess
from PyQt6 import QtCore


class ConsoleOutput(QTextEdit):
    def __init__(self):
        super().__init__()

        self.process = QProcess(self)
        self.process.setProgram("py")
        self.process.setProcessChannelMode(
            QProcess.ProcessChannelMode.MergedChannels)
        self.process.readyReadStandardOutput.connect(
            self.onReadyReadStandardOutput)
        self.process.finished.connect(self.onFinished)

        self.setReadOnly(True)
        self.on_finished = None

    def run(self, arguments: list[str]):
        self.clear()
        args = ["cli.py"]
        for a in arguments:
            args.append(a)
        self.process.setArguments(args)
        self.process.start()

    def stop(self):
        self.process.kill()

    @QtCore.pyqtSlot()
    def onReadyReadStandardOutput(self):
        text = self.process.readAllStandardOutput().data().decode()
        self.append(text)

    @QtCore.pyqtSlot()
    def onFinished(self):
        print("Finished")
        if self.on_finished:
            self.on_finished()
