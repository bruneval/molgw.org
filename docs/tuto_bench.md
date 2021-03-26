# Running series of calculations with python


Here we use a python script to generate many input files for **MOLGW**.
A template in python3 is given in `~molgw/utils/run_molgw.py`

Let us use the [GW100 benchmark](https://gw100.wordpress.com/) which collects the HOMO energy of 100 molecules.


# Generate the input files

The python script `run_molgw.py` runs over all the xyz files found in a folder named `structures'.

Download the structures [here](files/gw100xyz.tgz)

```sh
tar xzf gw100xyz.tgz
cp /path/to/molgw/utils/run_molgw.py .
```

Then edit the script especially here

```python
##################################################
#
# Hard-coded information
#
directory       = 'run_bhlyp'
executable      = '${HOME}/devel/molgw/molgw'
```

and here

```python
##################################################
#
# Create the calculation list here
#
ip = []
for basis in ['Def2-TZVPP']:
    ipp = collections.OrderedDict()
    ipp['basis']                   = basis
    ipp['ecp_basis']               = basis
    ipp['scf']                     = 'BHLYP'
    ipp['postscf']                 = 'G0W0'
    ipp['selfenergy_state_range']  = 3
    ipp['frozencore']              = 'yes'
    ipp['auxil_basis']             = 'AUTO'
    ipp['ecp_type']                = 'Def2-ECP'
    ipp['ecp_elements']            = 'Rb Ag I Xe'
    ip.append(ipp)
```

```sh
python3 run_molgw.py
```
generates all the input files in folder `run_bhlyp` and a bash script `run.sh` that can run all the calculations.

Besides the standard output, **MOLGW** generates a YAML formatted output that is very handy for post-processing.

Here follows a python script that lists all the `molgw.yaml` files and prints all the $GW$ HOMO energies.
The python script will use some functionalities that are implemented in the python module `molgw.py`, which should be added to the `PYTHONPATH` or copied in the working directory.
For instance, 
```sh
export PYTHONPATH=$PYTHONPATH:/path/to/molgw/utils/
```

Here is the script:
```python
#!/usr/bin/python3
  
import molgw


directory = 'run_bhlyp'

calc = molgw.parse_yaml_files(directory)

scf     = calc[0]['input parameters']['scf']
postscf = calc[0]['input parameters']['postscf']

print('\n{:<16} {:<16}  {:^9} {:^9}\n'.format('CAS number','Formula',scf + ' HOMO',postscf+' HOMO'))

data={}
formulas={}
for c in calc:
    mol =  c["input parameters"]["comment"]
    homo_gks = molgw.get_homo_energy("gks",c)
    formulas[mol] = molgw.get_chemical_formula(c)
    try:
        homo_gw  = molgw.get_homo_energy('gw',c)
        print('{:<16} {:<16} {:9.3f} {:9.3f}'.format(mol,formulas[mol],homo_gks,homo_gw))
        data[mol] = homo_gw
    except:
        pass

print('{} HOMO energies have been obtained'.format(len(data)))

details = dict()
details["orbital"]= 'HOMO'
details["remark"]= "RIJK with AUTO"
details["basis_size"]= "3"
details["parameters"]= { "eta": float(calc[0]["input parameters"]["eta"])*27.211 }
details["basis_name"]= calc[0]["input parameters"]["basis"]
details["calc_type"]= postscf + '@' + scf

# Useful addition from MOLGW
details["formulas"]= formulas

molgw.create_gw100_json('gw100'+postscf+'@'+scf+'.json',data,**details)
```


The beginning of the output looks like
```txt
CAS number       Formula           BHLYP HOMO G0W0 HOMO

1309-48-4        MgO                 -7.474    -7.620
60-29-7          C4OH10              -8.900    -9.874
25681-79-2       Na2                 -4.014    -4.929
593-66-8         C2IH3               -7.972    -9.183
1304-56-9        BeO                 -8.546    -9.607
```

A json file named `gw100G0W0@BHLYP.json` is also generated.
It conforms to the standard employed by the official GW100 web site.

Finally we can compare with GW100 data sets, which have been mirrored here:
```sh
wget http://www.molgw.org/files/G0W0@BH-LYP_HOMO_Tv7.0_def2_TZVPP_cbas.json
wget http://www.molgw.org/files/CCSD\(T\)_HOMO_Cv_def2-TZVPP.json
```

and compare them with our results
```py
#!/usr/bin/python3

import sys, json
import matplotlib.pyplot as plt

if len(sys.argv) > 2:
    files = sys.argv[1:3]
else:
    print('please specify two json files')
    sys.exit(1)

sets = []
for file in files:
    with open(file, 'r') as stream:
        try:
            sets.append(json.load(stream))
        except:
            print(file + ' is corrupted')
            pass

mol1 = set(sets[0]["data"].keys())
mol2 = set(sets[1]["data"].keys())
e1 = []
e2 = []

for mol in mol1.intersection(mol2):
   e1.append(float(sets[0]["data"][mol]))
   e2.append(float(sets[1]["data"][mol]))

print('{} common molecules found'.format(len(e1)))

xymin=min(e1+e2)
xymax=max(e1+e2)
plt.xlabel(files[0] + ' (eV)')
plt.ylabel(files[1] + ' (eV)')
plt.plot([xymin,xymax],[xymin,xymax],'-',color='black',lw=2.0)
plt.scatter(e1, e2,label='{} molecules'.format(len(e1)))
plt.legend()
plt.tight_layout()
plt.savefig('comp.png',format='png')
plt.show()
```

The agreement with the implementation in [Turbomole 7](http://www.turbomole.org) is excellent:

![TM](img/turbomole.png)

The small differences are certainly due the auxiliary basis or to the frozencore approximation used here.
The mean absolute error (MAE) is 29 meV.

The agreement with [CCSD(T)](http://dx.doi.org/10.1080/00268976.2015.1025113) is good.
The worst outlier is the HOMO of SO$_2$.
The mean absolute error (MAE) is about 140 meV.

![CC](img/ccsdt.png)


