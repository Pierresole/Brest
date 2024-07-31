from setuptools import setup, Extension
import pybind11
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        "recon.sigma",
        ["recon/sigma.cpp"],
        include_dirs=["include", pybind11.get_include()],
        language="c++",
        extra_compile_args=["-std=c++14"],  # or C++17 if needed
    ),
]

setup(
    name="recon",
    version="0.1",
    description="My project description",
    author="Your Name",
    author_email="your.email@example.com",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    packages=["recon"],
    zip_safe=False,
)
