from ast import List
from vm.instruction import Instruction

class Program():
    def __init__(self, instructions):
        self.instructions : List[Instruction] = instructions
        self.started = False

    def fetch_instruction(self, tag):
        loc = 0
        for instr in self.instructions:
            if instr.pm == tag:
                return loc + 1
            loc += 1
        return -1 #didn't find anything





