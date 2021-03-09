# Running MOLGW

**MOLGW** runs with
```bash
/path/to/molgw molgw.in > molgw.out 
```

With MPI, use
```bash
mpirun /path/to/molgw molgw.in > molgw.out 
```

With OPENMP, use
```bash
export OMP_NUM_THREADS=4
export OMP_STACKSIZE=512M
```

When `OMP_STACKSIZE` is too small, segmentation faults occur.


The input file are explained [here](tuto_dft.md).

