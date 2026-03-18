from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem


class MemoryWindow(QWidget):
    def __init__(self, cpu):
        super().__init__()

        self.cpu = cpu

        self.setWindowTitle("Memory")

        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Address", "Value"])

        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        self.refresh()

    def refresh(self):
        size = len(self.cpu.memory)
        self.table.setRowCount(size)

        for addr in range(size):
            self.table.setItem(addr, 0, QTableWidgetItem(f"0x{addr:03X}"))
            self.table.setItem(addr, 1, QTableWidgetItem(f"0x{self.cpu.memory[addr]:02X}"))