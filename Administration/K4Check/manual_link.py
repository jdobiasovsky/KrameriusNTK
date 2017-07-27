from tkinter import Tk
import os.path
import re

print("Getting records...")
print("Once you're done, you can merge 856_kramerius & aleph_manual_export for complete list of records")

if os.path.isfile("./output/missing_in_cat_resume") is True:
    data = open("./output/missing_in_cat_resume", "r")
    print("Resuming session")
else:
    data = open("./output/missing_in_cat.txt", "r")
    print("New session...")
# checks for resume file, if present will skip already done files

for_correction = sorted(data.readlines())
print("Records for manual update: ", len(for_correction))

if os.path.isfile("./output/missing_in_cat_resume") is False:
    print("Trying to recover some records from metadata")
    recoverednum = 0
    for uuid in for_correction:
        # opens each file and tries to find if there is a system number
        recordbuildname = uuid[5:]
        aleph_export = open("./output/aleph_manual_export.txt", 'a')
        recordfile = open("./input/fcrepo_export/uuid_" + recordbuildname[:-1] + ".xml")
        datacheck = recordfile.read()
        try:
            grab_sysno = re.search("(<mods:recordIdentifier source=\".*?\">)"
                                   "(\d\d\d\d\d\d\d\d\d)"
                                   "(</mods:recordIdentifier>)", datacheck)
            if grab_sysno is None:
                grab_sysno = re.search("(<dc:identifier>sysno:)(\d\d\d\d\d\d\d\d\d)(</dc:identifier>)", datacheck)
            sysno = grab_sysno.group(2)
            aleph_export.write(sysno + " 85640 L $$uhttp://kramerius.techlib.cz/search/handle/" + uuid[:-1] +
                               "$$yDigitalizovaný dokument\n")
            # uuid[:-1] removes \n character at the end of line when reading text file
            aleph_export.write(sysno + " BAS   L di\n")
            aleph_export.close()
            for_correction.remove(uuid)
            for_correction.sort()
            update_for_correction = open("./output/missing_in_cat_resume", "w")
            update_for_correction.truncate()
            for line in for_correction:
                update_for_correction.write(line)
            update_for_correction.close()
            # writes into manual export file and removes processed uuid from queue
            recoverednum += 1
        except AttributeError:
            continue
    print("Records for manual update: ", len(for_correction))
# will prompt user to start inputting system numbers that weren't recovered automatically

r = Tk()
# tkinter
for uuid in for_correction:
    aleph_export = open("./output/aleph_manual_export.txt", 'a')
    print("\n---------------\n" + uuid)

    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append("http://kramerius1.ntkcz.cz:8080/fedora/objects/" + uuid + "/export")
    # copies link into clipboard so user doesn't have to write it every time
    r.update()  # now it stays on the clipboard after the window is closed

    sysno = input("SYSNO / skip / exit: \n")
    if sysno == "skip":
        skips = open("./output/missing_in_cat_skipped.txt", "a")
        skips.write("https://kramerius.techlib.cz/search/handle/" + uuid)
        skips.close()
        for_correction.remove(uuid)
        for_correction.sort()
        update_for_correction = open("./output/missing_in_cat_resume", "w")
        update_for_correction.truncate()
        for line in for_correction:
            update_for_correction.write(line)
        update_for_correction.close()
        continue
    if sysno == "exit":
        print("Exiting...")
        exit(0)

    while len(sysno) is not 9:
        print("Invalid...")
        sysno = input("Enter SYSNO: \n")

    aleph_export.write(sysno + " 85640 L $$uhttps://kramerius.techlib.cz/search/handle/" + uuid[:-1] +
                       "$$yDigitalizovaný dokument\n")
    # uuid[:-1] removes \n character at the end of line when reading text file
    aleph_export.write(sysno + " BAS   L di\n")
    aleph_export.close()
    for_correction.remove(uuid)
    for_correction.sort()
    update_for_correction = open("./output/missing_in_cat_resume", "w")
    update_for_correction.truncate()
    for line in for_correction:
        update_for_correction.write(line)
    update_for_correction.close()
    # writes into manual export file and removes processed uuid from queue

    print("Records for manual update: ", len(for_correction))
    print("\n---------------\n")
