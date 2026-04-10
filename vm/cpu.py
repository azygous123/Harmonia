from email.policy import default
from vm.instruction import Instruction
from vm.program import Program


class CPU():
    def __init__(self):
        self.PC = 0
        self.SREG = 0
        self.SPH = 0x08
        self.SPL = 0xFF
        self.SP = 0x08FF
        self.registers = [0] * 32
        self.memory = [0] * 0x900
        self.tagflag = True #when a cpu hasn't run yet we can just call tag instruction with the needed tag as "main"
        self.tag = "main"
        self.alu1 = 0
        self.alu2 = 0
        self.register_window = None
        self.memory_window = None



    def run(self, instructions):
        currprogram = Program(instructions)
        locNextInst = 0
        upperBound = len(currprogram.instructions)
        InstName = None
        OpA = None
        OpB = None
        testA = False
        testB = False



        while (locNextInst != upperBound):
            # for each loop we need to fetch next instruction unless the tag flag is set
            # the tag flag is set when we need to jump to a lable instead
            if (self.tagflag):
                locNextInst = currprogram.fetch_instruction(self.tag)
                nextInst = currprogram.instructions[locNextInst]
                self.tagflag = False
            else:
                nextInst = currprogram.instructions[locNextInst]
            locNextInst += 1 #increment to get to the next instruction for the next loop
            
            # We are grouping instructions into three types: Labels, Instructions and Operands. 
            # If we encounter a label then we need to find the location of the instruction immediately following that label
            # If we encounter an instruction we need to take the next OP or next two OPS and execute the instruction with
            # the OPs as operands. 

            # I need a way to know which OP I'm at for the instruction.
            # what we will do is keep the OpA and OpB variables declared outside of the loop.
            # 

            #--3 cases for the instruction types: LBL, IN, OP--

            # - LBL: we need to set the tag flag to true and continue
            #done
            if (nextInst.instType == "LBL"):
                self.tagflag = True
                continue

            # IN: set testA continue to next to find operands
            # done, checked if it's an "in", now validate
            if (nextInst.instType == "IN"):
                if (testA):
                    print("Error: IN instruction without an operand")
                    return 
                else:
                    testA = True
                    print ("TestA true")
                    InstName = nextInst.op
                continue


            if (nextInst.instType == "OP"):
                if (testA):
                    OpA = nextInst.op
                    testB = True
                    testA = False
                    print ("TestB true")
                elif(testB):
                    OpB = nextInst.op
                    testB = False
                    testA = False
                    print ("Executing Command")
                    # here is where the execution phase should behing with fetching values from addresses
                    # then performing th instruction
                    # writeback and move on to the next instruction "Continue"
                    self.executePhase(InstName, OpA, OpB)



                else:
                    print("Error: OP instruction without an operand")
                    return

                continue




        #doublecheck off by 1 error in fetch instruction
        #simply adjust accordingly if there is one
    def executePhase(self, inst, opA, opB):
        print(f"Executing {inst} with operands {opA} and {opB}")
        # here is where we will execute the instruction with the operands
        # this is going to be a big switch statement that checks the instruction and executes it accordingly)
        match inst:
            case "ADD":
                self.alu1 = self.fetchOperand(opA, "reg")
                self.alu2 = self.fetchOperand(opB, "reg")
                result = self.alu1 + self.alu2

                self.registers[int(opA[1:])] = result & 0xFF

                self.update_ui()
            case "SUB":
                self.alu1 = self.fetchOperand(opA, "reg")
                self.alu2 = self.fetchOperand(opB, "reg")
                result = self.alu1 - self.alu2

                self.registers[int(opA[1:])] = result & 0xFF

                self.update_ui()
            case "MOV":
                self.alu1 = self.fetchOperand(opB, "reg")

                result = self.alu1

                self.registers[int(opA[1:])] = result & 0xFF
                self.update_ui()
            case "LDI":
                self.registers[int(opA[1:])] = int(opB, 0) & 0xFF
                self.update_ui()
            case _:
                print(f"Error: Instruction {inst} not implemented yet")

    def fetchOperand(self,memaddress,memtype):
        match memtype:
            case "reg":
                memaddress = int(memaddress[1:]) 
                return self.registers[memaddress]
            case "mem":
                pass
            case _:
                return 0
                
                # probably just have it return back the value input because it's an immediate value
                # then I can still just use it in the ALU and it will work fine (hopefully)
                
    def update_ui(self):
        if self.register_window:
            self.register_window.refresh()
        if self.memory_window:
            self.memory_window.refresh()

