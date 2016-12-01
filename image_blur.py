#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys
from PIL import Image
from optparse import OptionParser
import cv2

def filter2D(srcFile, destFile):
	"""
	将和模板放在图像的一个像素A上，求与之对应的图像上的每个像素点的和，核不同，得到的结果不同，而滤波的使用核心也是对于这个核模板的使用，需要注意的是，该滤波函数是单通道运算的，也就是说对于彩色图像的滤波，需要将彩色图像的各个通道提取出来，对各个通道分别滤波才行。 
	"""
	src = cv2.imread(srcFile)
	# blur kernel
	# kernel = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
	# shark kernel
	kernel = np.array([[1,0,0],[0,1,0,0,0],[0,0,1,0,0],[0,0,0,1,0],[0,0,0,0,1]])
	dest = cv2.filter2D(src, -1, kernel)
	cv2.imwrite(destFile, dest)

def blur(srcFile, destFile):
	"""
	上述生成的5*5核模板其实就是一个均值滤波。而opencv有一个专门的平均滤波模板供使用–归一化卷积模板，所有的滤波模板都是使卷积框覆盖区域所有像素点与模板相乘后得到的值作为中心像素的值。Opencv中均值模板可以用cv2.blur和cv2.boxFilter,
	"""
	src = cv2.imread(srcFile)
	dest = cv2.blur(src, (3, 5))
	cv2.imwrite(destFile, dest)

def gaussianBlur(srcFile, destFile):
	"""
	现在把卷积模板中的值换一下，不是全1了，换成一组符合高斯分布的数值放在模板里面，比如这时中间的数值最大，往两边走越来越小，构造一个小的高斯包。实现的函数为cv2.GaussianBlur()。对于高斯模板，我们需要制定的是高斯核的高和宽（奇数），沿x与y方向的标准差(如果只给x，y=x，如果都给0，那么函数会自己计算)。高斯核可以有效的出去图像的高斯噪声。
	"""
	src = cv2.imread(srcFile)
	dest = cv2.GaussianBlur(src, (5, 5), 0)
	cv2.imwrite(destFile, dest)

def medianBlur(srcFile, destFile):
	"""
	中值滤波模板就是用卷积框中像素的中值代替中心值，达到去噪声的目的。这个模板一般用于去除椒盐噪声。前面的滤波器都是用计算得到的一个新值来取代中心像素的值，而中值滤波是用中心像素周围（也可以使他本身）的值来取代他，卷积核的大小也是个奇数。
	"""
	src = cv2.imread(srcFile)
	dest = cv2.medianBlur(src, 5)
	cv2.imwrite(destFile, dest)

def bilateralFilter(srcFile, destFile):
	"""
	该滤波器可以在保证边界清晰的情况下有效的去掉噪声。它的构造比较复杂，即考虑了图像的空间关系，也考虑图像的灰度关系。双边滤波同时使用了空间高斯权重和灰度相似性高斯权重，确保了边界不会被模糊掉。
	"""
	src = cv2.imread(srcFile)
	dest = cv2.bilateralFilter(src, 9, 75, 75)
	cv2.imwrite(destFile, dest)

if __name__ == "__main__":
	parser = OptionParser(version = "v0.1")
	parser.add_option("-s", "--src", dest="src", help="the src images' path", metavar="DIRECTORY")
	parser.add_option("-d", "--dir", dest="dir", help="the dir images' path", metavar="DIRECTORY")
	parser.add_option("-f", "--filter", dest="filter", default="box", help="the images' filter: filter2D, box, median, gaussian, bilateral", metavar="blur")
	(options, args) = parser.parse_args()
	if os.path.isdir(options.src) == False:
		print "can not find the ", options.src, " directory..."
		sys.exit(-1)
	if os.path.exists(options.dir) == False:
		os.makedirs(options.dir)

	index = 0
	print "start blur all images in '%s' floder with %s ..." % (options.src, options.filter)
	for file in os.listdir(options.src):
		if file.endswith("jpg"):
			if options.filter is "filter":
				filter2D(os.path.join(options.src, file), os.path.join(options.dir, file))
			elif options.filter is "box":
				blur(os.path.join(options.src, file), os.path.join(options.dir, file))
			elif options.filter is "median":
				medianBlur(os.path.join(options.src, file), os.path.join(options.dir, file))
			elif options.filter is "gaussian":
				gaussianBlur(os.path.join(options.src, file), os.path.join(options.dir, file))
			elif options.filter is "bilateral":
				bilateralFilter(os.path.join(options.src, file), os.path.join(options.dir, file))
			#print os.path.join(options.src, file), "   ", os.path.join(options.dir, file)
			#exit()
			index += 1
	print "total size: ", index
