import os

# WHERE TO DOWNLOAD CHEMCOMP MMCIF FILE FROM
COMP_DICT_URL = 'ftp://ftp.wwpdb.org/pub/pdb/data/monomers/components.cif'

# WHERE TO STORE OUTPUT DATA
DATA_DIR = os.path.join(os.environ['HOME'], 'data', 'pdb_residue_types')

# WHERE TO STORE THE CHEMCOMP MMCIF FILE LOCALLY
COMP_DICT_FILE = os.path.join(DATA_DIR, 'components.cif')

# PROCESSED OUTPUT
RESIDUE_TYPES_JSON_FILE = os.path.join(DATA_DIR, 'pdb_residue_types.json')
RESIDUE_TYPES_BY_RESIDUE_JSON_FILE = os.path.join(DATA_DIR,
                                                  'pdb_residue_types_by_residue.json')
