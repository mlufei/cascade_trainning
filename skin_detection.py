#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys
from PIL import Image
from optparse import OptionParser
import cv2

def isSkinByRGB(R, G, B):
	i1 = (R > 95) and (G > 40) and (B>20) and (abs(R-G)>15) and (R > G) and (R > B)
	i2 = ((max(R, max(G, B)) - min(R, min(G, B)))>15) 
	i3 = (R > 220) and (G > 210) and (B > 170) and (abs(R-G) <= 15) and (R > G) and (R > B)
	return ((i1 and i2) or i3)

def isSkinByYCrCb(Y, Cr, Cb):
	i1 = Cr <= 1.5862 * Cb + 20
	i2 = Cr >= 0.3448 * Cb + 76.2069
	i3 = Cr >= -4.5652 * Cb + 234.5652
	i4 = Cr <= -1.15 * Cb + 301.75
	i5 = Cr <= -2.2857 * Cb + 432.85
	return (i1 and i2 and i3 and i4 and i5)

def isSkinByHSV(H, S, V):
	return (H < 25) or (H > 230);

def skinOnly(srcFile, destFile):
	src = cv2.imread(srcFile)
	ycrcb = cv2.cvtColor(src, cv2.COLOR_BGR2YCR_CB)
	hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
	for i in range(src.shape[0]):
		for j in range(src.shape[1]):
			if not isSkinByRGB(src[i][j][2], src[i][j][1], src[i][j][0]) or not isSkinByYCrCb(ycrcb[i][j][0], ycrcb[i][j][1], ycrcb[i][j][2]) or not isSkinByHSV(hsv[i][j][0], hsv[i][j][1], hsv[i][j][2]) :
			#if not isSkinByRGB(src[i][j][2], src[i][j][1], src[i][j][0]) or not isSkinByHSV(hsv[i][j][0], hsv[i][j][1], hsv[i][j][2]):
			#if not isSkinByRGB(src[i][j][2], src[i][j][1], src[i][j][0]):
				src[i,j] = 0
	cv2.imwrite(destFile, src)


def skinDetect(srcFile, destFile):
	"""
	简单的实现
	"""
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
			#skinDetect(os.path.join(options.src, file), os.path.join(options.dir, file))
			skinOnly(os.path.join(options.src, file), os.path.join(options.dir, file))
			#print os.path.join(options.src, file), "   ", os.path.join(options.dir, file)
			#exit()
			index += 1
	print "total size: ", index
