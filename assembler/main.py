import argparse


def parse_args() -> argparse.Namespace:
    """Parses command line arguments."""
    parser = argparse.ArgumentParser(description="Assembler and Interpreter for UVM")

    parser.add_argument(
        "mode",
        choices=["assemble", "interpret"],
        help="Operation mode: 'assemble' or 'interpret'",
    )
    parser.add_argument("input_file", help="Input file")
    parser.add_argument("output_file", help="Output file")
    parser.add_argument("log_file", help="Log file in XML format")
    parser.add_argument(
        "--result_file", help="Result file for interpreter (XML format)"
    )
    parser.add_argument(
        "--memory_start", help="Start of memory range for the interpreter", type=int
    )
    parser.add_argument(
        "--memory_start", help="End of memory range for the interpreter", type=int
    )

    return parser.parse_args()


def main() -> None: ...


if __name__ == "__main__":
    main()
