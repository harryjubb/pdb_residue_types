'''
Uses the Chemical Component dictionary to find out information about PDB
residues.
'''

import os
import simplejson as json

from config import DATA_DIR, COMP_DICT_FILE, RESIDUE_TYPES_JSON_FILE, RESIDUE_TYPES_BY_RESIDUE_JSON_FILE, WATERS

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

# MMCIF FIELDS TO EXTRACT FOR EACH RESIDUE
FIELDS_OF_INTEREST = set([
    'id',
    'name',
    'type',
    'pdbx_type',
    'formula',
    'mon_nstd_parent_comp_id',
    'pdbx_synonyms',
    'one_letter_code',
    'three_letter_code',
])

# CHECK THAT THE OUTPUT DIRECTORY EXISTS
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# CHECK THAT THE CHEMICAL COMPONENTS DICTIONARY HAS BEEN DOWNLOADED
if not os.path.exists(COMP_DICT_FILE):

    print 'Dictionary file not found, downloading...'

    # DOWNLOAD IF NOT
    os.system('python {}'.format(os.path.join(SCRIPT_PATH,
                                              'update_chemcomp_dict.py')))

# PARSE THE FILE AND EXTRACT THE RESIDUE TYPE DATA
print 'Parsing Chemical Component dictionary...'
compounds = {}

current_compound = None

with open(COMP_DICT_FILE, 'rb') as fo:
    for line in fo:

        line = line.strip()

        if line.startswith('data_'):
            current_compound = line[-3:]
            if current_compound not in compounds:
                compounds[current_compound] = {}
            else:
                raise ValueError('Shouldn\'t have duplicate compounds '
                                 '({} was duplicated)'.format(current_compound)
                                 )

            continue

        if line.startswith('_chem_comp.'):

            line = line.split()
            line = [line[0]] + [' '.join(line[1:])]
            field = line[0].split('.')[1]

            if field in FIELDS_OF_INTEREST:

                try:
                    compounds[current_compound][field] = line[1].strip('"')
                except IndexError as err:
                    print err.message + ' for {} in {}'.format(line,
                                                               current_compound
                                                               )
                    compounds[current_compound][field] = ''

# CATEGORISE RESIDUE TYPES
print 'Categorising residue types...'
all_res_types = set([x['type'] for x in compounds.itervalues()])

peptide_types = set([x for x in all_res_types if
                     'PEPTIDE' in x.upper() and
                     x.upper() != 'PEPTIDE-LIKE'])
peptide_like_types = set([x for x in all_res_types if
                          x.upper() == 'PEPTIDE-LIKE'])
nucleic_types = set([x for x in all_res_types if
                     'DNA' in x.upper() or
                     'RNA' in x.upper()])
dna_types = set([x for x in all_res_types if 'DNA' in x.upper()])
rna_types = set([x for x in all_res_types if 'RNA' in x.upper()])
saccharide_types = set([x for x in all_res_types if 'SACCHARIDE' in x.upper()])
non_polymer_types = set([x for x in all_res_types if
                         'NON-POLYMER' in x.upper()])

# RESIDUE TYPE JSON
# E.G. {'PEPTIDE': ['ALA', 'CYS', 'GLU'...]}
print 'Collecting residue types for all chemical components...'
residue_types = {
    'peptide': [x['id'] for x in compounds.itervalues() if
                x['type'] in peptide_types],

    'peptide_like': [x['id'] for x in compounds.itervalues() if
                     x['type'] in peptide_like_types],

    # 'nucleic': [x['id'] for x in compounds.itervalues() if
    #             x['type'] in nucleic_types],

    'dna': [x['id'] for x in compounds.itervalues() if
            x['type'] in dna_types],

    'rna': [x['id'] for x in compounds.itervalues() if
            x['type'] in rna_types],

    'saccharide': [x['id'] for x in compounds.itervalues() if
                   x['type'] in saccharide_types],

    'non_polymer': [x['id'] for x in compounds.itervalues() if
                    x['type'] in non_polymer_types and x['id'] not in WATERS],

    'water': [x['id'] for x in compounds.itervalues() if
              x['type'] in non_polymer_types and x['id'] in WATERS],
}

print 'Writing residue types JSON file...'
with open(RESIDUE_TYPES_JSON_FILE, 'wb') as fo:
    json.dump(residue_types, fo)

print 'Statistics'

for res_type, type_compounds in residue_types.iteritems():
    print res_type, ':', len(type_compounds)

# RESIDUE TYPES BY RESIDUE (AS OPPOSED TO BY TYPE)
# E.G. {'ALA': 'L-PEPTIDE LINKING', 'FMM': 'NON-POLYMER'...}
residue_types_by_residue = {}

for res_type, type_compounds in residue_types.iteritems():
    for compound in type_compounds:
        if compound not in residue_types_by_residue:
            residue_types_by_residue[compound] = res_type
        else:
            raise ValueError('residue_types_by_residue should not have '
                             'duplicates ({})'.format(compound))

print 'Writing residue types by residue JSON file...'
with open(RESIDUE_TYPES_BY_RESIDUE_JSON_FILE, 'wb') as fo:
    json.dump(residue_types_by_residue, fo)
