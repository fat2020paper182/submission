# small script to remove duplicated headers in csv files
import sys

with open(sys.argv[1]) as f:
    print(f.readline().strip())
    for line in f:
        if not line.startswith('time'):
            print(line.strip())
