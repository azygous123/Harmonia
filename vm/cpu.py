class CPU():
    def __init__(self):
        self.PC = 0
        self.SREG = 0
        self.SPH = 0x08
        self.SPL = 0xFF
        self.SP = 0x08FF
        self.registers = [0] * 32
        self.memory = [0] * 0x900
