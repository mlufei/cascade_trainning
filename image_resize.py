#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import os,sys  
from PIL import Image
from optparse import OptionParser

def thumbnail(src, dest, size):
        try:
                image = Image.open(src)
		image.thumnail(size, Image.ANTIALIAS)
		image.save(dist, "JPEG")
	except IOError:
		print "can not create thumbnail for '%s'" % src

def resizeImage(image, w, h):
	sWidth, sHeight = image.size
	factor = min(1.0 * w / sWidth, 1.0 * h / sHeight)
	width = int(sWidth * factor)
	height = int(sHeight * factor)
	return image.resize((w, h), Image.ANTIALIAS)

def resize(src, dest, w, h):
    try:
        image = Image.open(src)
        width, height = image.size
        if not w is None:
            width = int(w)
        if not h is None:
            height = int(h)
        dimage = resizeImage(image, width, height)
        #print "image resized from (%d, %d)" % image.size, " to (%d, %d)" % dimage.size
        dimage.save(dest, "JPEG")
    except IOError:
        print "can't resize the image which path is %s" % src

if __name__ == "__main__":
	parser = OptionParser(version = "v0.1")
	parser.add_option("-s", "--src", dest="src", help="the src images' path", metavar="DIRECTORY")
	parser.add_option("-d", "--dir", dest="dir", help="the dir images' path", metavar="DIRECTORY")
	parser.add_option("-w", "--width", dest="width", help="the image's window box width",
			metavar="INT")
	parser.add_option("-l", "--height", dest="height", help="the image's window box height",
			metavar="INT")
	(options, args) = parser.parse_args()
	if os.path.isdir(options.src) == False:
		print "can not find the ", options.src, " directory..."
		sys.exit(-1) 
	if os.path.exists(options.dir) == False:
		os.makedirs(options.dir)
	
	index = 0
	print "start resize all images in '%s' floder by the window which size is (%s, %s)" % (options.src, options.width, options.height)
	for file in os.listdir(options.src):
		if file.endswith("jpg"):
			resize(os.path.join(options.src, file), os.path.join(options.dir, file), options.width,
					options.height)
			#print os.path.join(options.src, file), "   ", os.path.join(options.dir, file)
			#exit()
			index += 1
	print "total size: ", index
