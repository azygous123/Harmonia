from PyQt6.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Harmonia")
        self.resize(1000, 700)

        self._create_menu_bar()

    def _create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        simulator_menu = menu_bar.addMenu("Simulator")