import os


def write_xyz_file(coordinates, output_path):
    """
    Creates an .xyz file and writes coordinates
    :param coordinates: "List of tuples containing element symbol and its xyz coordinates."
    :param output_path: "Path to the output XYZ file."
    """
    with open(output_path, 'w') as file:
        file.write(f"{len(coordinates)}\n")
        # Get the base name without extension
        base_name = os.path.splitext(os.path.basename(output_path))[0]
        file.write(f"{base_name}_optimized\n")
        for coord in coordinates:
            file.write(f"{coord[0]} {coord[1]} {coord[2]} {coord[3]}\n")


def write_com_file(file, theory, dispersion, solvent, basis_set, com_file_name, content, heavy_metals_in_molecule,
                   non_heavy_metals_in_molecule, calculation_type, split_basis_set, mem_alloc, nproc,
                   basis_set_heavy_atoms, ecp_heavy_atoms):
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
                   + f"{ecp_heavy_atoms}\n\n\n\n\n")
