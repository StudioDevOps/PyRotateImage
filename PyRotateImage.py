#!/usr/bin/python
################################################
#                                              #
#  File Crop Rotate and Add Random Background  #
#    by Jesse Corson and Studio Devops         #
#                                              #
################################################

import random
import sys
from PIL import Image
from os import listdir
from os.path import isfile, join

mypath = "/mnt/instaphoto/"
#mypath = input('Enter the direcotory path surrounded by quoation marks " :  ')

ImgUpperExt = ['.JPG','.PNG','.BMP','.GIF']
ImgLowerExt = [e.lower() for e in ImgUpperExt]
ImgFileExt = tuple(ImgUpperExt + ImgLowerExt)
dirOrig = mypath + "originals/"
bgdirOrig = mypath + "backgrounds/"
dirNew = mypath + "completed/"
anglelist = (-11,-9.-7,-5,-3,3,5,7,9,11)

#Fuction to remove new from the beginning of filenames
def remove_new(f):
  return f[3:]

#Getting Image and Background Filenames
fileOrig = [f for f in listdir(dirOrig) if isfile(join(dirOrig, f)) and  f.endswith(ImgFileExt) and not f.startswith(".")]
fileCompl = [f for f in listdir(dirNew) if isfile(join(dirNew, f)) and  f.endswith(ImgFileExt) and not f.startswith(".")]
fileComplMatch = [remove_new(f) for f in fileCompl]
fileTargets = [f for f in fileOrig if f not in fileComplMatch]
bgfileTargets = [f for f in listdir(bgdirOrig) if isfile(join(bgdirOrig, f)) and f.endswith(ImgFileExt) and not f.startswith(".")]

if not fileTargets:
  print("Either all files have been converted or there are no files to convert")

else:
  print("These files will be adjustedi:")
  print(fileTargets)

  for f in fileTargets:
    pathOrig = dirOrig + f
    img = Image.open(pathOrig, mode='r')

    img_w, img_h = img.size
    topcrop = 400
    botcrop = topcrop + img_w

#Rotating the Image
    img = img.convert(mode="RGBA")
    img = img.crop((0,topcrop, img_w, botcrop))
    img = img.rotate(random.choice(anglelist),expand=1)
    img = img.resize((900,900), Image.ANTIALIAS)
    img_w, img_h = img.size

#Adding the Background Image
    bgfileRan = random.choice(bgfileTargets)
    bgpathRan = bgdirOrig + bgfileRan
    bgimg = Image.open(bgpathRan,mode='r')
    bgimg = bgimg.crop((0,0,img_w, img_h))
    bgimg = bgimg.convert(mode="RGBA")

    img = Image.alpha_composite(bgimg,img)

#Showing the new Images
#  img.show()

#Saving the new file 
    fileNew = "new" + str(f)
    pathNew = dirNew + fileNew
    img.save(pathNew)
    print(fileNew + " saved!")

  print("All files adjusted. That was easy!")


