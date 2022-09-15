# Frequently Asked Questions


	
*The list of answered questions is being built. If your question is not in the list, please contact us.*

You may also consult the [Discussions](https://github.com/bruneval/molgw/discussions) section on our github page.


---
## Compilation

### The fortran compiler complains about new Fortran syntax, such as `c%re` for the complex number real part, or `class(*)` for polymorphic data

Use a newer fortran compiler. Gfortran  ≥ 9 or Intel ≥ 19 are strongly recommended.


### At linking time, the compiler complains about not finding some mathematical functions, for instance, `undefined reference to 'sqrtq'`

Sometimes LIBCINT is compiled with quadruple-precision maths in C.

Just edit `my_machine.arch` to add `-lquadmath`:

```sh
LIBCINT=-lcint -lquadmath
```


### Compilation of LIBINT is hard, long, delicate.

Yes, we are aware of that.

Starting with MOLGW version 3, **LIBCINT** can be used instead of **LIBINT**.
From our tests, LIBCINT is faster to compile and faster to run.
We strongly advise to switch to LIBCINT.

Please consult the [tutorial about compilation](tuto_compilation.md) for help.


### When compiling **MOLGW**, I obtain the following kinds of errors:

```sh
libint_twobody.cc(57): error: identifier "Libint_2eri_t" is undefined
   Libint_2eri_t* inteval = libint2::malloc(contrdepth2);
   ^
libint_twobody.cc(57): error: identifier "inteval" is undefined
   Libint_2eri_t* inteval = libint2::malloc(contrdepth2);

libint_twobody.cc(57): error: no instance of overloaded function "libint2::malloc" matches the argument list
            argument types are: (const unsigned int)
   Libint_2eri_t* inteval = libint2::malloc(contrdepth2);
                            ^
libint_twobody.cc(59): error: identifier "LIBINT2_MAX_AM_2eri" is undefined
   assert(amA <= LIBINT2_MAX_AM_2eri);
   ^
```
These errors are related to missing routines in the compilation of the LIBINT library.
Indeed, **MOLGW** needs a rather complete (and rather lengthy) compilation of LIBINT.
In particular, **MOLGW** absolutely requires the 2- and 3-center integrals.
Please make sure that LIBINT is configured (and then compiled) with at least options `--enable-eri3=0 --enable-eri2=0 --enable-contracted-ints`.


---
## Running the code 

### The job crashes with message:

```sh
At line 786 of file m_inputparam.f90 (unit = 5, file = 'stdin')
Fortran runtime error: End of file
```
You certainly wrote symbol < before the input file name in the command line. The correct use of **MOLGW** is simply ./molgw inputfile > outfile.

### Segmentation faults occur at runtime when using OPENMP parallelization.

Maybe you are short of OpenMP dedicated memory. Try
```sh
export OMP_STACKSIZE=512M
```
and run again.


---
## DFT / HF ground-state

### The SCF cycles do not converge smoothly. What should I do?

First of all, check your input file. Double-check the number of electrons, the spin configuration, the geometry of the molecule with a visualizer.
Then, be sure **MOLGW** does not start from a stupid RESTART file from a previous run for another molecule. The RESTART procedure is very permissive and allows for very unusual restarts.
Finally, tune the SCF cycling procedure. You may (in order of increasing difficulty and decreasing success rate)

- Decrease the desired accuracy with tolscf. Use for instance 5.0e-4. The default value is much often way too tight.
- Increase the history for Pulay mixing with `npulay_hist` (but not too much).
- For metallic systems (or having a small HOMO-LUMO gap), use some finite temperature with `temperature=0.1` for instance.
- For metallic systems (or having a small HOMO-LUMO gap), charge sloshing may occur. You can use the simplistic density-matrix linear damping implemented in **MOLGW**: `density_matrix_damping=0.5` for instance.
- Reduce the linear dependence in the basis set by increasing `min_overlap`. Try 1.0e-4, 1.0e-3 for instance.
- Avoid completely the Pulay mixing with `mixing_scheme='simple'` (works for isolated atoms or diatomic molecules).
- Use level shifting to open up the HOMO/LUMO gap with `level_shifting_energy`. Be careful with level shifting.
It may converge very smoothly to a local minimum and stay there forever.

### **MOLGW** does not want to read an old RESTART file.

From time to time, the format for RESTART files is changed. Then, the old files are not readable anymore.
Compatibility is not ensured by the developers.
Solutions: run the calculation again from scratch or stick to the **MOLGW** version that was used to generate the RESTART file.


---
## $GW$ calculation

### What is the largest system **MOLGW** can calculate within GW?

Well... It mostly depends on the basis set size and on the number of electrons.
In general, the most time-consuming and memory-limiting step is the diagonalization of the polarizability in the transition basis (Casida-like equation).
Evaluate the size of the product basis as

$$
N_{t} = N_\mathrm{occ} \times N_\mathrm{virtual} \times N_\mathrm{spin}
$$

The memory requirement scales as $N_{t}^2$ and the CPU time goes as $N_{t}^3$.
As an example, a $150,000 \times 150,000$ matrix diagonalization takes about 2 hours on 512 cores on 2018 supercomputer.
Do not hesitate to set `frozencore='yes'` to limit the number of active occupied states without much loss of accuracy.

If you are *just* interested in the HOMO/LUMO region, you may consider the Padé analytic continuation approach.
This avoids completely the diagonalization at the expense of a quadrature in the imaginary frequencies.
See the [tutorial](tuto_gw.md) for more details.


### Why does the first iteration of evGW (or GnWn) differ from G0W0?

For speed and simplicity, we decided to just evaluate the self-energy at the previous quasiparticle energy in evGW.

$$
  \Sigma_c(\epsilon_i^{(n-1)})
$$

instead of 

$$
  \Sigma_c(\epsilon_i^{(n)})  .
$$

This avoids the calculation of multiple frequencies and skips the graphical solution technique.
Once the self-consistency is reached $\epsilon_i^{(n-1)}=\epsilon_i^{(n)}$, the final result should be insensitive to this technical choice:
the self-energy is evaluated at the correct self-consistent quasiparticle energy!


---
## BSE / TDDFT calculation

### I would like to perform a BSE calculation on top of QSGW, however **MOLGW** keeps asking for an `ENERGY_QP` file.

The `ENERGY_QP` file is meant for one-shot GW runs. In QSGW, it is not needed. You can cheat on **MOLGW** by asking to use a tiny scissor shift of the energies so to skip the `ENERGY_QP` file reading with `scissor=0.00001`.

### The linear-response TDDFT calculations are awfully slow.

The construction of the TDDFT kernel is not optimized at all in **MOLGW**.
However you may save much time by using a smaller integration grid without much loss of accuracy with `tddft_grid_quality='low'` or `tddft_grid_quality='medium'`

### TDDFT and BSE solver complains that matrix (A-B) is not positive definite.

If (A-B) is not positive definite, this usual means that the singlet ground-state is metastable against a triplet ground-state.
As a consequence, the BSE or TDDFT will have negative neutral excitations.
Switching on the so-called Tamm-Dancoff approximation with `tda='yes'` may numerically solve the problem.
The literature about the singlet/triplet instability is vast in the TDDFT community.



