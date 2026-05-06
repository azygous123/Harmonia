from ast import List
from vm.instruction import Instruction

class Program():
    def __init__(self, instructions):
        self.instructions : List[Instruction] = instructions
        self.started = False

    def fetch_instruction(self, tag, instructions):
        # if (tag == "main" and not self.started):
        #     self.started = True
        #     return 0 #this is just here for now 
        loc = 0
        for instr in self.instructions:    #for each token we're counting through to find the location of the label in question so we can jump there
            if instr.op == tag and instr.instType == "LBL":
                return loc # preserve the location of the tag before the instruction 
            loc += 1
        return 0 #didn't find anything was ne

    def getlabel_line(self, tag, instructions):
        linecount = 0
        for instr in self.instructions:    #for each token we're counting through to find the location of the label in question so we can jump there
            if instr.instType == "IN" or instr.instType == "LBL":
                linecount += 1
            if instr.op == tag and instr.instType == "LBL":
                return linecount - 1  # preserve the location of the tag before the instruction             
        return 0 #didn't find anything was ne




