import cv2
import sys
import glob
import os

pixels = []
frames = []

showOutput = False

#Transforming mp4 to frame files in temp directory
vidcap = cv2.VideoCapture(sys.argv[1])
success, image = vidcap.read()

totalFrames = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

s = input("Show debug output in console? (may slow down the program) Y / N\n")
if s.upper() == "Y":
    showOutput = True

count = 0
while(success):
    cv2.imwrite("temp/frame%d.jpg" % count, image)

    #Saving all framePaths instead of saving frame images in memeroy to reduce load
    frames.append("temp/frame%d.jpg" % count)

    if showOutput:
        print(round(count/totalFrames*100,2), "%")

    success, image = vidcap.read()
    count += 1

if showOutput:
    print("Finished loading frames, now converting frames to bytes.")

width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#Handling width encoding: first 8 bytes will be summed up to get width of frame
for i in range(0,8):
    if width-255 > 0:
        pixels.append(255)
        width-=255
    else:
        pixels.append(width)
        width-=width

#Handling height encoding: second 8 bytes will be summed up to get height of frame
for i in range(0,8):
    if height-255 > 0:
        pixels.append(255)
        height-=255
    else:
        pixels.append(height)
        height-=height

width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))

for i in range(0,len(frames)):
    img = cv2.imread(frames[i])
    for y in range(0, height):
        for x in range(0, width):
            pixelColor = img[y,x][0]
            pixels.append(pixelColor)
    
    if showOutput:
        print(round(i/totalFrames*100,2),"%")

if showOutput:
    print("Finished converting, now writing to output file.")

fileBytes = bytes(pixels)
with open(sys.argv[2],"wb") as f:
    f.write(fileBytes)

if showOutput:
    print("Finished writing bytes. Delete Frame files?")

s = input("Delete frame-files? Y / N\n")

if s.upper() == "Y" :
    for i in range(0,len(frames)):
        os.remove(frames[i])
        print(round(i/totalFrames*100,2),"%")

exit()