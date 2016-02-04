# read files from dataset/neg and dataset/pos
# in each directory, extract the danmakus during the last 10 minutes. 
# import glob
# import os
# print os.listdir("")
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')
import codecs
from os import walk

def getMovieDurationInSeconds(path):
    with open(path, 'rb') as fh:
        first = next(fh).decode()
        fh.seek(-1024, 2)
        last_line = fh.readlines()[-1].decode()
        duration=last_line.split(",")[0] 
    return duration
    
def extractDanmakus(path,from_time, to_time):
    danmakus=""
    print path
    for line in codecs.open(path,'r','utf-8'):
        timestamp = float(line.split(",")[0])

        if timestamp <= to_time and timestamp >= from_time :
            content = line.split(",")[2]
            
            danmakus+=" "+content
    return danmakus

        
f = []
danmu_file = codecs.open('preparedData.csv', 'w', 'utf-8')
for (dirpath, dirnames, filenames) in walk("dataset/neg/"):
    f.extend(dirnames)
    print dirnames

    for dirname in dirnames:

        danmaku_path = "dataset/neg/"+dirname+"/danmu.csv"
        duration = float(getMovieDurationInSeconds(danmaku_path))
        from_timestamp = duration - 10*60
        to_timestamp = duration
        danmakus = extractDanmakus(danmaku_path,from_timestamp,to_timestamp)
        danmakus_line = "neg,"+ danmakus+"\n"
        danmu_file.write(danmakus_line)

    break
    
for (dirpath, dirnames, filenames) in walk("dataset/pos/"):
    f.extend(dirnames)
    for dirname in dirnames:

        danmaku_path = "dataset/pos/"+dirname+"/danmu.csv"
        duration = float(getMovieDurationInSeconds(danmaku_path))

        from_timestamp = duration - 10*60
        to_timestamp = duration

        danmakus = extractDanmakus(danmaku_path,from_timestamp,to_timestamp)

        danmakus_line = "pos," +danmakus+"\n"
        danmu_file.write(danmakus_line)

    break
danmu_file.close()