from tkinter import Tk
import os.path

print("Getting records...")

if os.path.isfile("./output/missing_in_cat_resume") is True:
    data = open("./output/missing_in_cat_resume", "r")
    print("Resuming session")
else:
    data = open("./output/missing_in_cat.txt", "r")
    print("New session...")

for_correction = sorted(data.readlines())
print("Records for manual update: ", len(for_correction))
r = Tk()
# tkinter

for uuid in for_correction:
    aleph_export = open("./output/aleph_manual_export.txt", 'a')
    print("\n---------------\n" + uuid)

    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append("http://kramerius1.ntkcz.cz:8080/fedora/objects/" + uuid + "/export")
    r.update()  # now it stays on the clipboard after the window is closed
    # copy fedora link into clipboard

    sysno = input("SYSNO / skip / exit: \n")
    if sysno == "skip":
        continue
    if sysno == "exit":
        exit(0)

    while len(sysno) is not 9:
        print("Invalid...")
        sysno = input("Enter SYSNO: \n")

    aleph_export.write(sysno + " 85640 L $$uhttp://kramerius.techlib.cz/search/handle/" + uuid +
                       "$$yDigitalizovaný dokument\n")
    aleph_export.write(sysno + " BAS   L di\n")
    aleph_export.close()
    for_correction.remove(uuid)
    for_correction.sort()
    update_for_correction = open("./output/missing_in_cat_resume", "w")
    update_for_correction.truncate()
    for line in for_correction:
        update_for_correction.write(line)
    update_for_correction.close()

    print("Records for manual update: ", len(for_correction))
    print("\n---------------\n")
