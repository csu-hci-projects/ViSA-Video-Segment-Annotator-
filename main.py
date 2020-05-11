import os
import sys
os.system("python ffmpeg-split.py -f "+sys.argv[1]+" -v h264 -m manifest.csv;python annotate.py")

