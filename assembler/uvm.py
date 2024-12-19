import xml.etree.ElementTree as ET
from typing import Tuple
import xml.dom.minidom


class UVM:
    def __init__(self, memory_size: int = 256):
        self.memory = [0] * memory_size
        self.accumulator = 0

    @staticmethod
    def to_signed(value: int, bits: int = 12) -> int:
        """
        Converts an unsigned number to a signed number by the given number of bits.
        """
        max_positive = (1 << (bits - 1)) - 1
        if value > max_positive:
            return value - (1 << bits)
        return value

    @staticmethod
    def to_unsigned(value: int, bits: int = 12) -> int:
        """
        Converts a signed number to an unsigned number by the given number of bits.
        """
        if value < 0:
            return (1 << bits) + value
        return value

    def load_const(self, operand: int) -> None:
        """Loads a constant into the accumulator."""
        self.accumulator = operand

    def load_mem(self, address: int) -> None:
        """Loads a value from memory into the accumulator."""
        self.accumulator = self.to_signed(self.memory[address])

    def store_mem(self, address: int) -> None:
        """Saves the value from the accumulator to memory."""
        self.memory[address] = self.to_unsigned(self.accumulator)

    def sgn(self) -> None:
        """Performs the unary operation sgn on the accumulator."""
        if self.accumulator > 0:
            self.accumulator = 1
        elif self.accumulator < 0:
            self.accumulator = -1
        else:
            self.accumulator = 0

    def execute_instruction(self, opcode: int, operand: int):
        """Executes one instruction."""
        if opcode == 2:  # LOAD_CONST
            self.load_const(operand)
        elif opcode == 1:  # LOAD_MEM
            self.load_mem(operand)
        elif opcode == 3:  # STORE_MEM
            self.store_mem(operand)
        elif opcode == 4:  # SGN
            self.sgn()
        else:
            raise ValueError(f"Unknown opcode: {opcode}")

    def execute(
        self, binary_file: str, result_file: str, memory_range: Tuple[int, int]
    ) -> None:
        """
        Executes a binary file and stores the result in the specified memory range.
        """
        with open(binary_file, "rb") as f:
            program = f.read()

        for i in range(0, len(program), 2):
            byte1 = program[i]
            byte2 = program[i + 1]
            opcode = byte1 & 0b111
            operand = ((byte1 >> 3) | (byte2 << 5)) & 0xFFF
            operand = self.to_signed(operand, bits=12)
            self.execute_instruction(opcode, operand)

        memory_start, memory_end = memory_range
        self.write_result_file(result_file, memory_start, memory_end)

    def write_result_file(
        self, result_file: str, memory_start: int, memory_end: int
    ) -> None:
        """
        Writes the memory values in the range to an XML file.
        """
        root = ET.Element("memory")
        for address in range(memory_start, memory_end + 1):
            cell = ET.SubElement(root, "cell", address=str(address))
            cell.text = str(self.to_signed(self.memory[address]))

        tree = ET.ElementTree(root)
        with open(result_file, "wb") as f:
            tree.write(f, encoding="utf-8", xml_declaration=True)

        with open(result_file, "r", encoding="utf-8") as f:
            xml_content = f.read()

        pretty_xml = xml.dom.minidom.parseString(xml_content).toprettyxml(indent="  ")

        with open(result_file, "w", encoding="utf-8") as f:
            f.write(pretty_xml)

        print(f"Result written to {result_file}")
