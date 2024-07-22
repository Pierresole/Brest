# Brest Project

This project is for parsing nuclear data and reconstructing differential cross-sections efficiently.

## Project Structure

- `parser/`: Contains the parsing modules for reading MF3 and MF4 data.
- `reconstruction/`: Contains the C++ code and Pybind11 setup for efficient reconstruction.
- `notebooks/`: Jupyter notebooks for testing and exploring functionalities.
- `data/`: Example data files for testing and development.
- `tests/`: Unit tests for parser and reconstruction modules.

## Setup

### Build Pybind11 Extension

Navigate to the `reconstruction` directory and build the extension:

```sh
cd reconstruction
python setup.py build_ext --inplace
