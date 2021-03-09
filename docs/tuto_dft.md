# DFT or HF calculations

Nothing simpler!

The input files consists of two sections:

1. A Fortran namelist starting with `&molgw` and ending with `/`.
Fortran syntax is applied here. Comments are marked with `!`. A comma `,` is a valid delimiter.

2. A list of atoms, which is very similar to an xyz file


Here follows a self-consistent DFT calculations with BHLYP functional.

```fortran
&molgw
  comment='H2O within BHLYP'    ! an optional plain text here

  scf='BHLYP'                   ! 'HF' gives Hartree-Fock

  basis='cc-pVTZ'
  auxil_basis='cc-pVTZ-RI'

  natom=3                       ! Atomic coordinates are in angstrom, unless otherwise stated
/
O      0.000000  0.000000  0.119262
H      0.000000  0.763239 -0.477047 
H      0.000000 -0.763239 -0.477047 
```

