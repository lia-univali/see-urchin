<img src="https://i.imgur.com/17AceWx.png" width="300">

# See_Urchin

A tool made in Python that detects and measures the size of _Paracentrotus lividus_ in its different evolutionary stages.  
The tool analyzes pictures, extrapolates the larvaes/eggs and uses [a neural network](https://uber.github.io/ludwig/) to detect the different stages of the evolutionary process.

## Scripts
#### getLarvae.py

This is the main file. It extracts the images; applies the image processing techniques; classifies the larvae; saves the individual larvae images (as .jpg) and builds a report. Its usage depends on the directory the user provides in the ```filename``` variable and the images must be numbered from 0 to the ```numberOfImages``` variable value. The destination folder can also be modified by changing the ```pathName``` variable.

#### imgClass.py

This file has the image processing functions in them bundled within a convenient class that allows for easy and intuitive image manipulation.

#### larvaeFunc.py

This file has the larvae-oriented functions in it, which are mainly for extracting the information from the processed images.

#### report.py

This file has the functions that write in the ```report.html``` file.

## Other Files

#### report.html

This file displays the larvae images and their information organizedly.

<img src="https://i.imgur.com/0i2sTtE.png">

#### Images

The larvae images must follow this model:

<img src="https://i.imgur.com/U60LPum.png" width=200>

Any image that doesnt have **dark** larvae on a **bright** background most likely won't work.

## Dependencies

● [Python](https://www.python.org/downloads/);  
● [OpenCV](https://pypi.org/project/opencv-python/);  
● [Numpy](https://pypi.org/project/numpy/);  
● [Ludwig](https://uber.github.io/ludwig/);  
● [Pandas](https://pypi.org/project/pandas/).

Scripts developed by Davi Mello, student of UNIVALI and participant of the LIA team.
