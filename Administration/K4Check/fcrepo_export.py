import glob
import re
from time import gmtime, strftime

print("Generates uuid list from fedora object repostiory. Press start to begin: ")
input()

convert = open("./output/fedora_list.txt", "w")
total_processed = 0
object_count = 0
print("Fetching object list")

for filename in glob.glob("/mnt/kramerius/data/fata5/fedora-3.5/data/objects/**/uuid_*", recursive=True):
        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), " >>> Found", filename)
        print("Object count: ", object_count)
        object_count += 1
        filedata = open(filename, "r")
        contents = filedata.read()
        print("File data read")
        modelcheckmonograph = re.search("(<dc:type>model:monograph</dc:type>)", contents)
        modelcheckperiodical = re.search("<dc:type>model:periodical</dc:type>", contents)
        modelcheckmap = re.search("<dc:type>model:map</dc:type>", contents)
        print("Checking object model")
        if modelcheckmonograph or modelcheckperiodical or modelcheckmap is not None:
                convert.write(filename + "\n")
                print("Correct model, writing " + filename)
                filedata.close()
                total_processed += 1
                continue

        print("Incorrect object model, skipping...")
        filedata.close()

print("Script finished!")
convert.write("List complete! Time process was terminated: " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
convert.close()
