# Gaussian Processor CLI

```shell
usage: Gaussian processor [-h] [--from-gaussian-out FROM_GAUSSIAN_OUT | --from-xyz FROM_XYZ | --from-gaussian-in FROM_GAUSSIAN_IN] [--to-spe | --to-opt | --to-xyz] [--config CONFIG] [--list-config]

Parse Gaussian input/output files

options:
  -h, --help            show this help message and exit
  --from-gaussian-out   FROM_GAUSSIAN_OUT
                        Path to Gaussian output file(s) directory
  --from-xyz FROM_XYZ   Path to XYZ file(s) directory
  --from-gaussian-in    FROM_GAUSSIAN_IN
                        Path to Gaussian input file(s) directory
  --to-spe
  --to-opt
  --to-xyz
  --config CONFIG       Choose pre-defined configuration from 1-6
  --list-config
```

## Example usage

```shell
python script.py --from-xyz path_to_xyz_files_dir --to-opt --config 1
```

## List available configurations

```shell
python script.py --list-config
```
