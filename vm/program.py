from ast import List
from vm.instruction import Instruction

class Program():
    def __init__(self, instructions):
        self.instructions : List[Instruction] = instructions
        self.started = False

    def fetch_instruction(self, tag, instructions):
        if (tag == "main" and not self.started):
            self.started = True
            return 0 #this is just here for now 
        loc = 0
        for instr in self.instructions:
            if instr.op == tag and instr.instType == "LBL":
                return loc + 1
            loc += 1
        return 0 #didn't find anything was ne





