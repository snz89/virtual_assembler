import unittest
import os
from assembler.assembler import Assembler
from assembler.config import LOAD_CONST


class TestAssembler(unittest.TestCase):
    def setUp(self):
        """Creates an Assembler obj and temporary files for testing."""
        self.assembler = Assembler()
        self.input_file = os.path.join("tests", "test_input.asm")
        self.binary_file = os.path.join("tests", "test_output.bin")
        self.log_file = os.path.join("tests", "test_log.xml")

    def tearDown(self):
        """Deletes temporary files after tests have been run."""
        for file in [self.input_file, self.binary_file, self.log_file]:
            if os.path.exists(file):
                os.remove(file)

    def write_input_file(self, lines):
        with open(self.input_file, "w") as f:
            f.write("\n".join(lines))

    def test_assemble_load_const(self):
        self.write_input_file(["load_const 179"])
        self.assembler.assemble(self.input_file, self.binary_file, self.log_file)

        with open(self.binary_file, "rb") as f:
            binary_data = f.read()
        expected_binary = bytearray(
            [(LOAD_CONST & 0x07) | ((179 & 0x1F) << 3), (179 >> 5) & 0xFF]
        )
        self.assertEqual(binary_data, expected_binary)

        with open(self.log_file, "r", encoding="utf-8") as f:
            log_data = f.read()
        self.assertIn("<opcode>2</opcode>", log_data)
        self.assertIn("<operand>179</operand>", log_data)

    def test_assemble_multiple_commands(self):
        commands = [
            "load_const 179",
            "store_mem 1",
            "load_mem 1",
            "sgn",
        ]
        self.write_input_file(commands)
        self.assembler.assemble(self.input_file, self.binary_file, self.log_file)

        with open(self.binary_file, "rb") as f:
            binary_data = f.read()
        self.assertEqual(len(binary_data), 8)

        with open(self.log_file, "r", encoding="utf-8") as f:
            log_data = f.read()
        self.assertIn("<opcode>2</opcode>", log_data)
        self.assertIn("<opcode>3</opcode>", log_data)
        self.assertIn("<opcode>1</opcode>", log_data)
        self.assertIn("<opcode>4</opcode>", log_data)

    def test_assemble_invalid_command(self):
        self.write_input_file(["unknown_command 123"])
        with self.assertRaises(ValueError):
            self.assembler.assemble(self.input_file, self.binary_file, self.log_file)

    def test_log_file_format(self):
        self.write_input_file(["load_const 10", "store_mem 2"])
        self.assembler.assemble(self.input_file, self.binary_file, self.log_file)

        with open(self.log_file, "r", encoding="utf-8") as f:
            log_data = f.read()
        self.assertTrue(log_data.startswith('<?xml version="1.0" ?>'))
        self.assertIn("<instruction>", log_data)
        self.assertIn("<opcode>2</opcode>", log_data)
        self.assertIn("<operand>10</operand>", log_data)


if __name__ == "__main__":
    unittest.main()
