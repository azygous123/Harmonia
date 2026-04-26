from calendar import c
from email.policy import default
from vm.instruction import Instruction
from vm.program import Program
IO_OFFSET = 0x20
SREG_ADDR = 0x5F

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
        self.I = 0
        self.T = 0
        self.H = 0
        self.S = 0
        self.V = 0
        self.N = 0
        self.Z = 0
        self.C = 0
        self.map = []

    def populateMap(self, instructions):
        currprogram = Program(instructions)
        locNextInst = 0
        upperBound = len(currprogram.instructions)
        InstName = None
        OpA = None
        OpB = None
        testA = False
        testB = False
        #while(locNextInst != upperBound):


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
                nextInst = currprogram.instructions[locNextInst] ##  
                self.tagflag = False
            else:
                nextInst = currprogram.instructions[locNextInst]
            locNextInst += 1 #increment to get to the next instruction for the next loop
            self.PC = locNextInst
            
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
                if (InstName == "ASR"):
                    testB = True
                    testA = False
                    #set to the same lock as 2 op instructions now it will execute
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
        match inst.upper():
            case "ADC":
                #get carry bit
                carry = self.fetchOperand(0x3F, "mem")
                carry = carry & 0x01
                print(f"Carry bit val: {carry}")

                #Fetch the two operands and add them together
                self.alu1 = self.fetchOperand(opA, "reg")
                self.alu2 = self.fetchOperand(opB, "reg")
                result = self.alu1 + self.alu2 # could be bigger than 8 bits
                res8 = result & 0x80
                # V flag set if overflow occured
                sign1 = (self.alu1 ^ self.alu2) #& 0x80 not supposed to happen until after 
                sign2 = (self.alu1 ^ result) #& 0x80
                vcheck = ~sign1 & sign2
                print(f"Sign1 : {sign1}")
                print(f"~Sign1 : {~sign1}")
                print(f"Sign2 : {sign2}")
                print(f"vcheck = {vcheck}")
                vcheck &= 0x80
                if(vcheck == 0):
                    self.V = 0
                else:
                    self.V = 1

                #update status register
                #Add instruction 
                # N flag set if result is negative
                if(result & 0x80):
                    self.N = 1
                else:
                    self.N = 0

                # Z flag set if zero result
                if((result & 0xFF) == 0):
                    self.Z = 1
                else:
                    self.Z = 0
                # H flag set if half carry flag is set
                # if carry from 3rd bit
                hcheck1 = self.alu1 & 0x0F
                hcheck2 = self.alu2 & 0x0F
                #mask off upper bits
                outcarry = hcheck1 + hcheck2
                outcarry = 0x10 & outcarry
                if(outcarry != 0):
                    self.H = 1
                else:
                    self.H = 0
                # if carry from 8th bit then outcarry will not be zero
                # C flag 
                print (f"Result: {result}")
                print (f"Result & 0x100: {result & 0x100}")
                outcarry = 0x100 & result
                if(outcarry != 0):
                    self.C = 1
                else:
                    self.C = 0
                
                self.S = (self.V ^ self.N)
                # flags set H,S,V,N,Z,C
                # bits not set: IT
                self.I = 2 #2 means ignore it and move on, only 1 and 0 are valid and forcefully updated each cycle
                self.T = 2

                self.registers[int(opA[1:])] = res8                
                self.update_ui()


            case "ADD":
                #Fetch the two operands and add them together
                self.alu1 = self.fetchOperand(opA, "reg")
                self.alu2 = self.fetchOperand(opB, "reg")
                result = self.alu1 + self.alu2 # could be bigger than 8 bits
                res8 = result & 0xFF

                # V flag set if overflow occured
                sign1 = (self.alu1 ^ self.alu2) #& 0x80 not supposed to happen until after 
                sign2 = (self.alu1 ^ result) #& 0x80
                vcheck = ~sign1 & sign2
                print(f"Sign1 : {sign1}")
                print(f"~Sign1 : {~sign1}")
                print(f"Sign2 : {sign2}")
                print(f"vcheck = {vcheck}")
                vcheck &= 0x80
                if(vcheck == 0):
                    self.V = 0
                else:
                    self.V = 1

                #update status register
                #Add instruction 
                # N flag set if result is negative
                if(result & 0x80):
                    self.N = 1
                else:
                    self.N = 0

                # Z flag set if zero result
                if(res8 == 0):
                    self.Z = 1
                else:
                    self.Z = 0
                # H flag set if half carry flag is set
                # if carry from 3rd bit
                hcheck1 = self.alu1 & 0x0F
                hcheck2 = self.alu2 & 0x0F
                #mask off upper bits
                outcarry = hcheck1 + hcheck2
                outcarry = 0x10 & outcarry
                if(outcarry != 0):
                    self.H = 1
                else:
                    self.H = 0
                # if carry from 8th bit then outcarry will not be zero
                # C flag 
                print (f"Result: {result}")
                print (f"Result & 0x100: {result & 0x100}")
                outcarry = 0x100 & result
                if(outcarry != 0):
                    self.C = 1
                else:
                    self.C = 0
                
                self.S = (self.V ^ self.N)
                # flags set H,S,V,N,Z,C
                # bits not set: IT
                self.I = 2 #2 means ignore it and move on, only 1 and 0 are valid and forcefully updated each cycle
                self.T = 2

                self.registers[int(opA[1:])] = res8                
                self.update_ui()
            case "AND":
                #Fetch the two operands and add them together
                self.alu1 = self.fetchOperand(opA, "reg")
                self.alu2 = self.fetchOperand(opB, "reg")
                result = self.alu1 & self.alu2 # could be bigger than 8 bits
                res8 = result & 0xFF

                # V set to 0 
                self.V = 0

                # N = 8th bit value
                if(result & 0x80):
                    self.N = 1
                else:
                    self.N = 0

                # S is  N ^ V
                self.S = (self.V ^ self.N)

                # Z set to 0 if result was zero
                if(res8 == 0):
                    self.Z = 0
                else:
                    self.Z = 1

                #bits not set ITHC
                self.I = 2 #2 means ignore it and move on, only 1 and 0 are valid and forcefully updated each cycle
                self.T = 2
                self.H
                self.C

                self.registers[int(opA[1:])] = res8                  
                self.update_ui()
            case "ANDI":         
                #Fetch the two operands and add them together
                self.alu1 = self.fetchOperand(opA, "reg")
                bval = int(opB, 0) & 0xFF
                result = self.alu1 & bval # could be bigger than 8 bits
                res8 = result & 0xFF

                # V set to 0 
                self.V = 0

                # N = 8th bit value
                if(result & 0x80):
                    self.N = 1
                else:
                    self.N = 0

                # S is  N ^ V
                self.S = (self.V ^ self.N)

                # Z set to 0 if result was zero
                if(res8 == 0):
                    self.Z = 0
                else:
                    self.Z = 1

                #bits not set ITHC
                self.I = 2 #2 means ignore it and move on, only 1 and 0 are valid and forcefully updated each cycle
                self.T = 2
                self.H = 2
                self.C = 2

                self.registers[int(opA[1:])] = res8                  
                self.update_ui()
            case "ASR":
                print("ASR Running...")

                self.alu1 = self.fetchOperand(opA, "reg")
                print(f"This is the value of {opA}: {self.alu1}" )
                lowbit = self.alu1 & 0x01
                print(f"Lowbit {lowbit}")
                result = self.alu1 >>1
                print(f"Here's the result: {result}'")

                print(f"Status Regrister before arithmatic bitwise shift right: {self.SREG} ")
                print(f"We gotta do some tests... checking the status register bits S,V,N,Z,C")
                print(f"These are the one's we're not testing...I, T, H")
                self.printSReg()
                print("Just testing it out :P")
                print("Back to testing now...")
                # Bits we copy S,V,N,Z,C
                #starting with N
                if (result & 0x80):
                    #n set if MSB is set
                    self.N = 1
                else:
                    self.N = 0

                #z bit 
                if (result == 0):
                    self.Z == 1
                else:
                    self.Z == 0

                #C bit
                self.C = lowbit

                #S bit
                self.V = self.N ^ self.C

                #V bit
                self.S = self.N ^ self.V







                self.printSReg()
                print("Just testing it out :P")
                print("Back to now that bits are set now...")
                # SREG bits we do not I, T, H

                self.I = 2
                self.T = 2
                self.H = 2
            case "BRBC": #branch if bit clear (= 0) 
                # We need to update the PC if Bit Clear
                # How do we find the location of the instruction?

                #locNextInst = currprogram.fetch_instruction(self.tag)
                #nextInst = currprogram.instructions[locNextInst] ##  
                #self.tagflag = False
                pass

                
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


                    #// READ ME:
                    #// https://www.google.com/search?client=firefox-b-1-d&q=avr+location+memory+of+SREG&fbs=ADc_l-aN0CWEZBOHjofHoaMMDiKpaEWjvZ2Py1XXV8d8KvlI3sbM0Xv-BZKE_VrZb6-djVgPsTSy5UjazDfPq8BLa8BriI08eYAyMPM-9LNl6snbW0RI8x10I65p7k_mDqeHGhWd5G3zo_UP1QuiWQbQdC0uEyj49Iy43Tk0qIMousFs65SKUlmLSf2tVZi7oM3I5JQfNhYdwWzq9bejlmxLE2kuAY1D9A&ved=2ahUKEwiY556IuYKUAxWPEjQIHYnvHN4Q0NsOegQIAxAB&aep=10&ntc=1&mstk=AUtExfAW0oZdu0l_yqmr2AqlIN2R56fCzOkN8v-TtttG-2g1zNkPas-xQiZ-zJnBBRtqlKFRUK1-zXKmMy-uVhHx2WP4_XIrqRMgseD0_E3C4JCEPFYrv2w8LawW_tt_UStCMMfDV_yt9gf23sZU7u3fdsuAFKKkWWTQ-7h5nsP3JI4It7u3mBFEGhyy93xvn3PSjGRyhSdM3_dx6xm7LO51XmZwC47kOCR6jm6xXVYbzJco7ugMv9pz5jIrnw&csuir=1&udm=50
    def fetchOperand(self,memaddress,memtype):
        match memtype:
            case "reg":
                memaddress = int(memaddress[1:]) 
                return self.registers[memaddress]
            case "mem":
                memaddress = int(memaddress) 
                return self.memory[memaddress] #0 indexed IN/OUT if not IN/OUT use offset
            case _:
                return 0
                
                # probably just have it return back the value input because it's an immediate value
                # then I can still just use it in the ALU and it will work fine (hopefully)
         
                
    def update_ui(self):
        self.setSREG()
        if self.register_window:
            self.register_window.refresh()
        if self.memory_window:
            self.memory_window.refresh()
    
    def setSREG(self):
        if(self.I == 1):
            self.SREG |= 0x80
        if(self.T == 1):
            self.SREG |= 0x40
        if(self.H == 1):
            self.SREG |= 0x20
        if(self.S == 1):
            self.SREG |= 0x10
        if(self.V == 1):
            self.SREG |= 0x08
        if(self.N == 1):
            self.SREG |= 0x04
        if(self.Z == 1):
            self.SREG |= 0x02
        if(self.C == 1):
            self.SREG |= 0x01
        
        if(self.I == 0):
            self.SREG &= 0x7F #0111 1111
        if(self.T == 0):
            self.SREG &= 0xBF #1011 1111
        if(self.H == 0):
            self.SREG &= 0xDF #1101 1111
        if(self.S == 0):
            self.SREG &= 0xEF #1110 1111
        if(self.V == 0):
            self.SREG &= 0xF7 #1111 0111
        if(self.N == 0):
            self.SREG &= 0xFB #1111 1011
        if(self.Z == 0):
            self.SREG &= 0xFD #1111 1101
        if(self.C == 0):
            self.SREG &= 0xFE #1111 1110
        self.memory[0x3F] = self.SREG

    def printSReg(self):
        # let's do this 
            #I,T,H,S,V,N,Z,C
            print(f"I = {self.I},T = {self.T},H = {self.H},S = {self.S},V = {self.V},N = {self.N},Z = {self.Z},C = {self.C}")
            