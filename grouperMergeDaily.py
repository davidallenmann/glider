import glob, os

dataPath = '/w/loggerhead/glider/M72/daily'
# output file
mergeFile = '/w/loggerhead/glider/M72/M72_RedGrouper.csv'

f1 = open(mergeFile, "w+")

os.chdir(dataPath)
for file in glob.glob("*.csv"):
    print(file)
    with open(file) as f:
        for line in f:
            f1.write(line)

f1.close()