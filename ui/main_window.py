from xml.etree.ElementTree import tostring
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QAction
from ui.editor import CodeEditor
from assembler.assembler import Asslembler
from assembler.parser import Instruction
from typing import List
from ui.register_window import RegisterWindow
from ui.memory_window import MemoryWindow
from vm.cpu import CPU

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Harmonia")
        self.resize(1000, 700)

        self._create_menu_bar()
        self._create_editor()
        

        self.cpu = CPU()

        self.register_window = RegisterWindow(self.cpu)
        self.memory_window = MemoryWindow(self.cpu)


    def _create_menu_bar(self):
        menu_bar = self.menuBar()

        # ===== File Menu =====

        file_menu = menu_bar.addMenu("File") # This will have [New,Open,Save,Save As...,Options,Exit]

        new_action = QAction("New", self)
        open_action = QAction("Open", self)
        save_action = QAction("Save", self)
        exit_action = QAction("Exit", self)

        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # Connect signals
        new_action.triggered.connect(self.new_file)
        open_action.triggered.connect(self.open_file)
        save_action.triggered.connect(self.save_file)
        exit_action.triggered.connect(self.close)

        # ===== Simulator Menu =====
        simulator_menu = menu_bar.addMenu("Simulator")

        run_action = QAction("Run", self)
        step_action = QAction("Step", self)
        reset_action = QAction("Reset", self)

        simulator_menu.addAction(run_action)
        simulator_menu.addAction(step_action)
        simulator_menu.addAction(reset_action)

        run_action.triggered.connect(self.run_simulator)
        step_action.triggered.connect(self.step_simulator)
        reset_action.triggered.connect(self.reset_simulator)

        build_menu = menu_bar.addMenu("Build") # This will have [Assenble, Upload, Upload Image]
        

        # ===== View Menu ===== # This will have [Registers, Memory, Console]
        view_menu = menu_bar.addMenu("View")

        registers_action = QAction("Registers", self)
        memory_action = QAction("Memory", self)

        view_menu.addAction(registers_action)
        view_menu.addAction(memory_action)

        registers_action.triggered.connect(self.show_registers)
        memory_action.triggered.connect(self.show_memory)

    def _create_editor(self):
        self.editor = CodeEditor()
        self.setCentralWidget(self.editor)


    # ===== File Methods =====
    def new_file(self):
        print("New file triggered")
        self.editor.clear()

    def open_file(self):
        print("Open file triggered")

    def save_file(self):
        print("Save file triggered")

    # ===== Simulator Methods =====
    def run_simulator(self):
        print("Run triggered")
        # so we need to make a new instance of the assembler here
        # pass it a reference to the text
        program_text = self.editor.toPlainText()
        asselmbler = Asslembler() # C# would be Assembler assembler = new Assembler()
        instructions : List[Instruction] = asselmbler.assemble(program_text) # this will give us a list of instructions to pass of the the simulator
        for i in instructions:
            print(i.op + " - " + i.instType)

    def step_simulator(self):
        print("Step triggered")

    def reset_simulator(self):
        print("Reset triggered")

    def show_registers(self):
        self.register_window.refresh()
        self.register_window.show()


    def show_memory(self):
        self.memory_window.refresh()
        self.memory_window.show()