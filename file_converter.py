import os

from gaussian_parser import parse_gaussian_output, parse_gaussian_input
from writer import write_xyz_file


def out_to_xyz(input_file, output_file):
    """
    Converts Gaussian output file to .xyz file.
    :param input_file: "Path to the Gaussian output file."
    :param output_file: "Path to the output .xyz file."
    """
    coordinates = parse_gaussian_output(input_file)
    write_xyz_file(coordinates, output_file)


def all_files_directory_out_to_xyz(directory):
    """
    Processes all Gaussian output files in the specified directory.
    :param directory: Path to the directory containing Gaussian output files.
    """
    for filename in os.listdir(directory):
        if filename.endswith('.out'):
            input_file = os.path.join(directory, filename)
            base_name = os.path.splitext(filename)[0]  # Get the file name without extension
            output_file = os.path.join(directory, f"{base_name}.xyz")
            try:
                out_to_xyz(input_file, output_file)
                print(f"Processed {filename} -> {output_file}")
            except ValueError as e:
                print(f"Error processing {filename}: {e}")


def com_to_xyz(input_file, output_file):
    """
    Converts Gaussian input file to .xyz file.
    :param input_file: "Path to the Gaussian input file."
    :param output_file: "Path to the output .xyz file."
    """
    coordinates = parse_gaussian_input(input_file)
    write_xyz_file(coordinates, output_file)


def all_files_directory_com_to_xyz(directory):
    """
    Processes all Gaussian input files in the specified directory.
    :param directory: Path to the directory containing Gaussian input files.
    """
    for filename in os.listdir(directory):
        if filename.endswith('.com'):
            input_file = os.path.join(directory, filename)
            base_name = os.path.splitext(filename)[0]  # Get the file name without extension
            output_file = os.path.join(directory, f"{base_name}.xyz")
            try:
                com_to_xyz(input_file, output_file)
                print(f"Processed {filename} -> {output_file}")
            except ValueError as e:
                print(f"Error processing {filename}: {e}")
