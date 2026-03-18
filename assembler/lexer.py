class Lexer():
    def __init__(self):
        self.INSTRUCTIONS = [
    "ADC",
    "ADD",
    "AND",
    "ANDI",
    "ASR",
    "BRBC",
    "BRBS",
    "CALL",
    "COM",
    "CP",
    "CPI",
    "EOR",
    "IN",
    "JMP",
    "LDI",
    "LDS",
    "LSR",
    "MOV",
    "NEG",
    "NOP",
    "OR",
    "ORI",
    "OUT",
    "POP",
    "PUSH",
    "RCALL",
    "RET",
    "RETI",
    "RJMP",
    "STS"
        ]
    def tokenize(self, line):
        tokens = line.replace(",", "").split()
        inst = []
        for t in tokens:
            if t in self.INSTRUCTIONS:
                tkn = Token(t,"IN")
            else:
                tkn = Token(t,"OP")
            inst.append(tkn)
        return inst

class Token():
    def __init__(self, value, t_type):
        self.value = value
        self.type = t_type

