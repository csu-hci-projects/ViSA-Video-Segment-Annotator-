# Python program to write
# text on video

import sys
import os

from os import walk
from subprocess import check_output

def get_length(file_name):
    a = str(check_output('ffprobe -i  "'+file_name+'" 2>&1 |grep "Duration"',shell=True))
    a = a.split(",")[0].split("Duration:")[1].strip()
    h, m, s = a.split(':')
    s = str(int(float(s))+4)
    if len(s)==1:
        s="0"+s
    return [h,m,s]

sys.tracebacklimit = 0

files = []
for (dirpath, dirnames, filenames) in walk("."):
    files.extend(filenames)
    break

for i in range(len(files)):
    if ".mp4" not in files[i]:
        continue
    f = open("subtitles/"+files[i][:-4]+"_subtitle.srt","w")
    f.write(str(1)+"\n")
    h,m,s = get_length( files[i])
    f.write("00:00:00,000 --> "+h+":"+m+":"+s+",000"+"\n")
    f.write(files[i][:-4] + "\n")
    f.close()
    os.system("ffmpeg -i subtitles/"+files[i][:-4]+"_subtitle.srt subtitles/"+files[i][:-4]+"_subtitles.ass")
    os.system("ffmpeg -i "+files[i]+" -vf ass=subtitles/"+files[i][:-4]+"_subtitles.ass new_videos/"+files[i])
    os.system("rm "+files[i])
