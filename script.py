import argparse


# "   1. Convert Gaussian output files to input files for SPE calculation \n"
# "   2. Convert Gaussian output files to input files for optimization \n"
# "   3. Convert .xyz files to input files for SPE calculation \n"
# "   4. Convert .xyz files to input files for optimization \n"
# "   5. Convert Gaussian input files to .xyz files \n"
# "   6. Convert Gaussian output files to .xyz files \n"

def setup_parser():
    parser = argparse.ArgumentParser(prog="Gaussian processor", description="Example script with named arguments")

    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--from-gaussian-out", type=str, help="Path to Gaussian output file")
    input_group.add_argument("--from-xyz", type=str, help="Path to XYZ file")
    input_group.add_argument("--from-gaussian-in", type=str, help="Path to Gaussian input file")

    output_group = parser.add_mutually_exclusive_group(required=True)
    output_group.add_argument("--to-spe", action="store_true", help="Convert to single point energy input")
    output_group.add_argument("--to-opt", action="store_true", help="Convert to optimization input")
    output_group.add_argument("--to-xyz", action="store_true", help="Convert to XYZ format")

    return parser


def run():
    parser = setup_parser()
    args = parser.parse_args()

    # gaussian output -> [spe, opt, xyz]
    # xyz             -> [spe, opt]
    # gaussian input  -> [xyz]

    if hasattr(args, "name"):
        print(args.name)


if __name__ == "__main__":
    run()
