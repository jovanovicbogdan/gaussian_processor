class DefaultConfig:
    SPE_DEFAULTS = {
        "1": {
            "name": "uM06-GD3/6-311++G(d,p)-SDD(Ni)/SMD(PhMe)",
            "split_basis_set": True,
            "level_of_theory": "um06",
            "empirical_dispersion": "gd3",
            "solvent": "toluene",
            "basis_set_heavy_atoms": "SDD",
            "ecp_heavy_atoms": "SDD",
            "basis_set": "6-311++G(d,p)"
        },
        "2": {
            "name": "uM06-GD3/def2TZVP/SMD(PhMe)",
            "split_basis_set": False,
            "level_of_theory": "uM06",
            "empirical_dispersion": "gd3",
            "solvent": "toluene",
            "basis_set": "def2TZVP"
        },
        "3": {
            "name": "uM06-GD3/def2TZVPP/SMD(PhMe)",
            "split_basis_set": False,
            "level_of_theory": "uM06",
            "empirical_dispersion": "gd3",
            "solvent": "toluene",
            "basis_set": "def2TZVPP"
        },
        "4": {
            "name": "uB3LYP-GD3BJ/6-311++G(d,p)-SDD(Ni)/SMD(DCE)",
            "split_basis_set": True,
            "level_of_theory": "uB3LYP",
            "empirical_dispersion": "gd3bj",
            "solvent": "dichloroethane",
            "basis_set_heavy_atoms": "SDD",
            "ecp_heavy_atoms": "SDD",
            "basis_set": "6-311++G(d,p)"
        },
        "5": {
            "name": "WB97XD/def2TZVPP/SMD(PhMe)",
            "split_basis_set": False,
            "level_of_theory": "WB97XD",
            "empirical_dispersion": "",
            "solvent": "toluene",
            "basis_set": "def2TZVPP"
        },
        "6": {
            "name": "WB97XD/6-311++G(d,p)-SDD(Ni)/SMD(PhMe)",
            "split_basis_set": True,
            "level_of_theory": "WB97XD",
            "empirical_dispersion": "",
            "solvent": "toluene",
            "basis_set_heavy_atoms": "SDD",
            "ecp_heavy_atoms": "SDD",
            "basis_set": "6-311++G(d,p)"
        }
    }

    OPT_DEFAULTS = {
        "1": {
            "name": "B3LYP-D3BJ/6-31G(d,p)-LANL2DZ(heavy metals)/gas",
            "split_basis_set": True,
            "level_of_theory": "uB3LYP",
            "empirical_dispersion": "gd3bj",
            "solvent": None,
            "basis_set_heavy_atoms": "LANL2DZ",
            "ecp_heavy_atoms": "LANL2",
            "basis_set": "6-31G(d,p)"
        },
        "2": {
            "name": "B3LYP-D3BJ/6-31+G(d,p)-LANL2DZ(heavy metals)/gas",
            "split_basis_set": True,
            "level_of_theory": "uB3LYP",
            "empirical_dispersion": "gd3bj",
            "solvent": None,
            "basis_set_heavy_atoms": "LANL2DZ",
            "ecp_heavy_atoms": "LANL2",
            "basis_set": "6-31+G(d,p)"
        },
        "3": {
            "name": "B3LYP-D3BJ/def2svp/gas",
            "split_basis_set": False,
            "level_of_theory": "uB3LYP",
            "empirical_dispersion": "gd3bj",
            "solvent": None,
            "basis_set": "def2svp"
        },
        "4": {
            "name": "B3LYP-D3BJ/def2tzvp/gas",
            "split_basis_set": False,
            "level_of_theory": "uB3LYP",
            "empirical_dispersion": "gd3bj",
            "solvent": None,
            "basis_set": "def2tzvp"
        },
        "5": {
            "name": "M06-D3/6-31G(d,p)-LANL2DZ(heavy metals)/gas",
            "split_basis_set": True,
            "level_of_theory": "uM06",
            "empirical_dispersion": "gd3",
            "solvent": None,
            "basis_set_heavy_atoms": "LANL2DZ",
            "ecp_heavy_atoms": "LANL2",
            "basis_set": "6-31G(d,p)"
        },
        "6": {
            "name": "M06-D3/def2svp/gas",
            "split_basis_set": False,
            "level_of_theory": "uM06",
            "empirical_dispersion": "gd3",
            "solvent": None,
            "basis_set": "def2svp"
        }
    }

    def __str__(self):
        output = ["SPE", "-" * 40]
        for key, config in self.SPE_DEFAULTS.items():
            output.append(f"{key}. {config['name']}")
        output.append("\nOPT")
        output.append("-" * 40)
        for key, config in self.OPT_DEFAULTS.items():
            output.append(f"{key}. {config['name']}")

        return "\n".join(output)
