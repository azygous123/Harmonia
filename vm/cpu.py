from calendar import c
from email.policy import default
from vm.instruction import Instruction
from ui.editor import CodeEditor
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
        self.main_window = None
        self.HighlightedLine = 0
        self.editorOut = None

        #going to attempt adding step
        # execution state
        self.locNextInst = 0
        self.currprogram = None        
        self.tagflag = False
        self.tag = "main"

        # instruction assembly (token parsing)
        self.InstName = None
        self.OpA = None
        self.OpB = None
        self.testA = False
        self.testB = False              
        self.nextInst = None
        #set up
        self.initialized = False

        #highlighter fix
        self.locOfIn = 0
        self.current_index = 0       # points to next LBL or IN token
        self.source_lines = []       # maps instruction/label tokens to editor line numbers
        self.token_to_line = {}      # token index -> real editor line number
        self.max_steps = 10000


    def getHighlightedLine(self):
        return self.HighlightedLine

    def get_pc_from_map(self, instruction_index):
        for pc, value in enumerate(self.map):
            if value == instruction_index:
                return pc
        return -1  # not found

    def step(self, instructions, editor):
        if not self.initialized:
            self.initialize_execution(instructions, editor)

        if self.current_index >= self.upperBound:
            print("End of program")
            return

        curr = self.currprogram.instructions[self.current_index]

        # Case 1: label
        if curr.instType == "LBL":
            self.highlight_token(self.current_index)

            # Move past the label for the next step.
            # The label itself does not execute.
            self.current_index += 1
            return

        # Case 2: instruction
        if curr.instType == "IN":
            inst_name, opA, opB, next_index = self.collect_instruction(self.current_index)

            # Highlight the instruction being executed.
            self.highlight_token(self.current_index)

            # Set PC to this instruction's PC.
            pc = self.get_pc_from_map(self.current_index)
            if pc != -1:
                self.PC = pc

            print(f"Executing {inst_name} with operands {opA} and {opB}")

            branch_taken = self.executePhase(
                inst_name,
                opA,
                opB,
                self.currprogram,
                instructions
            )

            if branch_taken:
                # executePhase already sets self.tag for BRBC/BRBS
                self.current_index = self.currprogram.fetch_instruction(self.tag, instructions)
            else:
                self.current_index = next_index

            # After execution, update PC to the next real instruction if possible.
            self.update_pc_to_next_instruction()

            if self.register_window:
                self.register_window.refresh()

            return

        # Case 3: somehow landed on an operand
        # Skip it so we don't get stuck.
        self.current_index += 1

    def set_highlight_line_lbl(self, linenum):
        #just set the line number we were given with the program line number fetching method.
        self.HighlightedLine = linenum

        if self.main_window:
            self.main_window.highlight_line(linenum)

    def run(self, instructions, editor):
        if not self.initialized:
            self.initialize_execution(instructions, editor)

        steps = 0

        while self.current_index < self.upperBound:
            self.step(instructions, editor)

            steps += 1
            if steps >= self.max_steps:
                print("Run stopped: possible infinite loop")
                return



        #doublecheck off by 1 error in fetch instruction
        #simply adjust accordingly if there is one
    def executePhase(self, inst, opA, opB, currProgram,instructions):
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
                result = self.alu1 + self.alu2 + carry # could be bigger than 8 bits
                
                
                res8 = result & 0xFF
                # V flag set if overflow occured
                sign1 = (self.alu1 ^ self.alu2) #& 0x80 not supposed to happen until after 
                sign2 = (self.alu1 ^ result) #& 0x80
                vcheck = (~sign1 & sign2) & 0x80   #vcheck = ~sign1 & sign2
              
                if(vcheck == 0):
                    self.V = 0
                else:
                    self.V = 1

                #update status register
                #Add instruction 
                # N flag set if result is negative
                if(res8 & 0x80):
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
                outcarry = hcheck1 + hcheck2 + carry
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
                return False

            case "ADD":
                #Fetch the two operands and add them together
                self.alu1 = self.fetchOperand(opA, "reg")
                self.alu2 = self.fetchOperand(opB, "reg")
                result = self.alu1 + self.alu2 # could be bigger than 8 bits
                res8 = result & 0xFF
                print(f"Result = {result}, Res8 = Result & 0xFF = {res8}")


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
                if(res8 & 0x80):
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
                return False

            case "AND":
                #Fetch the two operands and add them together
                self.alu1 = self.fetchOperand(opA, "reg")
                self.alu2 = self.fetchOperand(opB, "reg")
                result = self.alu1 & self.alu2 # could be bigger than 8 bits
                res8 = result & 0xFF

                # V set to 0 
                self.V = 0

                # N = 8th bit value
                if(res8 & 0x80):
                    self.N = 1
                else:
                    self.N = 0

                # S is  N ^ V
                self.S = (self.V ^ self.N)

                # Z set to 0 if result was zero
                if(res8 == 0):
                    self.Z = 1
                else:
                    self.Z = 0

                #bits not set ITHC
                self.I = 2 #2 means ignore it and move on, only 1 and 0 are valid and forcefully updated each cycle
                self.T = 2
                self.H = 2
                self.C = 2

                self.registers[int(opA[1:])] = res8                  
                self.update_ui()
                return False

            case "ANDI":         
                #Fetch the two operands and add them together
                self.alu1 = self.fetchOperand(opA, "reg")
                bval = int(opB, 0) & 0xFF
                result = self.alu1 & bval # could be bigger than 8 bits
                res8 = result & 0xFF

                # V set to 0 
                self.V = 0

                # N = 8th bit value
                if(res8 & 0x80):
                    self.N = 1
                else:
                    self.N = 0

                # S is  N ^ V
                self.S = (self.V ^ self.N)

                # Z set to 0 if result was zero
                if(res8 == 0):
                    self.Z = 1
                else:
                    self.Z = 0

                #bits not set ITHC
                self.I = 2 #2 means ignore it and move on, only 1 and 0 are valid and forcefully updated each cycle
                self.T = 2
                self.H = 2
                self.C = 2

                self.registers[int(opA[1:])] = res8                  
                self.update_ui()
                return False

            case "ASR":
                print("ASR Running...")

                self.alu1 = self.fetchOperand(opA, "reg")
                print(f"This is the value of {opA}: {self.alu1}" )
                lowbit = self.alu1 & 0x01
                print(f"Lowbit {lowbit}")
                result = self.alu1 >>1
                
                print(f"Here's the result: {result}'")
                self.registers[int(opA[1:])] = result & 0xFF 
                print(f"Status Regrister before arithmatic bitwise shift right: {self.SREG} ")
                print(f"We gotta do some tests... checking the status register bits S,V,N,Z,C")
                print(f"These are the one's we're not testing...I, T, H")
                
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
                    self.Z = 1
                else:
                    self.Z = 0

                #C bit
                self.C = lowbit

                #S bit
                self.V = self.N ^ self.C

                #V bit
                self.S = self.N ^ self.V

                              
                print("Back to now that bits are set now...")
                # SREG bits we do not I, T, H

                self.I = 2
                self.T = 2
                self.H = 2
                self.update_ui()
                return False

            case "BRBC": #branch if bit clear (= 0) 
                # We need to update the PC if Bit Clear
                # How do we find the location of the instruction?
                initVal = 1
                mul = int(opA)
                for i in range(mul):
                    initVal *= 2
                testVal = self.SREG & initVal

                if (testVal == 0):
                    #branch here
                    # branch logic works by looking up the next instruction based on the tag
                    incouter = 0
                   # for insg in instructions
                    self.tag = opB # this is the lable we need'
                    #locationWeNeed = currProgram.fetch_instruction(self.tag, instructions)    
                    self.I = 2
                    self.T = 2
                    self.H = 2
                    self.S = 2
                    self.V = 2
                    self.N = 2
                    self.Z = 2
                    self.C = 2               
                    return True                  
                else:
                    # No SREG effected 
                    self.I = 2
                    self.T = 2
                    self.H = 2
                    self.S = 2
                    self.V = 2
                    self.N = 2
                    self.Z = 2
                    self.C = 2
                    return False
                #locNextInst = currprogram.fetch_instruction(self.tag)
                #nextInst = currprogram.instructions[locNextInst] ##  
                #self.tagflag = False
            case "BRBS": #branch if bit clear (= 0) 
                # We need to update the PC if Bit Clear
                # How do we find the location of the instruction?
                initVal = 1
                mul = int(opA)
                for i in range(mul):
                    initVal *= 2
                testVal = self.SREG & initVal

                if (testVal != 0):
                    #branch here
                    # branch logic works by looking up the next instruction based on the tag
                    incouter = 0
                   # for insg in instructions
                    self.tag = opB # this is the lable we need'
                    #locationWeNeed = currProgram.fetch_instruction(self.tag, instructions)
                    self.I = 2
                    self.T = 2
                    self.H = 2
                    self.S = 2
                    self.V = 2
                    self.N = 2
                    self.Z = 2
                    self.C = 2                   
                    return True                  
                else:
                    # No SREG effected 
                    self.I = 2
                    self.T = 2
                    self.H = 2
                    self.S = 2
                    self.V = 2
                    self.N = 2
                    self.Z = 2
                    self.C = 2
                    #self.PC += 1
                    return False
                #locNextInst = currprogram.fetch_instruction(self.tag)
                #nextInst = currprogram.instructions[locNextInst] ##  
                #self.tagflag = False
                
            case "COM":
                print("COM Running...")

                self.alu1 = self.fetchOperand(opA, "reg")

                result = ~self.alu1 #1s complement
                res8 = result & 0xFF # 8 bit version

                self.registers[int(opA[1:])] = res8

                # Bits we copy S,V,N,Z,C
                #starting with N
                if (result & 0x80):
                    #n set if MSB is set
                    self.N = 1
                else:
                    self.N = 0

                #z bit 
                if (result == 0):
                    self.Z = 1
                else:
                    self.Z = 0

                #C bit
                self.C = 1

                #V bit
                self.V = 0

                #S bit
                self.S = self.N ^ self.V

                              
                # SREG bits we do not I, T, H

                self.I = 2
                self.T = 2
                self.H = 2
                self.update_ui()
                return False
            
                
            case "SUB":
                self.alu1 = self.fetchOperand(opA, "reg")
                self.alu2 = self.fetchOperand(opB, "reg")
                result = self.alu1 - self.alu2

                self.registers[int(opA[1:])] = result & 0xFF

                self.update_ui()
                return False
            case "MOV":
                self.alu1 = self.fetchOperand(opB, "reg")

                result = self.alu1

                self.registers[int(opA[1:])] = result & 0xFF
                self.update_ui()
                return False

            case "NEG":
                # Fetch operand
                self.alu1 = self.fetchOperand(opA, "reg")                
                result = 0 - self.alu1               
                res8 = result & 0xFF

                self.registers[int(opA[1:])] = res8

                # Z flag
                if res8 == 0:
                    self.Z = 1
                else:
                    self.Z = 0

                # N flag (bit 7)
                if res8 & 0x80:
                    self.N = 1
                else:
                    self.N = 0

                # V flag (overflow only if result == 0x80)
                if res8 == 0x80:
                    self.V = 1
                else:
                    self.V = 0

                # S flag
                self.S = self.N ^ self.V

                # C flag (set if original value != 0)
                if self.alu1 != 0:
                    self.C = 1
                else:
                    self.C = 0

                # H flag (borrow from bit 3)
                if (self.alu1 & 0x0F) != 0:
                    self.H = 1
                else:
                    self.H = 0

                # I, T not affected
                self.I = 2
                self.T = 2

                self.update_ui()
                return False

            case "LDI":
                self.registers[int(opA[1:])] = int(opB, 0) & 0xFF
                self.update_ui()          
           
                return False
            case "NOP":
                self.I = 2
                self.T = 2
                self.H = 2
                self.S = 2
                self.V = 2
                self.N = 2
                self.Z = 2
                self.C = 2
                self.update_ui()
                return False
            case _:
                print(f"Error: Instruction {inst} not implemented yet")
                return False

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
        self.printSReg()
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

    def set_highlight_line(self, linenum):
        program_text = self.editorOut.toPlainText()
        count = 0
        rlcount = 0        
        for line in program_text.splitlines():
            if count == linenum:
                break
            if (":" not in line):                
                count += 1;
            rlcount += 1        
        #if (foundtag):
            #line += 1
        self.HighlightedLine = rlcount

        if self.main_window:
            self.main_window.highlight_line(rlcount)
    
    def set_highlight_line_run(self, line):
        program_text = self.editorOut.toPlainText()
        count = 0
        rlcount = 0
        foundtag = False
        for line in program_text.splitlines():
            if count == line:
                break
            if (":" in line):
                foundtag = True
            else:
                count += 1;
            rlcount += 1
        line = rlcount
        #if (foundtag):
            #line += 1
        self.HighlightedLine = line

        if self.main_window:
            self.main_window.highlight_line(line)


    def reset(self):
        self.initialized = False
        self.registers = [0] * 32
        self.memory = [0] * 0x900
        self.PC = 0
        self.SREG = 0
        self.SPH = 0x08
        self.SPL = 0xFF

        self.current_index = 0
        self.token_to_line = {}
        self.currprogram = None

        self.update_ui()
        #now we can just hit run or step again it will reinitialize everything and start from the beginning of the program
        # run should have no issue happening after step or reset because everything is tied to global state variables that work 
        # as an extension of the run functionality.
        # step should also have no issue happening after run or reset for the same reason as run

    def populateMap(self, instructions):
        self.map = []

        two_word_ops = {"CALL", "JMP", "LDS", "STS"}

        i = 0
        n = len(instructions)

        while i < n:
            inst = instructions[i]

            # Only care about real instructions
            if inst.instType == "IN":
                op = inst.op.upper()

                # Add mapping for this instruction
                self.map.append(i)

                if op in two_word_ops:
                    # Add twice for 2-word instruction
                    self.map.append(i)

            i += 1
    
    def initialize_execution(self, instructions, editor):
        self.initialized = True
        self.editorOut = editor
        self.currprogram = Program(instructions)
        self.populateMap(self.currprogram.instructions)

        self.current_index = 0
        self.upperBound = len(self.currprogram.instructions)

        self.InstName = None
        self.OpA = None
        self.OpB = None

        self.build_token_line_map(editor)
        self.PC = 0

    def build_token_line_map(self, editor):
        self.token_to_line = {}

        program_text = editor.toPlainText()
        real_lines = program_text.splitlines()

        token_index = 0

        for real_line_number, line in enumerate(real_lines):
            stripped = line.strip()

            if stripped == "":
                continue

            # Find next useful parser token
            while token_index < len(self.currprogram.instructions):
                inst = self.currprogram.instructions[token_index]

                if inst.instType == "LBL":
                    self.token_to_line[token_index] = real_line_number
                    token_index += 1
                    break

                if inst.instType == "IN":
                    self.token_to_line[token_index] = real_line_number

                    # Skip over operands that belong to this instruction
                    token_index += 1
                    while token_index < len(self.currprogram.instructions):
                        next_inst = self.currprogram.instructions[token_index]
                        if next_inst.instType == "IN" or next_inst.instType == "LBL":
                            break
                        token_index += 1

                    break

                token_index += 1
                
    def highlight_token(self, instruction_index):
        if instruction_index in self.token_to_line:
            line_number = self.token_to_line[instruction_index]
            self.HighlightedLine = line_number

            if self.main_window:
                self.main_window.highlight_line(line_number)

    def update_pc_to_next_instruction(self):
        i = self.current_index

        while i < self.upperBound:
            curr = self.currprogram.instructions[i]

            if curr.instType == "IN":
                pc = self.get_pc_from_map(i)
                if pc != -1:
                    self.PC = pc
                return

            i += 1

    def collect_instruction(self, start_index):
        instr = self.currprogram.instructions[start_index]
        inst_name = instr.op

        operands = []
        i = start_index + 1

        while i < self.upperBound:
            curr = self.currprogram.instructions[i]

            if curr.instType == "IN" or curr.instType == "LBL":
                break

            if curr.instType == "OP":
                operands.append(curr.op)

            i += 1

        opA = operands[0] if len(operands) >= 1 else None
        opB = operands[1] if len(operands) >= 2 else None

        return inst_name, opA, opB, i