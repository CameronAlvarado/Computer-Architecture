"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 255
        self.reg = [0] * 8
        self.pc = 0
        self.fl = 0

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr
        return self.ram[mar]

    def load(self, program):
        """Load a program into memory."""
        path = sys.argv[1]
        # Checks if file exists
        try:
            with open(path, 'r') as f:
                contents = f.read()
                cpu.load(contents)

                address = 0

                for line in program:
                    line = line.split('#', 1)[0]
                    print("Line:", line)
                    value = line.rstrip()
                    if value == "":
                        continue
                    num = '{0:08b}'.format(int(value))
                    # print(num)
                    self.ram_write(line, address)
                    address += 1
        except:
            print("EXCEPTION")

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8     | - 3 slots
        #     0b00000000,  # | -
        #     0b00001000,  # | -
        #     0b01000111,  # PRN R0       | - 2 slots
        #     0b00000000,  # | -
        #     0b00000001,  # HLT
        # ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        # Set flag register
        self.reg[self.fl] = 0
        # Instructions Decoded from LS8-spec
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010

        while True:
            # This is the Instruction Register as 'command'
            command = self.ram_read(self.pc)
            #  op_a needs to read next byte after PC
            operand_a = self.ram_read(self.pc + 1)
            #  op_b needs to read next 2 bytes after PC
            operand_b = self.ram_read(self.pc + 2)
            # print('Running ---', IR)

            if command == HLT:
                print("HALT")
                running = False
                sys.exit(0)

            if command == MUL:
                # Multiply the values in two registers together and store in reg A
                mult = operand_a * operand_b
                self.reg[operand_a] = mult
                self.pc += 3
                self.trace()

            if command == LDI:
                # LDI: register immediate. Set the value of a register to an integer
                # Now put value in correct register
                print("LDI runs first")
                self.reg[operand_a] = operand_b
                print("reg", self.reg)
                # used both, so advance by 3 to start at next correct value
                # op_a will be 1 ahead from current pos, op_b 2
                print("PC", self.pc)
                # self.trace()
                self.pc += 3

            if command == PRN:
                # PRN: register pseudo-instruction
                # print numeric value stored in given register
                print(self.reg[operand_a])
                # self.trace()
                print("reg", self.reg)
                print("PC", self.pc)
                self.pc += 2

            else:
                # self.trace()
                print("------------------")
                print("IR, 130 = LDI =>", command)
                print("PC", self.pc)
                print("reg", self.reg)
                print("op_a", operand_a)
                print("op_b", operand_b)
                print("------------------")
