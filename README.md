# PDB Residue Types

Extract dictionaries of types of [PDB](http://www.rcsb.org/pdb/home/home.do)
residues from the Chemical Component dictionary.

## Dependencies

    pip install -r requirements.txt

## Scripts

- `config.py`: Set up where to save files
- `update_chemcomp_dict.py`: Download the latest version of the Chemical Components dictionary
- `determine_residue_types.py`: Assign simple types to each PDB residue ID, e.g. protein/peptide, DNA, RNA, saccharide, non-polymer
