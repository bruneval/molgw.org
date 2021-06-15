# Download

## Sources

- Latest release [MOLGW 2.F](https://github.com/bruneval/molgw/archive/v2.F.tar.gz)

- Browse the latest sources directly on github [![github](img/icon_github.png)](https://github.com/bruneval/molgw)

- Clone **MOLGW** with `git` 
```sh
git clone https://github.com/bruneval/molgw.git molgw
```

## Compilation

### Compilers

Fortran2008 and C++ compilers are mandatory.

**MOLGW** is specifically tested to compile properly with

- the GNU compiler suite: `gfortran` and `g++` (Version ≥ 9.1.0 recommended)
- the Intel compiler suite: `ifort` and `icpc` (Version ≥ 19.0 recommended)

### Libraries

**MOLGW** requires three external libraries:

- **BLAS/LAPACK** (mandatory) for linear algegra from [netlib.org](http://www.netlib.org) or better from the vendor of your specific machine.
For instance, for Intel processors, the highly efficient MKL library can be obtained for free

- **Libint** (mandatory) for the Coulomb integrals evaluation: [Download page](https://github.com/evaleev/libint/releases/)
    - Recommended version: [2.6.0](https://github.com/evaleev/libint/releases/tag/v2.6.0)

- **Libxc** (mandatory) for the exchange-correlation approximation of DFT: [Download Page](https://www.tddft.org/programs/libxc/download/previous/)
    - Recommended version: [5.1.5](http://www.tddft.org/programs/libxc/down.php?file=5.1.5/libxc-5.1.5.tar.gz)

and two optional libraries to run in parallel:

- **MPI** (optional) for distributed calculations from [open MPI](http://www.open-mpi.org) for instance
- **SCALAPACK** (optional) for distributed linear algegra from [netlib.org](http://www.netlib.org) or better from the vendor of your specific machine.


### Configuration

Libraries and compilers are all set up in a file named `my_machine.arch` that should be created or copied in the `src/` folder.

Examples of typical `my_machine.arch` are provided in the `config/` folder.


### Help needed for the compilation?

Please visit the [tutorial section](tuto_compilation.md).
