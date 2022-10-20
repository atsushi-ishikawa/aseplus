# aseplus

## Usage
### `make_adsorbed_surf.py`
* Make surface + adsorbate system, and output it to a VASP POSCAR file
 
#### Argument
* `--cif_file`: cif file for surface
* `--adsorbate_smiles`: SMILES string for adsorbate
* `--rotate`: rotation direction and angle (e.g. x,90)
* `--height`: height of adsorbate

#### Note
* please adjust rotate and height arguments by checking POSCAR
 
#### Example
* `python make_adsorbed_surf.py --cif_file="Pt.cif" --adsorbate_smiles="NC1=CC=CC=C1" --rotate=y,90 --height=2.0`