from assembler.lexer import Token
from typing import List

class Parser():
    def __init__(self):
        
        pass

    def Instructions(self, t_list : List[Token]):
        inst = []
        for token in t_list:            
            a = token.type
            b = token.value
            instA = Instruction(a,b)
            inst.append(instA)
        return inst

class Instruction():
    def __init__(self, inst_type, pm):
        self.instType = inst_type
        self.op = pm



        


