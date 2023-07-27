#!/usr/bin/python
from __future__ import print_function
__author__ = "Dr. Dinga Wonanke"
__status__ = "production"
import random
import glob
import shutil
destination = ''  # '../db/html/'
source = ''  # '/Volumes/Elements/MOF_Database/Articles/All_HTML/*html'
all_html = glob.glob(source)
selected = random.sample(all_html, 500)

for files in selected:
    shutil.copy(files, destination)
