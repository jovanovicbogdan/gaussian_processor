import re

from periodic_data import PeriodicData


def parse_gaussian_input(file_path):
    coordinates = []
    with open(file_path, "r") as file:
        lines = file.readlines()

    start = None
    for i, line in enumerate(lines):
        if "0 1" in line:
            start = i + 1
            break

    if start is None:
        raise ValueError("Coordinates not found in the file")

    for line in lines[start:]:
        parts = line.split()
        if len(parts) < 4:
            break  # Stop when encountering a line that doesn't contain coordinate data
        coordinates.append((parts[0], parts[1], parts[2], parts[3]))

    return coordinates


def parse_gaussian_output(file_path):
    """
    Parses G16 output file and extracts atom coordinates.
    :param file_path: Path to the output file
    :return: List of tuples containing element symbol and its xyz coordinates.
    """

    coordinates = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

        # Find the start of the final geometry section. # Each time it finds a line
        # with "Standard orientation:", it updates the variable start to the current line index.
        start = None
        for i, line in enumerate(lines):
            if "Standard orientation:" in line:
                start = i

        if start is None:
            raise ValueError("Standard orientation section not found in the file")

        # Skip the header lines
        start += 5

        # Extract coordinates
        for line in lines[start:]:
            if re.match(r'^\s*-+\s*$', line):  # End of the coordinates section
                break
            parts = line.split()
            if len(parts) > 5 and parts[1].isdigit():
                element_number = int(parts[1])
                element_symbol = PeriodicData.convert_element_number_to_symbol(element_number)
                x, y, z = parts[3:6]
                coordinates.append((element_symbol, x, y, z))

    return coordinates
