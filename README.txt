OpenCV Cascade Trainning
========

To train the cascade model easily, we write this tool as python. You can train any object you want, just puting the samples in the negdata/posdata folder, and then run as below:

```
    $ chmod a+x opencv_trainning.py 
    $ ./opencv_trainning.py -n negdata -p posdata -w 20 -l 20 -s 8
```

and you can use the -h option to get the help informations.

```
    $ ./opencv_trainning.py -h
```

Resize the image
=======
You can use the image_resize.py to resize image file like below:

```
    $ image_resize.py -s from/ -d to/ -w 20 -l 20
```

