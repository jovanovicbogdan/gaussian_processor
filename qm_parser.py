import os
import re

periodic_table = {
    1: "H", 2: "He", 3: "Li", 4: "Be", 5: "B", 6: "C", 7: "N", 8: "O", 9: "F", 10: "Ne",
    11: "Na", 12: "Mg", 13: "Al", 14: "Si", 15: "P", 16: "S", 17: "Cl", 18: "Ar", 19: "K", 20: "Ca",
    21: "Sc", 22: "Ti", 23: "V", 24: "Cr", 25: "Mn", 26: "Fe", 27: "Co", 28: "Ni", 29: "Cu", 30: "Zn",
    31: "Ga", 32: "Ge", 33: "As", 34: "Se", 35: "Br", 36: "Kr", 37: "Rb", 38: "Sr", 39: "Y", 40: "Zr",
    41: "Nb", 42: "Mo", 43: "Tc", 44: "Ru", 45: "Rh", 46: "Pd", 47: "Ag", 48: "Cd", 49: "In", 50: "Sn",
    51: "Sb", 52: "Te", 53: "I", 54: "Xe", 55: "Cs", 56: "Ba", 57: "La", 58: "Ce", 59: "Pr", 60: "Nd",
    61: "Pm", 62: "Sm", 63: "Eu", 64: "Gd", 65: "Tb", 66: "Dy", 67: "Ho", 68: "Er", 69: "Tm", 70: "Yb",
    71: "Lu", 72: "Hf", 73: "Ta", 74: "W", 75: "Re", 76: "Os", 77: "Ir", 78: "Pt", 79: "Au", 80: "Hg",
    81: "Tl", 82: "Pb", 83: "Bi", 84: "Po", 85: "At", 86: "Rn", 87: "Fr", 88: "Ra", 89: "Ac", 90: "Th",
    91: "Pa", 92: "U", 93: "Np", 94: "Pu", 95: "Am", 96: "Cm", 97: "Bk", 98: "Cf", 99: "Es", 100: "Fm",
    101: "Md", 102: "No", 103: "Lr", 104: "Rf", 105: "Db", 106: "Sg", 107: "Bh", 108: "Hs", 109: "Mt", 110: "Ds",
    111: "Rg", 112: "Cn", 113: "Nh", 114: "Fl", 115: "Mc", 116: "Lv", 117: "Ts", 118: "Og"
}

heavy_metals = [
    "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",  # Sc to Zn
    "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe",
    # Metals after Rb
    "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu",
    "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn",
    "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr",
    "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"
]


def convert_element_number_to_symbol(atomic_number):
    return periodic_table.get(atomic_number, 'X')  # Default to 'X' if element is not found


def parse_gaussian_output(file_path):
    """
    Parses G16 output file and extracts atom coordinates.
    :param file_path (str): Path to the output file
    :return: List of tuples containing element symbol and its xyz coordinates.
    """

    coordinates = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

        # Find the start of the final geometry section. Each time it finds a line with "Standard orientation:", it updates the variable start to the current line index.
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
                element_symbol = convert_element_number_to_symbol(element_number)
                x, y, z = parts[3:6]
                coordinates.append((element_symbol, x, y, z))

    return coordinates


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


def write_xyz_file(coordinates, output_path):
    """
    Creates an .xyz file and writes coordinates
    :param coordinates: "List of tuples containing element symbol and its xyz coordinates."
    :param output_path: "Path to the output XYZ file."
    """
    with open(output_path, 'w') as file:
        file.write(f"{len(coordinates)}\n")
        base_name_full = f"{output_path.split()}"  # gives something like 'C:\Users\stojil0000\PycharmProjects\parse_gaussian\oxar_p_1.xyz'
        base_name_with_extension = base_name_full.split("\\")[-1]  # gives oxar_p_1.xyz
        base_name_without_extension = base_name_with_extension.split(".", 1)[0]  # gives oxar_p_1
        file.write(f"{base_name_without_extension}_optimized\n")
        for coord in coordinates:
            file.write(f"{coord[0]} {coord[1]} {coord[2]} {coord[3]}\n")


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


# HERE ends out to xyz part
# HERE starts the xyz to com part

def sort_elements_for_genecp(elements):
    """
    Sorts elements so that first is always C, then H and then the rest of elements in the order of the periodic table.
    :param elements: List of elements to sort
    :return:
    """
    atomic_numbers = {symbol: num for num, symbol in
                      periodic_table.items()}  # Create a reverse lookup to get atomic numbers for symbols

    def sort_key(element):
        if element == "C":
            return (0,)
        elif element == "H":
            return (1,)
        else:
            return (2, atomic_numbers.get(element,
                                          str('X')))  # Return a tuple where second item is the atomic number or X if not found

    return sorted(elements, key=sort_key)


def process_elements(content):
    """
    Extracts unique elements from the content of an .xyz file and separates them into heavy metals and non-heavy metals.
    """
    elements = set()  # initialize an empty set
    for line in content:
        element = line.split()[0]  # extract the element from the line
        elements.add(element)  # add the element to the set

    # Separate elements into heavy metals and non-heavy metals
    heavy_metals_in_molecule = [el for el in elements if el in heavy_metals]
    non_heavy_metals_in_molecule = [el for el in elements if el not in heavy_metals]

    # Sort the elements for GenECP
    heavy_metals_sorted = sort_elements_for_genecp(heavy_metals_in_molecule)
    non_heavy_metals_sorted = sort_elements_for_genecp(non_heavy_metals_in_molecule)

    return heavy_metals_sorted, non_heavy_metals_sorted


def write_com_file(file, theory, dispersion, solvent, basis_set, com_file_name, content, heavy_metals_in_molecule,
                   non_heavy_metals_in_molecule, calculation_type):
    if calculation_type == "reopt":
        if "ts" in com_file_name:
            job = " opt=(ts,calcfc,noeigentest) freq=noraman"
        else:
            job = " opt freq=noraman"
    elif calculation_type == "spe":
        job = "p"
    else:
        raise ValueError("Invalid calculation type.")

    if split_basis_set and heavy_metals_in_molecule:
        input_line_basis = "genecp"
    else:
        input_line_basis = basis_set

    file.write((f"%mem={mem_alloc}GB" if nproc else "%mem=16GB")
               + "\n"
               + (f"%nprocshared={nproc}" if nproc else "%nprocshared=16")
               + "\n"
                 f"%chk={com_file_name.replace('.com', '')}.chk\n"
                 f"#{job} {theory}/{input_line_basis}"
               + (f" scrf=(smd,solvent={solvent})" if solvent else "")
               + (f" em={dispersion}" if dispersion else "")
               + " gfinput\n\n"
                 f"{com_file_name.replace('.com', '')}\n\n"
                 f"0 1\n")
    file.writelines(content)
    file.write("\n")

    if split_basis_set and heavy_metals_in_molecule:
        file.write(f"{' '.join(heavy_metals_in_molecule)} 0\n"
                   f"{basis_set_heavy_atoms}\n"
                   "****\n"
                   f"{' '.join(non_heavy_metals_in_molecule)} 0\n"
                   f"{basis_set}\n"
                   "****\n\n"
                   f"{' '.join(heavy_metals_in_molecule)} 0\n"
                   + (f"{ecp_heavy_atoms}\n\n\n\n\n"))


def xyz_to_com(folder_path, theory, dispersion, solvent, basis_set, calculation_type):
    """
    Processes all .xyz files in the specified folder, creating a new .com file for each of them.
    The new file will be a Gaussian input file for either optimization or SPE calculation.

    :param folder_path: Path to the folder containing the .xyz files
    :param theory: Level of theory specified by the user
    :param dispersion: Empirical dispersion specified by the user
    :param solvent: Implicit SMD solvent specified by the user
    :param basis_set: Basis set for light atoms specified by the user
    :param calculation_type: Either 'opt' for optimization or 'spe' for single point energy
    """
    # Get a list of all .xyz files in the specified folder
    xyz_files = [f for f in os.listdir(folder_path) if f.endswith(".xyz")]

    for xyz_file in xyz_files:
        # Construct the full file path
        xyz_file_path = os.path.join(folder_path, xyz_file)

        # Read the content of the .xyz file, skipping the first two lines
        with open(xyz_file_path, "r") as file:
            lines = file.readlines()
            content = lines[2:]  # Skip the first two lines

        # Extract elements contained in the xyz file
        heavy_metals_in_molecule, non_heavy_metals_in_molecule = process_elements(content)

        # Create the new file name with .com extension
        clean_basis_set = re.sub(r"[(),]", "", basis_set)  # Removes ( ) and ,
        clean_basis_set = clean_basis_set.replace("+", "plus")  # Converts + to plus and makes it lower case
        com_file_name = xyz_file.replace(".xyz", f"_{theory}_{clean_basis_set}_{calculation_type}.com").lower()
        com_file_path = os.path.join(folder_path, com_file_name)

        # Write the content to the com file
        with open(com_file_path, "w") as file:
            write_com_file(file, theory, dispersion, solvent, basis_set, com_file_name, content,
                           heavy_metals_in_molecule, non_heavy_metals_in_molecule, calculation_type)

        print(f"Processed {xyz_file} -> {com_file_name}")


# Wrapper functions for SPE and optimization
def xyz_to_com_spe(folder_path, theory, dispersion, solvent, basis_set):
    xyz_to_com(folder_path, theory, dispersion, solvent, basis_set, calculation_type="spe")


def xyz_to_com_opt(folder_path, theory, dispersion, solvent, basis_set):
    xyz_to_com(folder_path, theory, dispersion, solvent, basis_set, calculation_type="reopt")


def remove_xyz_files(directory):
    """
    Removes all .xyz files from the specified directory.
    """
    for filename in os.listdir(directory):
        if filename.endswith(".xyz"):
            file_path = os.path.join(directory, filename)
            os.remove(file_path)
            print(f"Deleted {file_path}")


if __name__ == "__main__":
    # Get user input for Gaussian parameters
    print(
        "This is a software that converts Gaussian output files (.out) or xyz files to Gaussian input files (.com) for SPE calculation, or reoptimization.\n"
        "It also converts Gaussian input and output files to .xyz files.\n"
        "The software comes with some default, commonly used options. You can also define your own method.\n"
        "The script takes care of the split basis set input, as well as the input if there are no heavy elements.\n"
        "However, the current version of the script cannot handle charged species, or species with non-singlet multiplicity.\n"
        "In the end, the script will ask you whether you want to remove the xyz files that the script created. It is not neccessary to keep them, but always good to ask.\n"
        "Please follow the instructions below to proceed.\n")

    task = input(
        "Please choose what you wish to do from the options below: \n"
        "   1. Convert Gaussian output files to input files for SPE calculation \n"
        "   2. Convert Gaussian output files to input files for optimization \n"
        "   3. Convert .xyz files to input files for SPE calculation \n"
        "   4. Convert .xyz files to input files for optimization \n"
        "   5. Convert Gaussian input files to .xyz files \n"
        "   6. Convert Gaussian output files to .xyz files \n"
        "Please choose what you want to do: ").strip().lower()

    if task != "5" and task != "6":
        nproc = input("Enter the number of processors to use (16 by default): ").strip()
        mem_alloc = input("Enter the amount of RAM memory you with to reserve in total (16 GB by default): ").strip()

    if task == "1" or task == "3":
        default_options_spe = input(
            "Do you want to use some of the default options?: \n "
            "   0) I wish to define my own method \n "
            "   1) uM06-GD3/6-311++G(d,p)-SDD(heavy metals)/SMD(PhMe)\n "
            "   2) uM06-GD3/def2TZVP/SMD(PhMe)\n "
            "   3) uM06-GD3/def2TZVPP/SMD(PhMe)\n "
            "   4) uB3LYP-GD3BJ/6-311++G(d,p)-SDD(heavy metals)/SMD(DCE)\n "
            "   5) wB97X-D/def2TZVPP/SMD(PhMe)\n "
            "   6) wB97X-D/6-311++G(d,p)-SDD(heavy metals)/SMD(PhMe)\n "
            "Please choose what you wish to do: ").strip().lower()

        if default_options_spe == "1":  # uM06-GD3/6-311++G(d,p)-SDD(Ni)/SMD(PhMe)
            split_basis_set = True
            level_of_theory = "um06"
            empirical_dispersion = "gd3"
            solvent = "toluene"
            basis_set_heavy_atoms = "SDD"
            ecp_heavy_atoms = "SDD"
            basis_set = "6-311++G(d,p)"
        elif default_options_spe == "2":  # uM06-GD3/def2TZVP/SMD(PhMe)
            split_basis_set = False
            level_of_theory = "uM06"
            empirical_dispersion = "gd3"
            solvent = "toluene"
            basis_set = "def2TZVP"
        elif default_options_spe == "3":  # uM06-GD3/def2TZVPP/SMD(PhMe)
            split_basis_set = False
            level_of_theory = "uM06"
            empirical_dispersion = "gd3"
            solvent = "toluene"
            basis_set = "def2TZVPP"
        elif default_options_spe == "4":  # uB3LYP-GD3BJ/6-311++G(d,p)-SDD(Ni)/SMD(DCE)
            split_basis_set = True
            level_of_theory = "uB3LYP"
            empirical_dispersion = "gd3bj"
            solvent = "dichloroethane"
            basis_set_heavy_atoms = "SDD"
            ecp_heavy_atoms = "SDD"
            basis_set = "6-311++G(d,p)"
        elif default_options_spe == "5":  # WB97XD/def2TZVPP/SMD(PhMe)
            split_basis_set = False
            level_of_theory = "WB97XD"
            basis_set = "def2TZVPP"
            empirical_dispersion = ""
            solvent = "toluene"
        elif default_options_spe == "6":  # WB97XD/6-311++G(d,p)-SDD(Ni)/SMD(PhMe)
            split_basis_set = True
            level_of_theory = "WB97XD"
            empirical_dispersion = ""
            solvent = "toluene"
            basis_set_heavy_atoms = "SDD"
            ecp_heavy_atoms = "SDD"
            basis_set = "6-311++G(d,p)"

        elif default_options_spe == "0":
            split_basis_set = True if input(
                "Do you want to use different basis sets on different atoms? (y/n): ").strip().lower() == 'y' else False
            if split_basis_set:
                level_of_theory = input("Choose the level of theory (e.g., um06,b3lyp,wb97xd): ").strip()
                empirical_dispersion = input(
                    "Choose the empirical dispersion (leave blank for default) (e.g., gd3 or gd3bj): ").strip()
                solvent = input("Choose the implicit SMD solvent (e.g., toluene): ").strip()
                basis_set_heavy_atoms = input("Choose the basis set for heavy atoms (e.g., LANL2DZ or SDD): ").strip()
                ecp_heavy_atoms = input("Enter the ECP card for heavy atoms (e.g., SDD or LANL2): ").strip()
                basis_set = input("Choose the basis set for light atoms (e.g., 6-311++G(d,p)): ").strip()
            else:
                level_of_theory = input("Choose the level of theory (e.g., um06,b3lyp,wb97xd): ").strip()
                basis_set = input("Choose the basis set (e.g., def2-TZVP): ").strip()
                empirical_dispersion = input(
                    "Choose the empirical dispersion (leave blank for default) (e.g., gd3 or gd3bj): ").strip()
                solvent = input("Choose the implicit SMD solvent (e.g., toluene): ").strip()
        else:  # Invalid option
            print("Invalid option. Please try again...")

    elif task == "2" or task == "4":
        default_options_opt = input(
            "Do you want to use some of the default options?: \n "
            "   0) I wish to define my own method \n "
            "   1) B3LYP-D3BJ/6-31G(d,p)-LANL2DZ(heavy metals)/gas\n "
            "   2) B3LYP-D3BJ/6-31+G(d,p)-LANL2DZ(heavy metals)/gas\n "
            "   3) B3LYP-D3BJ/def2svp/gas\n "
            "   4) B3LYP-D3BJ/def2tzvp/gas\n "
            "   5) M06-D3/6-31G(d,p)-LANL2DZ(heavy metals)/gas\n "
            "   6) M06-D3/def2svp/gas\n "
            "Please choose what you wish to do: ").strip().lower()

        if default_options_opt == "1":  # B3LYP-D3BJ/6-31G(d,p)-LANL2DZ(heavy metals)/gas
            split_basis_set = True
            level_of_theory = "uB3LYP"
            empirical_dispersion = "gd3bj"
            solvent = None
            basis_set_heavy_atoms = "LANL2DZ"
            ecp_heavy_atoms = "LANL2"
            basis_set = "6-31G(d,p)"
        elif default_options_opt == "2":  # B3LYP-D3BJ/6-31+G(d,p)-LANL2DZ(heavy metals)/gas
            split_basis_set = True
            level_of_theory = "uB3LYP"
            empirical_dispersion = "gd3bj"
            solvent = None
            basis_set_heavy_atoms = "LANL2DZ"
            ecp_heavy_atoms = "LANL2"
            basis_set = "6-31+G(d,p)"
        elif default_options_opt == "3":  # B3LYP-D3BJ/def2svp/gas
            split_basis_set = False
            level_of_theory = "uB3LYP"
            empirical_dispersion = "gd3bj"
            solvent = None
            basis_set = "def2svp"
        elif default_options_opt == "4":  # B3LYP-D3BJ/def2tzvp/gas
            split_basis_set = False
            level_of_theory = "uB3LYP"
            empirical_dispersion = "gd3bj"
            solvent = None
            basis_set = "def2tzvp"
        elif default_options_opt == "5":  # M06-D3/6-31G(d,p)-LANL2DZ(heavy metals)/gas
            split_basis_set = True
            level_of_theory = "uM06"
            empirical_dispersion = "gd3"
            solvent = None
            basis_set_heavy_atoms = "LANL2DZ"
            ecp_heavy_atoms = "LANL2"
            basis_set = "6-31G(d,p)"
        elif default_options_opt == "6":  # M06-D3/def2svp/gas
            split_basis_set = False
            level_of_theory = "uM06"
            empirical_dispersion = "gd3"
            solvent = None
            basis_set = "def2svp"
        elif default_options_opt == "0":
            split_basis_set = True if input(
                "Do you want to use different basis sets on different atoms? (y/n): ").strip().lower() == 'y' else False
            if split_basis_set:
                level_of_theory = input("Choose the level of theory (e.g., um06,b3lyp,wb97xd): ").strip()
                empirical_dispersion = input(
                    "Choose the empirical dispersion (leave blank for default) (e.g., gd3 or gd3bj): ").strip()
                solvent = input("Choose the implicit SMD solvent (e.g., toluene): ").strip()
                basis_set_heavy_atoms = input("Choose the basis set for heavy atoms (e.g., LANL2DZ or SDD): ").strip()
                ecp_heavy_atoms = input("Enter the ECP card for heavy atoms (e.g., SDD or LANL2): ").strip()
                basis_set = input("Choose the basis set for light atoms (e.g., 6-311++G(d,p)): ").strip()
            else:
                level_of_theory = input("Choose the level of theory (e.g., um06,b3lyp,wb97xd): ").strip()
                basis_set = input("Choose the basis set (e.g., def2-TZVP): ").strip()
                empirical_dispersion = input(
                    "Choose the empirical dispersion (leave blank for default) (e.g., gd3 or gd3bj): ").strip()
                solvent = input("Choose the implicit SMD solvent (e.g., toluene): ").strip()
        else:
            print("Invalid option. Please try again...")
            exit(1)

    current_directory = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the script

    if task == "1" or task == "2":
        all_files_directory_out_to_xyz(current_directory)  # out_to_xyz_command

        if task == "1":
            xyz_to_com_spe(current_directory, level_of_theory, empirical_dispersion, solvent, basis_set)
        elif task == "2":
            xyz_to_com_opt(current_directory, level_of_theory, empirical_dispersion, solvent, basis_set)

        keep_xyz = input("Do you want to keep the .xyz files? (y/n): ").strip().lower()
        if keep_xyz != 'y':
            remove_xyz_files(current_directory)


    elif task == "3":
        xyz_to_com_spe(current_directory, level_of_theory, empirical_dispersion, solvent, basis_set)
    elif task == "4":
        xyz_to_com_opt(current_directory, level_of_theory, empirical_dispersion, solvent, basis_set)
    elif task == "5":
        all_files_directory_com_to_xyz(current_directory)
    elif task == "6":
        all_files_directory_out_to_xyz(current_directory)
    else:
        print("Invalid option. Please try again...")

    print("All done! Have a great day!")
