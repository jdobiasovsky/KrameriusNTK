#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import re
import shutil

print("Will check whether digital object is in catalog and verify it's ID structure...")
print("Required files for input:")
print(">>> ./input/fcrepo_export/uuid_*         # Exported objects from fedora repository")
print(">>> ./input/856_kramerius                # Scratch file from Aleph for 856_kramerius (scratch/STK01/...")

input("Press ENTER to continue...")
print("\n\n")
print("Checking presence in catalog...")

idlist = open("./input/856_kramerius", "r")
idlist_walk = re.findall("(search/handle/)(uuid:.*?)(\$\$y)", idlist.read(), re.DOTALL)
idlist_walk = [x[1] for x in idlist_walk]
# makes list of uuid identifiers found in 856_kramerius (documents present in catalog)
print("Total items: ", len(idlist_walk))

missing = open("./missing_in_cat.txt", "w")
correct = open("./present_in_cat.txt", "w")
# files that will list all documents present / missing in catalog
missing_count = 0
correct_count = 0
# counters for no. of documents present / missing

for files in glob.glob("./input/fcrepo_export/*.xml"):
    # iterates through all files in ^path, checks their uuid against idlist, copies to target folders according to result
    file_uuid = re.search("(./input/fcrepo_export/uuid_)(.*?)(.xml)", files)
    uuid = str("uuid:" + file_uuid.group(2))
    if uuid not in idlist_walk:
        missing.write(uuid + "\n")
        missing_count += 1
        shutil.copy(files, "./output/cat_missing/" + re.search("(./input/fcrepo_export/)(.*?.xml)", files).group(2))

    if uuid in idlist_walk:
        correct_count += 1
        correct.write(uuid + "\n")

        shutil.copy(files, "./output/cat_correct/" + re.search("(./input/fcrepo_export/)(.*?.xml)", files).group(2))

missing.close()
correct.close()


print("Verifying metadata structure...")

aleph_export = open("./output/aleph_export", "w")
# file for batch aleph export (scratch/856_kramerius)
proc_count = 0
err_count = 0
disc_count = 0

for file in glob.glob("./input/fcrepo_export/**/*.xml", recursive=True):
    # iterates through given path, checks model, discards if doesn't math criteria
    data = open(file, "r")
    contents = data.read()
    modelcheckmonograph = re.search("(<dc:type>model:monograph</dc:type>)", contents)
    modelcheckperiodical = re.search("<dc:type>model:periodical</dc:type>", contents)
    modelcheckmap = re.search("<dc:type>model:map</dc:type>", contents)
    if modelcheckmonograph or modelcheckperiodical or modelcheckmap is not None:
        try:
            grab_uuid = re.search("(./input/fcrepo_export/uuid_)(.*?)(.xml)", file)
            uuid = "uuid:" + grab_uuid.group(2)

            grab_sysno = re.search("(<mods:recordIdentifier source=\".*?\">)"
                                   "(\d\d\d\d\d\d\d\d\d)"
                                   "(</mods:recordIdentifier>)", contents)
            sysno = grab_sysno.group(2)

            aleph_export.write(sysno + " 85640 L $$uhttp://kramerius.techlib.cz/search/handle/" + uuid +
                               "$$yDigitalizovaný dokument\n")
            aleph_export.write(sysno + " BAS   L di\n\n")
            # extracts uuid and sysno, writes line into aleph_output
            shutil.move(file, "./output/processed/" + re.search("uuid_.*.xml", file).group(0))
            proc_count += 1
            data.close()
        except AttributeError:
            # moves aside files that yield error
            shutil.move(file, "./output/error/" + re.search("uuid_.*.xml", file).group(0))
            err_count += 1
            data.close()
    else:
        shutil.move(file, "./output/discarded/" + re.search("uuid_.*.xml", file).group(0))
        disc_count += 1
        data.close()


print("Done!")
print("\n\n----------------------------------------------------------\n")
print("Succesful verification: ", proc_count)
print("Missing ID or bad sysno syntax: ", err_count)
print("Discarded objects due to model mismatch: ", disc_count)
print("----------------------------------------------------------\n")
print("In catalog:", correct_count)
print("Missing:", missing_count)




