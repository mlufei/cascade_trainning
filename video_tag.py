#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys
from PIL import Image
from optparse import OptionParser
import cv2

IMAGE_DEFAULT_FOLDER = "images"

def saveTagList(tagList, destFile):
	"""
	save the tag list into a file
	"""
	tagFile = open(destFile, "w")
	for key in tagList.keys():
		tagFile.write("%s" % (key))
		for rect in tagList[key]:
			tagFile.write(",%s-%s-%s-%s" % rect)
		tagFile.write("\r\n")
	tagFile.close()

def getTagList(tagListFile):
	"""
	parse the tag list from file
	Rect: index, size, left, top, width, height,...
	"""
	tagFile = open(tagListFile)
	tagList = {}
	for line in tagFile.readlines():
	        if not line.strip():
			continue
	        tags = line.split(",")
	        if len(tags) <= 0:
			continue
	        tagList[int(tags[0])] = []
	        length = int(tags) - 1
        	for index in range(length):
			rect = tags[index + 1].split("-")
			if len(rect) < 4:
				continue
			tagList[int(tags[0])].append((int(rect[0]), int(rect[1]), int(rect[2]), int(rect[3])))
	tagFile.close()
	return tagList

def imageTag(frame, tags):
	color = (0,255,0)
	for rect in tags:
		cv2.rectangle(frame, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), color,5)

def videoTag(videoIn, videoOut, tagList):
	"""
	get frames from video, and add some tags into the every frame, then save into the videoOut
	"""
	videoCapture = cv2.VideoCapture(videoIn)
	fps = videoCapture.get(cv2.CAP_PROP_FPS)
	size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
	videoWriter = cv2.VideoWriter(videoOut, cv2.cv.CV_FOURCC('M', 'J', 'P', 'G'), fps, size)
	success, frame = videoCapture.read()
	index = 0
	while success:
		cv2.imshow('video', frame)
		if(cv2.waitKey(0)==27):
			cv2.destroyAllWindows()
			break
		index += 1
		imageTag(frame, tagList[index])
		videoWriter.write(frame)
		cv2.imshow('video', frame)
		success, frame = videoCapture.read()

def videoDetectTag(videoIn, videoOut, cascade, folder):
	"""
	get frames from video, and add some tags into the every frame, then save into the videoOut
	"""
	videoCapture = cv2.VideoCapture(videoIn)
	fps = videoCapture.get(cv2.CAP_PROP_FPS)
	size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
	videoWriter = cv2.VideoWriter(videoOut, cv2.cv.CV_FOURCC('M', 'J', 'P', 'G'), fps, size)
	success, frame = videoCapture.read()
	index = 0
	while success:
		cv2.imshow('src', frame)
		if(cv2.waitKey(0)==27):
			cv2.destroyAllWindows()
			break
		index += 1
		imageTag(frame, tagList[index])
		videoWriter.write(frame)
		cv2.imshow('dest', frame)
		success, frame = videoCapture.read()

if __name__ == "__main__":
	parser = OptionParser(version = "v0.1")
	parser.add_option("-s", "--src", dest="src", help="video src file", metavar="FILE")
	parser.add_option("-d", "--dest", dest="dest", help="video dest file", metavar="FILE")
	parser.add_option("-c", "--cascade", dest="cascade", help="cascade file", metavar="FILE")
	parser.add_option("-f", "--folder", dest="folder", help="image folder", metavar="DIRECTORY")
	parser.add_option("-t", "--tag", dest="tag", help="video tag list file", metavar="FILE")
	(options, args) = parser.parse_args()
	if os.path.exists(options.src) == False:
		print "can not find the ", options.src, " file(src)..."
		sys.exit(-1)
	if os.path.exists(options.dest) == False:
		print "can not find the ", options.dest, " file(dest)..."
		sys.exit(-1)
	if os.path.exists(options.cascade) == False:
		print "can not find the ", options.cascade, " file(cascade)..."
		sys.exit(-1)
	if (not os.path.exists(options.tag)):
		print "can not find the ", options.tag," file(tag)..."
		sys.exit(-1)
	if options.folder is None:
		options.folder = IMAGE_DEFAULT_FOLDER
	if not os.path.exists(options.folder):
		os.makedirs(options.folder)
	if os.path.exists(options.tag):
		tagList = getTagList(options.tag)
		videoTag(options.src, options.dest, tagList)
	else:
		tagList = videoDetectTag(options.src, options.dest, options.cascade, options.folder)
		saveTagList(tagList, options.tag)
