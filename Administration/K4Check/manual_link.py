from tkinter import Tk

data = open("./missing_in_cat.txt")
for_correction = data.readlines()

# Tkinter
r = Tk()

for uuid in for_correction:
    aleph_export = open("./output/aleph_manual_export.txt", 'w')
    print(uuid)
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append("http://kramerius.techlib.cz/search/handle/" + uuid)
    r.update()  # now it stays on the clipboard after the window is closed
    sysno = input("Enter SYSNO: \n")
    while len(sysno) is not 9:
        print("Invalid...")
        sysno = input("Enter SYSNO: \n")

    aleph_export.write(sysno + " 85640 L $$uhttp://kramerius.techlib.cz/search/handle/" + uuid +
                       "$$yDigitalizovaný dokument\n")
    aleph_export.write(sysno + " BAS   L di\n\n")
    aleph_export.close()

