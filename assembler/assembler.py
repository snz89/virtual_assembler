import xml.etree.ElementTree as ET

from assembler.config import LOAD_CONST, LOAD_MEM, STORE_MEM, SGN


class Assembler:
    def assemble(self, input_file, binary_file, log_file):
        with open(input_file, "r") as f:
            lines = f.readlines()

        binary_data = bytearray()
        root = ET.Element("log")

        for line in lines:
            parts = line.strip().split()
            command = parts[0].lower()

            if command == "load_const":
                opcode = LOAD_CONST
                operand = int(parts[1])
            elif command == "load_mem":
                opcode = LOAD_MEM
                operand = 0
            elif command == "store_mem":
                opcode = STORE_MEM
                operand = int(parts[1])
            elif command == "sgn":
                opcode = SGN
                operand = 0
            else:
                raise ValueError(f"Unknown command: {command}")

            byte1 = (opcode & 0x07) | ((operand & 0x1F) << 3)
            byte2 = (operand >> 5) & 0xFF

            binary_data.extend([byte1, byte2])

            instruction = ET.SubElement(root, "instruction")
            instruction.set("opcode", str(opcode))
            instruction.set("operand", str(operand))

        # Saving a binary file
        with open(binary_file, "wb") as f:
            f.write(binary_data)

        # Saving the log file
        tree = ET.ElementTree(root)
        tree.write(log_file)
