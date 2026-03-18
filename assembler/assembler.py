from html import parser
from assembler.lexer import Lexer
from assembler.parser import Parser

class Asslembler():
    def assemble(self, program_text):
        print("Assembling...")
        lexer = Lexer()
        instr = []
        tokens = []
        for line in program_text.splitlines():
            lineToken = lexer.tokenize(line)
            for t in lineToken:
                tokens.append(t)
        # no we've got all our tokens now going to convert them to a list of instructions.
        parser = Parser()
        inst = parser.Instructions(tokens)

        return inst # returning an empty list for now 