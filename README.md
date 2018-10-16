# ImageComparisonTool
Simple tool for image comparison using pixel values

1. Requires a folder/directory of .jpg images named "images" in the same location as PixInfo.py and ImageViewer.py
2. PixInfo.py class processes each image as follows - 
  a. Creates a flat array of pixels
  b. Extracts a 6-bit Color Code for each pixel by combining the two most significant bits of each pixel value (R, G, B)
  c. Extracts the Intensity of each pixel according to the following function - Intensity = (.299*r)+(.587*g)+(.114*b) 
  d. Creates an array of bins 64 for the Color Code and increments the corresponding bin for each represented Color Code
  e. Creates an array of 25 bins for Intensity and increments the corresponding bin as follows - 0-9, 10-19 ... 230-239, 240-255 
3. ImageViewer.py contains the main class, instantiates the GUI, and processes image comparison on command
  a. Tkinter and Tkinter.ttk used for the GUI
  b. Each images corresponding bins are compared to the target images bins using Manhattan distance 
    and drawn onto a tabbed results page
  c. The target image distance is calculated once and stored on the local stack for comparing to each image
