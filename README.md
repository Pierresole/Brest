# RAT Project

This project focuses on parsing nuclear data and reconstructing differential cross-sections. It began as a self-educational endeavor to experiment with resonances.
1 fitted resonance parameter = 1 distribution

*play = Fit from experiments. Reconstruct cross-sections, analyze sensitivity to resonance parameters, propagate uncertainty.


## Project Structure

- `parser/`: Contains the parsing modules for reading MF3 and MF4 data.
- `recon/`: Contains the C++ code and Pybind11 setup for efficient reconstruction.
- `rmatrix/`: Contains the C++ code and Pybind11 setup for R-Matrix parametrization.
- `notebooks/`: Jupyter notebooks for testing and exploring functionalities.
- `data/`: Example data files for testing and development.
- `tests/`: Unit tests for parser and reconstruction modules.

## Resonance Analysis Tool

### Build Pybind11 Extension

Navigate to the `recon` directory and build the extension:

```sh
cd reconstruction
python setup.py build_ext --inplace
