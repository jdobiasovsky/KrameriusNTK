#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import re
import shutil

print("Will check whether digital object is in catalog and verify it's ID structure...")
print("Required files for input:")
print(">>> ./input/fcrepo_export/uuid_*         # Exported objects from fedora repository")
print(">>> ./input/idlist.xml                   # VuFind export for tag \"Digitized\"")

input("Press ENTER to continue...")
print("\n\n")
print("Checking presence in catalog...")

idlist = open("./input/idlist.xml", "r")
idlist_walk = re.findall("(uuid:.*?)<", idlist.read(), re.DOTALL)
print("Total items: ", len(idlist_walk))

missing = open("./missing_in_cat.txt", "w")
correct = open("./present_in_cat.txt", "w")
missing_count = 0
correct_count = 0

for files in glob.glob("./input/fcrepo_export/*.xml"):
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
proc_count = 0
err_count = 0
disc_count = 0

for file in glob.glob("./input/fcrepo_export/**/*.xml", recursive=True):
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

            aleph_export.write(sysno + " 85640 L $$uhttp://k4.techlib.cz/search/handle/" + uuid +
                               "$$yDigitalizovaný dokument\n")
            aleph_export.write(sysno + " BAS   L di\n\n")

            shutil.move(file, "./output/processed/" + re.search("uuid_.*.xml", file).group(0))
            proc_count += 1
            data.close()
        except AttributeError:
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



