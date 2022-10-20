from ase.build import fcc111, surface, sort, niggli_reduce, add_adsorbate
from ase.calculators.emt import EMT
from ase.db import connect
from ase.io import read, write
from ase.visualize import view
from ase import Atoms
import os
import numpy as np
import collections
from tools import fix_lower_surface, sort_atoms_by
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--cif_file")
parser.add_argument("--adsorbate_smiles", help="smiles string for adsorbate")
parser.add_argument("--rotate", default=None, type=str, help="x|y|z,degree")
parser.add_argument("--height", default=None, type=float)
parser.add_argument("--nlayer", default=4, type=int)
parser.add_argument("--vacuum", default=10.0, type=float)

args = parser.parse_args()

cif_file = args.cif_file
adsorbate_smiles = args.adsorbate_smiles

if args.rotate is None:
    rotate_dir_and_angle = ["x", 0]
else:
    rotate_dir_and_angle = [args.rotate[0], args.rotate[2:]]

if args.height is None:
    height = 4.0
else:
    height = args.height

nlayer = args.nlayer
vacuum = args.vacuum

lattice = "fcc"
facet   = "111"
#lattice = "hcp"
#lattice = "sp15"
#facet = "010"

indices = []
for c in facet:
    indices.append(int(c))
bulk = read(cif_file)
surf = surface(lattice=bulk, indices=indices, layers=nlayer, vacuum=vacuum)

surf = surf*[3, 3, 1]
#surf = surf*[3, 2, 1]
surf = sort(surf)
surf = sort_atoms_by(surf, xyz="z")

formula = surf.get_chemical_formula()

offset_fac = (2.1, 1.5)
offset_fac = np.array(offset_fac)

surf.translate([0, 0, -vacuum+0.5])
surf = fix_lower_surface(surf)
#
# prepare adsorbate
#
os.system('obabel -:"{0:s}" -oxyz -h --gen3D -O tmp.xyz'.format(adsorbate_smiles))
adsorbate = read("tmp.xyz")
adsorbate.center()
adsorbate.rotate(v=rotate_dir_and_angle[0], a=int(rotate_dir_and_angle[1]))

# shift
min_ind = min(adsorbate.positions[2, :])
adsorbate.translate([0, 0, -min_ind])

#
# adsorb on surface
#
if adsorbate is not None:
    offset = (0.16, 0.33)  # x1y1
    offset = np.array(offset)
    add_adsorbate(surf, adsorbate, height=height, position=(0, 0), offset=offset*offset_fac)

write("POSCAR", surf)
