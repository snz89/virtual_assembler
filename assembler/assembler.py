import xml.etree.ElementTree as ET

from typing import List, Dict

from assembler.config import LOAD_CONST, LOAD_MEM, STORE_MEM, SGN


class Assembler:
    def assemble(self, input_file: str, binary_file: str, log_file: str) -> None:
        """Converts the source code of the programme into binary code and saves it to a file."""
        with open(input_file, "r") as f:
            lines = f.readlines()

        binary_data = bytearray()
        log_file_data = []

        for line in lines:
            parts = line.strip().split()
            command = parts[0].lower()

            if command == "load_const":
                opcode = LOAD_CONST
                operand = int(parts[1])
            elif command == "load_mem":
                opcode = LOAD_MEM
                operand = int(parts[1])
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

            # Add the instruction data to log file data for better XML formatting
            log_file_data.append(
                {
                    "opcode": str(opcode),
                    "operand": str(operand),
                    "byte1": str(byte1),
                    "byte2": str(byte2),
                }
            )

        # Saving a binary file
        with open(binary_file, "wb") as f:
            f.write(binary_data)

        # Saving the log file
        self.write_log_file(log_file, log_file_data)

    def write_log_file(
        self, log_file: str, log_file_data: List[Dict[str, str]]
    ) -> None:
        """Saves logs to an xml file"""
        root = ET.Element("log")
        for entry in log_file_data:
            instruction = ET.SubElement(root, "instruction")
            for key, value in entry.items():
                ET.SubElement(instruction, key).text = str(value)

        tree = ET.ElementTree(root)

        with open(log_file, "wb") as f:
            tree.write(f, encoding="utf-8", xml_declaration=True)

        with open(log_file, "r", encoding="utf-8") as f:
            xml_content = f.read()

        import xml.dom.minidom

        pretty_xml = xml.dom.minidom.parseString(xml_content).toprettyxml(indent="  ")

        with open(log_file, "w", encoding="utf-8") as f:
            f.write(pretty_xml)

        print(f"Log written to {log_file}")
