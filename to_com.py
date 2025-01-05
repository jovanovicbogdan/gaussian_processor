import os
import re

from writer import write_com_file
from periodic_data import PeriodicData


def sort_elements_for_genecp(elements):
    """
    Sorts elements so that first is always C, then H and then the rest of elements in the order of the periodic table.
    :param elements: List of elements to sort
    :return:
    """
    atomic_numbers = {symbol: num for num, symbol in
                      PeriodicData.PERIODIC_TABLE.items()}  # Create a reverse lookup to get atomic numbers for symbols

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
    heavy_metals_in_molecule = [el for el in elements if el in PeriodicData.HEAVY_METALS]
    non_heavy_metals_in_molecule = [el for el in elements if el not in PeriodicData.HEAVY_METALS]

    # Sort the elements for GenECP
    heavy_metals_sorted = sort_elements_for_genecp(heavy_metals_in_molecule)
    non_heavy_metals_sorted = sort_elements_for_genecp(non_heavy_metals_in_molecule)

    return heavy_metals_sorted, non_heavy_metals_sorted


def xyz_to_com(folder_path, theory, dispersion, solvent, basis_set, calculation_type, split_basis_set, mem_alloc, nproc,
               basis_set_heavy_atoms, ecp_heavy_atoms):
    """
    Processes all .xyz files in the specified folder, creating a new .com file for each of them.
    The new file will be a Gaussian input file for either optimization or SPE calculation.

    :param folder_path: Path to the folder containing the .xyz files
    :param theory: Level of theory specified by the user
    :param dispersion: Empirical dispersion specified by the user
    :param solvent: Implicit SMD solvent specified by the user
    :param basis_set: Basis set for light atoms specified by the user
    :param calculation_type: Either 'opt' for optimization or 'spe' for single point energy
    :param ecp_heavy_atoms:
    :param basis_set_heavy_atoms:
    :param nproc:
    :param mem_alloc:
    :param split_basis_set:
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
                           heavy_metals_in_molecule, non_heavy_metals_in_molecule, calculation_type, split_basis_set,
                           mem_alloc, nproc, basis_set_heavy_atoms, ecp_heavy_atoms)

        print(f"Processed {xyz_file} -> {com_file_name}")
