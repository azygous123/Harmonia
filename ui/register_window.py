from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from PyQt6.QtCore import Qt


class RegisterWindow(QWidget):
    def __init__(self, cpu):
        super().__init__()

        self.cpu = cpu

        self.setWindowTitle("Registers")

        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Name", "Value"])

        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        self.refresh()

    def refresh(self):
        total_rows = 3 + 32  # PC, SP, SREG + registers
        self.table.setRowCount(total_rows)

        row = 0

        self._set_row(row, "PC", f"0x{self.cpu.PC:04X}")
        row += 1

        self._set_row(row, "SP", f"0x{self.cpu.SP:04X}")
        row += 1

        self._set_row(row, "SREG", f"0x{self.cpu.SREG:02X}")
        row += 1

        for i in range(32):
            self._set_row(row, f"R{i}", f"0x{self.cpu.registers[i]:02X}")
            row += 1

    def _set_row(self, row, name, value):
        self.table.setItem(row, 0, QTableWidgetItem(name))
        self.table.setItem(row, 1, QTableWidgetItem(value))