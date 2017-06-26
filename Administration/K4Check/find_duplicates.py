import re

print("Scanning 856_kramerius_new for possible duplicates")

duplicates = open("./output/duplicates.txt", "a")
scanfile = open("./output/856_kramerius_new.txt", "r")
scanfile_data = scanfile.read()
sysnolist = list()
uuidlist = list()

for match in re.findall("(\d\d\d\d\d\d\d\d\d)( \d\d\d\d\d L \$\$uhttp)", scanfile_data):
    sysnolist.append(match[0])


for match in re.findall("(search/handle/)(uuid:.*?)(\$\$y)", scanfile_data):
    uuidlist.append(match[1])

print("Total system numbers found: ", len(sysnolist))
print("Total uuid's found: ", len(uuidlist))

dupl_sysno_count = 0

for sysno in set(sysnolist):
    match = re.findall(sysno + " \d\d\d\d\d L \$\$uhttp", scanfile_data)
    if len(match) > 1:
        print("Duplicate:", match)
        dupl_sysno_count += 1
        duplicates.write("Duplicate sysno: " + sysno + "\n")

dupl_uuid_count = 0
for uuid in set(uuidlist):
    match = re.findall(uuid, scanfile_data)
    if len(match) > 1:
        print("Duplicate: ", match)
        dupl_uuid_count += 1
        duplicates.write("Duplicate uuid: " + uuid + "\n")

print("Found:", dupl_uuid_count, " duplicate uuid's")
print(dupl_sysno_count, " duplicate sysno's")
