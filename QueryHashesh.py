import psycopg2
from PIL import Image
import imagehash
import os
maxDifference = 0 #the maximum hamming distance
conn = psycopg2.connect(database = "postgres", user = "postgres", password = "mehrdad", host = "127.0.0.1")
cursor = conn.cursor()
print("Connection Successful to PostgreSQL")

def twos_complement(hexstr, bits):
        value = int(hexstr,16) #convert hexadecimal to integer

		#convert from unsigned number to signed number with "bits" bits
        if value & (1 << (bits-1)):
            value -= 1 << bits
        return value
#flag=True
#frameNum = 4
#while (flag==True | frameNum <= 4)
myDir = './frames/'
for entry in sorted(os.listdir("./frames")):
    dummyFrame=int(entry.split('.')[0])
    print('Checking frame id: %2d' % (dummyFrame))
    path = myDir + entry
    with open(path, "rb") as imageBinary:
            img = Image.open(imageBinary)
            imgHash=str(imagehash.phash(img))
            hashInt = twos_complement(imgHash, 64) #convert from hexadecimal to 64 bit signed integer
            cursor.execute(f"SELECT appname FROM hashes WHERE (frameid={dummyFrame} AND hash <@ ({hashInt}, {maxDifference}))")
            hashRows = cursor.fetchall()
            appnames = [x[0] for x in hashRows]
            if(len(appnames)!=1):                
                flag=False
                print('Behavior not found, please perform the computation')
                break
            print('Looking like: %s'% (appnames[0]))
