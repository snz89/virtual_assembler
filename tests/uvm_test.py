import unittest
import os

from assembler.config import LOAD_CONST, LOAD_MEM, STORE_MEM, SGN
from assembler.uvm import UVM


class TestUVM(unittest.TestCase):
    def setUp(self):
        self.uvm = UVM()

    def test_to_signed(self):
        self.assertEqual(UVM.to_signed(2047), 2047)
        self.assertEqual(UVM.to_signed(2048), -2048)
        self.assertEqual(UVM.to_signed(4095), -1)
        self.assertEqual(UVM.to_signed(0), 0)
        self.assertEqual(UVM.to_signed(1024), 1024)
        self.assertEqual(UVM.to_signed(3072), -1024)

    def test_to_unsigned(self):
        self.assertEqual(UVM.to_unsigned(-2048), 2048)
        self.assertEqual(UVM.to_unsigned(-1), 4095)
        self.assertEqual(UVM.to_unsigned(0), 0)
        self.assertEqual(UVM.to_unsigned(2047), 2047)
        self.assertEqual(UVM.to_unsigned(1024), 1024)
        self.assertEqual(UVM.to_unsigned(-1024), 3072)

    def test_load_const(self):
        self.uvm.load_const(10)
        self.assertEqual(self.uvm.accumulator, 10)
        self.uvm.load_const(-5)
        self.assertEqual(self.uvm.accumulator, -5)
        self.uvm.load_const(0)
        self.assertEqual(self.uvm.accumulator, 0)

    def test_load_mem(self):
        self.uvm.memory[5] = UVM.to_unsigned(15)
        self.uvm.load_mem(5)
        self.assertEqual(self.uvm.accumulator, 15)

        self.uvm.memory[10] = UVM.to_unsigned(-20)
        self.uvm.load_mem(10)
        self.assertEqual(self.uvm.accumulator, -20)

        self.uvm.memory[0] = UVM.to_unsigned(0)
        self.uvm.load_mem(0)
        self.assertEqual(self.uvm.accumulator, 0)

    def test_store_mem(self):
        self.uvm.accumulator = 25
        self.uvm.store_mem(20)
        self.assertEqual(UVM.to_signed(self.uvm.memory[20]), 25)

        self.uvm.accumulator = -10
        self.uvm.store_mem(30)
        self.assertEqual(UVM.to_signed(self.uvm.memory[30]), -10)

        self.uvm.accumulator = 0
        self.uvm.store_mem(40)
        self.assertEqual(UVM.to_signed(self.uvm.memory[40]), 0)

    def test_sgn(self):
        self.uvm.accumulator = 5
        self.uvm.sgn()
        self.assertEqual(self.uvm.accumulator, 1)

        self.uvm.accumulator = -5
        self.uvm.sgn()
        self.assertEqual(self.uvm.accumulator, -1)

        self.uvm.accumulator = 0
        self.uvm.sgn()
        self.assertEqual(self.uvm.accumulator, 0)

    def test_execute_instruction(self):
        self.uvm.execute_instruction(LOAD_CONST, 10)
        self.assertEqual(self.uvm.accumulator, 10)

        self.uvm.memory[5] = UVM.to_unsigned(-5)
        self.uvm.execute_instruction(LOAD_MEM, 5)
        self.assertEqual(self.uvm.accumulator, -5)

        self.uvm.execute_instruction(STORE_MEM, 10)
        self.assertEqual(UVM.to_signed(self.uvm.memory[10]), -5)

        self.uvm.accumulator = 2
        self.uvm.execute_instruction(SGN, 0)
        self.assertEqual(self.uvm.accumulator, 1)

        with self.assertRaises(ValueError):
            self.uvm.execute_instruction(99, 0)

    def test_write_result_file(self):
        result_file = "test_result.xml"
        memory_range = (0, 2)

        self.uvm.memory[0] = UVM.to_unsigned(10)
        self.uvm.memory[1] = UVM.to_unsigned(-5)
        self.uvm.memory[2] = UVM.to_unsigned(0)

        self.uvm.write_result_file(result_file, *memory_range)
        self.assertTrue(os.path.exists(result_file))

        with open(result_file, "r") as f:
            content = f.read()
        self.assertIn('<cell address="0">10</cell>', content)
        self.assertIn('<cell address="1">-5</cell>', content)
        self.assertIn('<cell address="2">0</cell>', content)

        os.remove(result_file)


if __name__ == "__main__":
    unittest.main()
