from assembler.lexer import Token
from typing import List
from vm.instruction import Instruction

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





        


