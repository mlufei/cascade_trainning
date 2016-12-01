#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys
from PIL import Image
from optparse import OptionParser
import cv2

def skinDetect(srcFile, destFile):
	src = cv2.imread(srcFile)
	dest = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
	dest = cv2.inRange(dest, (7, 10, 60), (29, 150, 255))
	cv2.imwrite(destFile, dest)

if __name__ == "__main__":
	parser = OptionParser(version = "v0.1")
	parser.add_option("-s", "--src", dest="src", help="the src images' path", metavar="DIRECTORY")
	parser.add_option("-d", "--dir", dest="dir", help="the dir images' path", metavar="DIRECTORY")
	(options, args) = parser.parse_args()
	if os.path.isdir(options.src) == False:
		print "can not find the ", options.src, " directory..."
		sys.exit(-1)
	if os.path.exists(options.dir) == False:
		os.makedirs(options.dir)

	index = 0
	print "start skin detect all images in '%s' floder " % (options.src)
	for file in os.listdir(options.src):
		if file.endswith("jpg"):
			skinDetect(os.path.join(options.src, file), os.path.join(options.dir, file))
			#print os.path.join(options.src, file), "   ", os.path.join(options.dir, file)
			#exit()
			index += 1
	print "total size: ", index
