import os
import urllib2

from config import DATA_DIR, COMP_DICT_URL, COMP_DICT_FILE

# MAKE THE DATA DIRECTORY IF IT DOESN'T EXIST
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# GET CHEMCOMP FILE AND SAVE LOCALLY
response = urllib2.urlopen(COMP_DICT_URL)

print "Saving chemical components file..."
with open(COMP_DICT_FILE, 'wb') as fo:
    fo.write(response.read())
