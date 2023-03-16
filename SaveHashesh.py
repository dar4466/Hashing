import psycopg2
import os
from io import BytesIO
from PIL import Image
import imagehash

def twos_complement(hexstr, bits):
        value = int(hexstr,16) #convert hexadecimal to integer

		#convert from unsigned number to signed number with "bits" bits
        if value & (1 << (bits-1)):
            value -= 1 << bits
        return value

conn = psycopg2.connect(database = "postgres", user = "postgres", password = "mehrdad", host = "127.0.0.1")
cursor = conn.cursor()
print("Connection Successful to PostgreSQL")
for entry in os.scandir("./images"):
    splitName=entry.name.split('-')
    appName=splitName[0]
    splitName1=splitName[1].split('.')
    dummy=splitName1[0]
    frameID = int(dummy)
    print(frameID)
    print(appName)
    with open(entry.path, "rb") as imageBinary:
        img = Image.open(imageBinary)
        imgHash = str(imagehash.phash(img))
        hashInt = twos_complement(imgHash, 64)
        cursor.execute("INSERT INTO hashes(hash, appname, frameid) VALUES (%s, %s, %s)", (hashInt, appName, frameID))
        conn.commit()
        print(f"added image with hash {hashInt} to database")
