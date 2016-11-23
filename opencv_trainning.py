#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys
import shutil
from optparse import OptionParser

POSTIVE_FILE = "pos.txt"
NEGTIVE_FILE = "neg.txt"
POSTIVE_VEC = "pos.vec"
POSTIVE_NUM = 2000
NEGTIVE_NUM = 4000
FEATURE_TYPE = 'LBP' # 'HOG', 'LBP', 'HAAR'
BOOST_TYPE = 'GAB'  # 'LB', 'GAB', 'RAB', 'DAB'
DATA_FOLDER = 'data'

def createSample(dir, postive, fileName, width = 0, height = 0):
    if postive:
        os.system('find %s -name "*.jpg" -exec echo {} 1 0 0 %s %s \; > %s ' % (dir, width, height, fileName))
    else:
        os.system('find %s -name "*.jpg" > %s ' % (dir, fileName))
    return int(os.popen('find %s -name "*.jpg" | wc -l' % dir).read())

def createSampleList(dir, postive, fileName, width = 0, height = 0):
	dataFile = open(fileName, 'w')
	index = 0
	for file in os.listdir(dir):
		if file.endswith('jpg'):
			if postive:
				dataFile.writelines("%s 1 0 0 %s %s \r\n" % (os.path.join(dir, file), width, height))
			else:
				dataFile.writelines(os.path.join(dir, file) + "\r\n")
			index += 1
	dataFile.close()
	return index

def cleanParam():
	#if os.path.exists(DATA_FOLDER): shutil.rmtree(DATA_FOLDER)
	if os.path.exists(DATA_FOLDER): os.system("rm %s -rf" % DATA_FOLDER)
	if os.path.exists(POSTIVE_FILE): os.remove(POSTIVE_FILE)
	if os.path.exists(POSTIVE_VEC): os.remove(POSTIVE_VEC)
	if os.path.exists(NEGTIVE_FILE): os.remove(NEGTIVE_FILE)

if __name__ == "__main__":
	parser = OptionParser(version = "v0.1")
	parser.add_option("-n", "--negtive", dest="negtive", help="the negtive sample folder", metavar="DIRECTORY")
	parser.add_option("-p", "--postive", dest="postive", help="the postive sample folder", metavar="DIRECTORY")
	parser.add_option("-d", "--data", dest="data", help="the train result folder", default=DATA_FOLDER, metavar="INT")
	parser.add_option("-w", "--width", dest="width", type='int', help="the sample image width", metavar="INT")
	parser.add_option("-l", "--height", dest="height", type='int', help="the sample image height", metavar="INT")
	parser.add_option("-s", "--stages", dest="stages", type='int', help="training stage count", metavar="INT")
	parser.add_option("-c", "--clean", action="store_true", default=False, dest="clean", help="clean all paramenter")
	(options, args) = parser.parse_args()
	if options.clean:
		cleanParam()
		if len(sys.argv) <= 2:
			os._exit(0)
	if options.negtive is None or os.path.isdir(options.negtive) == False:
		print "can not find the negtive samples' directory..."
		sys.exit(-1)
	if options.postive is None or os.path.isdir(options.postive) == False:
		print "can not find the postive samples' directory..."
		sys.exit(-1)
	if options.stages is None:
		print "the training stages is None.."
		sys.exit(-1)
	if options.width is None:
		print "the sample width is None.."
		sys.exit(-1)
	if options.height is None:
		print "the sample height is None.."
		sys.exit(-1)
	print "the training param data directory is ", options.data
	if not os.path.exists(options.data):
	    os.makedirs(options.data)
	num = createSample(options.negtive, False, NEGTIVE_FILE)
	print 'the neg sample count is %d ...' % num
	num = createSample(options.postive, True, POSTIVE_FILE, options.width, options.height)
	#shutil.move(POSTIVE_FILE, os.path.join(options.postive, POSTIVE_FILE))
	print 'the pos sample count is %d ...' % num
	command = 'opencv_createsamples -info {0} -vec {1} -num {2} -w {3} -h {4} -bg {5}'.format(POSTIVE_FILE, POSTIVE_VEC, num, options.width, options.height, NEGTIVE_FILE)
	print "current path: ", os.getcwd()
	print "start run command : ", command
	os.system(command)
	command = 'opencv_traincascade -data {0} -vec {1} -bg {2} -numPos {3} -numNeg {4} -bt {5} -featureType {6} -w {7} -h {8} -numStages {9} -maxFalseAlarmRate 0.1'
	command = command.format(options.data, POSTIVE_VEC, NEGTIVE_FILE, POSTIVE_NUM, NEGTIVE_NUM, BOOST_TYPE, FEATURE_TYPE, options.width, options.height, options.stages)
	print "start run command : ", command
	os.system(command)
