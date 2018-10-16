# Ben Pittman
# UW-Bothell CSS 584
# Autumn 2018
# Requires a set of .jpg images in folder named images

from PIL import Image
from PIL import ImageTk
import glob, os


# Pixel Info class.
class PixInfo:
    
    # Constructor.
    def __init__(self, master):
    
        self.master = master
        self.imageList = []
        self.photoList = []
        self.xmax = 0
        self.ymax = 0
        self.colorCode = []
        self.intenCode = []
        
        # Add each image (for evaluation) into a list, 
        # and a Photo from the image (for the GUI) in a list.
        for infile in glob.glob('images/*.jpg'):
            
            file, ext = os.path.splitext(infile)
            im = Image.open(infile)
            
            
            # Resize the image for thumbnails.
            imSize = im.size
            x = imSize[0]//4
            y = imSize[1]//4
            imResize = im.resize((x, y), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(imResize)

            # Find the max height and width of the set of pics.
            if x > self.xmax:
              self.xmax = x
            if y > self.ymax:
              self.ymax = y
            
            
            # Add the images to the lists.
            self.imageList.append(im)
            self.photoList.append(photo)


        # Create a list of pixel data for each image and add it
        # to a list.
        for im in self.imageList[:]:
            
            pixList = list(im.getdata())
            CcBins, InBins = self.encode(pixList)
            self.colorCode.append(CcBins)
            self.intenCode.append(InBins)


    # Bin function returns an array of bins for each
    # image, both Intensity and Color-Code methods.
    def encode(self, pixList):

        # array initilazation for bins, initialized
        # to zero.
        CcBins = [0] * 64
        InBins = [0] * 25
        

        # loop over image pixels, extract information for each pixel and add to respective array
        for pixel in pixList:
            (R, G, B) = pixel

            # extract intensity of each pixel with the given method and convert to appropriate bin number
            # and increment appropriate bin
            intensitysum = int((.299 * R) + (.587 * G) + (.114 * B))
            binnum = (intensitysum // 10) if (intensitysum // 10) < 25 else 24

            # Convert each pixel integer to binary string, extract two left most 'bits' for each color code and
            # combine to create a '6-bit' string, convert back to integer and increment appropriate bin
            binaryR = bin(R)
            binaryR = binaryR[2:].zfill(8)
            binaryG = bin(G)
            binaryG = binaryG[2:].zfill(8)
            binaryB = bin(B)
            binaryB = binaryB[2:].zfill(8)
            binarySum = binaryR[:2] + binaryG[:2] + binaryB[:2]

            CcBins[int(binarySum, 2)] += 1
            InBins[binnum] += 1

        # Return the list of binary digits, one digit for each
        # pixel.
        return CcBins, InBins
    
    
    # Accessor functions:
    def get_imageList(self):
        return self.imageList
    
    def get_photoList(self):
        return self.photoList
    
    def get_xmax(self):
        return self.xmax
    
    def get_ymax(self):
        return self.ymax
    
    def get_colorCode(self):
        return self.colorCode
        
    def get_intenCode(self):
        return self.intenCode
    
    
