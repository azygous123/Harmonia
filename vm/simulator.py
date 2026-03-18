from pickle import INST
from assembler.parser import Instruction
from vm.cpu import CPU
from vm.memory import Memory
#from vm.registers import Registers
from typing import List

# simulator has a CPU and instructions
class Simulator():
    def __init__(self):
        self._mainCpu = CPU()
        self._mainMemory = Memory()
        self._mainProgram : List[Instruction] = []
        #self._mainRegisters = Registers()
        # now we have initialized everything and it's all in one place ready to go

    def run(self, insts : List[Instruction]): # this is going to take a list of 
        self._mainProgram = insts
