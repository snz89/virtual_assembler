import argparse

from assembler.assembler import Assembler
from assembler.uvm import UVM


def main():
    parser = argparse.ArgumentParser(description="Assembler and Interpreter for UVM")
    subparsers = parser.add_subparsers(dest="mode", help="Operation mode")

    # Assembler parser
    assembler_parser = subparsers.add_parser("assemble", help="Assemble UVM code")
    assembler_parser.add_argument(
        "input_file", help="Path to the input file with UVM assembly code"
    )
    assembler_parser.add_argument("binary_file", help="Path to the output binary file")
    assembler_parser.add_argument("log_file", help="Path to the output log file (XML)")

    # Interpreter parser
    interpreter_parser = subparsers.add_parser(
        "interpret", help="Interpret UVM binary code"
    )
    interpreter_parser.add_argument("binary_file", help="Path to the input binary file")
    interpreter_parser.add_argument(
        "result_file", help="Path to the output result file (XML)"
    )
    interpreter_parser.add_argument(
        "start_address", type=int, help="Start address of memory range to save"
    )
    interpreter_parser.add_argument(
        "end_address", type=int, help="End address of memory range to save"
    )

    args = parser.parse_args()

    if args.mode == "assemble":
        assembler = Assembler()
        assembler.assemble(args.input_file, args.binary_file, args.log_file)
        print(
            f"Assembly completed. Binary saved to {args.binary_file}, log saved to {args.log_file}"
        )
    elif args.mode == "interpret":
        uvm = UVM()
        uvm.execute(
            args.binary_file, args.result_file, (args.start_address, args.end_address)
        )
        print(f"Interpretation completed. Result saved to {args.result_file}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
