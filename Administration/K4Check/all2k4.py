import re

print("Reading 856_all")
allfile = open("./input/856_all", "r")
k4file = open("./input/856_kramerius", "w")
datalines = allfile.readlines()

for line in datalines:
    searchline1 = re.match("\d\d\d\d\d\d\d\d\d \d\d\d\d\d L \$\$uhttp://k4.techlib.cz/search/handle/.*?\$\$y", line)
    if searchline1 is not None:
        k4file.write(line)

    searchline2 = re.match("\d\d\d\d\d\d\d\d\d \d\d\d\d\d L \$\$uhttp://kramerius.techlib.cz/search/handle/.*?\$\$y",
                           line)
    if searchline2 is not None:
        k4file.write(line)

print("Done, stored data into 856_kramerius")
