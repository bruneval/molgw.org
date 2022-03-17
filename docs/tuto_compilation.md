# Compilation

**MOLGW** needs the following compilers:

- Fortran 2008
- C++

To be fully operational, **MOLGW** needs the following libraries:

- LIBCINT or LIBINT for the Gaussian integrals $(\alpha\beta| \frac{1}{|\mathbf{r}-\mathbf{r'}|} | P )$ for instance
- LIBXC  for the DFT approximate functionals: $E_{xc}(\rho(\mathbf{r}))$
- MPI for parallelism
- BLAS/LAPACK/SCALAPACK for the linear algebra (matrix multiplication/inversion/diagonalization)


## Standard route

### Compiling LIBXC

Obtain the latest LIBXC version, compile and install
```sh
wget http://www.tddft.org/programs/libxc/down.php?file=5.1.5/libxc-5.1.5.tar.gz
tar xzf libxc-5.1.5.tar.gz
cd libxc-5.1.5
./configure --prefix=$(HOME)/opt/libxc-5.1.5/
make
make install
```


### Compiling LIBCINT


LIBCINT is a very relevant alternative to LIBINT.

Starting with MOLGW version 3, we strongly advise to use LIBCINT instead of LIBINT.
From our tests, LIBCINT is faster and easier to compile *and* faster to run.

Just compare the length of this tutorial section compared to the LIBINT section...


Here is a compilation example:
```sh
wget https://github.com/sunqm/libcint/archive/refs/tags/v5.1.1.tar.gz
tar xzf v5.1.1.tar.gz; cd libcint-5.1.1
mkdir build; cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=${HOME}/opt/libcint-5.1.1/ -DWITH_RANGE_COULOMB=1 -DBUILD_SHARED_LIBS=0 ..
make; make install
```

But on modern linux distributions, LIBCINT can be obtained with the package manager directly:

On Fedora, for instance:
```sh
sudo dnf install libcint libcint-devel

```



### Compiling LIBINT 

LIBINT is compilation tricky and lengthy. It relies on external libraries and very modern C++.

The external libraries GMP and Boost can be obtained directly on modern linux distributions.
Here is how to compile LIBINT on linux Fedora:
```sh
sudo dnf install automake autoconf gcc-c++ boost-devel gmp-devel # to obtain the required packages
#this is for Fedora but there are equivalent packages for Ubuntu to be obtained with apt-get
wget https://github.com/evaleev/libint/archive/v2.6.0.tar.gz
tar xzf v2.6.0.tar.gz
cd libint-2.6.0
./autogen.sh
mkdir build
cd build
../configure --prefix=$(HOME)/opt/libint-2.6.0/ --enable-1body=1 --enable-eri=0 --enable-eri3=0 --enable-eri2=0 --enable-contracted-ints --with-max-am=7 --with-opt-am=2 --with-cxxgen=g++ --with-cxxgen-optflags=-O1 --with-cxx=g++ --with-cxx-optflags=-O1
make -j 4
make install
```

If LIBINT compilation is really too long, one may reduce it by limiting the maximum angular momentum and removing optimizations:
```sh
../configure --prefix=$(HOME)/opt/libint-2.6.0/ --enable-1body=1 --enable-eri=0 --enable-eri3=0 --enable-eri2=0 --enable-contracted-ints --with-max-am=5 --with-opt-am=1 --with-cxxgen=g++ --with-cxxgen-optflags=-O0 --with-cxx=g++ --with-cxx-optflags=-O0
```

This *fast* compilation took about 25 minutes on a laptop...



### Configuring and compiling MOLGW

Libraries and compilers are all set up in a file named `my_machine.arch` that should be created or copied in the `~molgw/src/` folder.

Examples of typical `my_machine.arch` are provided in the `~molgw/config/` folder.
```sh
cd /path/to/molgw/src
cp ../config/my_machine_gfortran_mpi_mkl.arch my_machine.arch
make -j
```

The executable will be created as `~molgw/molgw`.


Most often, the `my_machine.arch` file needs editing.
Here is an example for gfortran with MKL, MPI and OPENMP.
```sh
OPENMP= -fopenmp

CPPFLAGS=-cpp -DHAVE_LIBXC -DHAVE_MPI -DHAVE_SCALAPACK -DHAVE_MKL -DHAVE_LIBCINT

FC=mpif90
FCFLAGS=  -O2

CXX=g++
CXXFLAGS= -O2

LAPACK= ${MKLROOT}/lib/intel64/libmkl_scalapack_lp64.a -Wl,--start-group ${MKLROOT}/lib/intel64/libmkl_gf_lp64.a ${MKLROOT}/lib/intel64/libmkl_gnu_thread.a ${MKLROOT}/lib/intel64/libmkl_core.a ${MKLROOT}/lib/intel64/libmkl_blacs_openmpi_lp64.a -Wl,--end-group -lgomp -lpthread -lm -ldl

SCALAPACK=

LIBXC_ROOT=${HOME}/opt/libxc-5.1.5/

LIBINT_ROOT=

LIBCINT=-lcint
```

The most tricky line is the [MKL linking](https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/onemkl/link-line-advisor.html).
Another way to obtain this line:
```sh
${MKLROOT}/bin/intel64/mkl_link_tool -libs  --compiler=gnu_f --linking=static --openmp=gomp --cluster_library=scalapack --mpi=openmpi
```











## Spack

[Spack](https://spack.io/) is a handy scientific package manager.
It is an easy way to obtain all the libraries needed by **MOLGW**, and in particular LIBINT.

### Install spack

If you do not have Spack yet, then install it with
```sh
git clone https://github.com/spack/spack.git spack
. spack/share/spack/setup-env.sh  # or better add this line in the ~/.bashrc
spack compilers
==> Available compilers
-- gcc fedora33-x86_64 ------------------------------------------
gcc@10.2.1
```

### Install libraries

Then compiling the libraries should be a piece of cake:
```sh
spack install openmpi                  # MPI
spack install intel-mkl                # BLAS/LAPACK/SCALAPACK
spack install libxc                    # LIBXC
spack install libint tune=molgw-lmax-7 # LIBINT compilation especially tuned for MOLGW
```
Then, load the libraries with the `module` tool:
```sh
module available
#find the unique names for your modules and load them
module load openmpi
module load intel-mkl
module load libxc
module load libint
```

At this stage, the environment should be ready. Test it for instance with
```sh
echo $MKLROOT
```

With this, edit the file `molgw/src/my_machine.arch`:
```sh
OPENMP= -fopenmp

CPPFLAGS=-cpp -DHAVE_LIBXC -DHAVE_MPI -DHAVE_SCALAPACK -DHAVE_MKL

FC=mpif90
FCFLAGS=  -O2

CXX=g++
CXXFLAGS= -O2

LAPACK= ${MKLROOT}/lib/intel64/libmkl_scalapack_lp64.a -Wl,--start-group ${MKLROOT}/lib/intel64/libmkl_gf_lp64.a ${MKLROOT}/lib/intel64/libmkl_gnu_thread.a ${MKLROOT}/lib/intel64/libmkl_core.a ${MKLROOT}/lib/intel64/libmkl_blacs_openmpi_lp64.a -Wl,--end-group -lgomp -lpthread -lm -ldl
```

This simple example creates a fully operational version of **MOLGW** with OPENMP and MPI/SCALAPACK enabled.

Again, the most difficult line is the linking to MKL.


