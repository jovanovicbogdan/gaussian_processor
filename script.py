import argparse

from default_config import DefaultConfig
from file_converter import all_files_directory_out_to_xyz, all_files_directory_com_to_xyz
from to_com import xyz_to_com


def setup_parser():
    parser = argparse.ArgumentParser(prog="Gaussian processor", description="Parse Gaussian input/output files")

    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument("--from-gaussian-out", type=str, help="Path to Gaussian output file(s) directory")
    input_group.add_argument("--from-xyz", type=str, help="Path to XYZ file(s) directory")
    input_group.add_argument("--from-gaussian-in", type=str, help="Path to Gaussian input file(s) directory")

    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument("--to-spe", action="store_true")
    output_group.add_argument("--to-opt", action="store_true")
    output_group.add_argument("--to-xyz", action="store_true")

    parser.add_argument("--config", type=str, help="Choose pre-defined configuration from 1-6")
    parser.add_argument("--list-config", action="store_true")

    # TODO: add argument for 'mem_alloc' and 'nproc'. Currently, hard-coded to mem_alloc=16, nproc=10.
    # TODO: add argument/config for defining your own methods

    return parser


def xyz_to_com_spe(folder_path, theory, dispersion, solvent, basis_set, split_basis_set, mem_alloc, nproc,
                   basis_set_heavy_atoms, ecp_heavy_atoms):
    xyz_to_com(folder_path, theory, dispersion, solvent, basis_set, "spe", split_basis_set, mem_alloc, nproc,
               basis_set_heavy_atoms, ecp_heavy_atoms)


def xyz_to_com_opt(folder_path, theory, dispersion, solvent, basis_set, split_basis_set, mem_alloc, nproc,
                   basis_set_heavy_atoms, ecp_heavy_atoms):
    xyz_to_com(folder_path, theory, dispersion, solvent, basis_set, "reopt", split_basis_set, mem_alloc, nproc,
               basis_set_heavy_atoms, ecp_heavy_atoms)


def convert_gaussian_output_files_to_input_files_for_spe_calculation(data_dir, config):
    print("Convert Gaussian output files to input files for SPE calculation with config: ", config)
    all_files_directory_out_to_xyz(data_dir)
    xyz_to_com_spe(data_dir, config["level_of_theory"], config["empirical_dispersion"], config["solvent"],
                   config["basis_set"], config["split_basis_set"], 16, 10, config["basis_set_heavy_atoms"],
                   config["ecp_heavy_atoms"])


def convert_gaussian_output_files_to_input_files_for_optimization(data_dir, config):
    print("Convert Gaussian output files to input files for optimization with configuration: ", config)
    all_files_directory_out_to_xyz(data_dir)
    xyz_to_com_opt(data_dir, config["level_of_theory"], config["empirical_dispersion"], config["solvent"],
                   config["basis_set"], config["split_basis_set"], 16, 10, config["basis_set_heavy_atoms"],
                   config["ecp_heavy_atoms"])


def convert_xyz_files_to_input_files_for_spe_calculation(data_dir, config):
    print("Convert .xyz files to input files for SPE calculation with configuration: ", config)
    xyz_to_com_spe(data_dir, config["level_of_theory"], config["empirical_dispersion"], config["solvent"],
                   config["basis_set"], config["split_basis_set"], 16, 10, config["basis_set_heavy_atoms"],
                   config["ecp_heavy_atoms"])


def convert_xyz_files_to_input_files_for_optimization(data_dir, config):
    print("Convert .xyz files to input files for optimization with configuration: ", config)
    xyz_to_com_opt(data_dir, config["level_of_theory"], config["empirical_dispersion"], config["solvent"],
                   config["basis_set"], config["split_basis_set"], 16, 10, config["basis_set_heavy_atoms"],
                   config["ecp_heavy_atoms"])


def convert_gaussian_input_files_to_xyz_files(data_dir):
    print("Convert Gaussian input files to .xyz files")
    all_files_directory_com_to_xyz(data_dir)


def convert_gaussian_output_files_to_xyz_files(data_dir):
    print("Convert Gaussian output files to .xyz files")
    all_files_directory_out_to_xyz(data_dir)


def run():
    parser = setup_parser()
    args = parser.parse_args()

    # gaussian output -> [spe, opt, xyz]
    # xyz             -> [spe, opt]
    # gaussian input  -> [xyz]

    if args.from_gaussian_out and args.to_spe and args.config:
        config = DefaultConfig.SPE_DEFAULTS[args.config]
        convert_gaussian_output_files_to_input_files_for_spe_calculation(args.from_gaussian_out, config)
    elif args.from_gaussian_out and args.to_opt and args.config:
        config = DefaultConfig.SPE_DEFAULTS[args.config]
        convert_gaussian_output_files_to_input_files_for_optimization(args.from_gaussian_out, config)
    elif args.from_xyz and args.to_spe and args.config:
        config = DefaultConfig.SPE_DEFAULTS[args.config]
        convert_xyz_files_to_input_files_for_spe_calculation(args.from_xyz, config)
    elif args.from_xyz and args.to_opt and args.config:
        config = DefaultConfig.SPE_DEFAULTS[args.config]
        convert_xyz_files_to_input_files_for_optimization(args.from_xyz, config)
    elif args.from_gaussian_in and args.to_xyz:
        convert_gaussian_input_files_to_xyz_files(args.from_gaussian_in)
    elif args.from_gaussian_out and args.to_xyz:
        convert_gaussian_output_files_to_xyz_files(args.from_gaussian_out)
    elif args.list_config:
        print(f"Available configurations:\n{DefaultConfig()}")
    else:
        parser.print_help()
        exit(1)


if __name__ == "__main__":
    run()
