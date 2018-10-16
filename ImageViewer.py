# Ben Pittman
# UW-Bothell CSS 584
# Autumn 2018


from tkinter import *
from tkinter.ttk import *
import math, os
from PixInfo import PixInfo

# Main app.
class ImageViewer(Frame):
    
    # Constructor.
    def __init__(self, master, pixInfo, resultWin):
        
        Frame.__init__(self, master)
        self.master    = master
        self.pixInfo   = pixInfo
        self.resultWin = resultWin
        self.colorCode = pixInfo.get_colorCode()
        self.intenCode = pixInfo.get_intenCode()
        # Full-sized images.
        self.imageList = pixInfo.get_imageList()
        # Thumbnail sized images.
        self.photoList = pixInfo.get_photoList()
        # Image size for formatting.
        self.xmax = pixInfo.get_xmax()
        self.ymax = pixInfo.get_ymax()
        self.imgFilename = []
        for i in range(len(self.imageList)):
            self.imgFilename.append(self.imageList[i].filename)
        self.images_per_page = 20

        # Create Main frame.
        mainFrame = Frame(master)
        mainFrame.pack()
        listFrame = Frame(mainFrame)
        listFrame.pack(side=LEFT)
        
        # Create Control frame.
        controlFrame = Frame(mainFrame)
        controlFrame.pack(side=RIGHT)

        # Create Preview frame.
        previewFrame = Frame(mainFrame, 
            width=self.xmax+45, height=self.ymax)
        previewFrame.pack_propagate(0)
        previewFrame.pack(side=RIGHT)

        # Create Results frame.
        self.note = Notebook(self.resultWin)
        self.tabs = []
        self.pages = int(math.ceil(len(self.imageList) / self.images_per_page))
        
        
        # Layout Picture Listbox.
        self.listScrollbar = Scrollbar(listFrame)
        self.listScrollbar.pack(side=RIGHT, fill=Y)
        self.list = Listbox(listFrame, 
            yscrollcommand=self.listScrollbar.set, 
            selectmode=BROWSE, 
            height=10)
        for i in range(len(self.imageList)):
            self.list.insert(i, self.imageList[i].filename)
        self.list.pack(side=LEFT, fill=BOTH)
        self.list.activate(1)
        self.list.bind('<<ListboxSelect>>', self.update_preview)
        self.listScrollbar.config(command=self.list.yview)

        # Layout Controls.
        button = Button(controlFrame, text="Inspect Pic",
            command=lambda j=self.list.get(ACTIVE) : self.inspect_pic(j))
        button.grid(padx=10, row=0, sticky=E)
        
        self.b1 = Button(controlFrame, text="Color-Code",
            command=lambda : self.find_distance(method='CC'))
        self.b1.grid(padx=10, row=1, sticky=E)
        
        self.b2 = Button(controlFrame, text="Intensity",
            command=lambda : self.find_distance(method='Inten'))
        self.b2.grid(padx=10, row=2, sticky=E)
        
        
        # Layout Preview.
        self.selectImg = Label(previewFrame, image=self.photoList[0])
        self.selectImg.pack()
    
    
    # Event "listener" for listbox change.
    def update_preview(self, event):
        i = self.list.curselection()[0]
        self.selectImg.configure(
            image=self.photoList[int(i)])
    
    
    # Find the Manhattan Distance of each image and return a
    # list of distances between image i and each image in the
    # directory uses the comparison method of the passed 
    # binList
    def find_distance(self, method):
        # Get the target comparison image and the method comparison list
        master_comp_bins = self.colorCode if method == 'CC' else self.intenCode
        i = self.list.curselection()[0]
        target_img = self.imageList[int(i)]
        target_img_comp = master_comp_bins[int(i)]

        # Create a list of the target images factor in the distance calculation
        target_img_bin_distance_list = []
        for bin_num in target_img_comp:
            target_img_bin_distance_list.append(bin_num / target_img.size[0] * target_img.size[1])

        # Calculate distance between each image and the comparison image
        img_distance_list = []
        for img_num in range(len(self.imageList)):
            distance = 0
            image = self.imageList[img_num]
            comp_bins = master_comp_bins[img_num]
            for bin_num in range(len(target_img_comp)):
                distance += abs(target_img_bin_distance_list[bin_num] -
                                (comp_bins[bin_num] / image.size[0] * image.size[1]))

            img_distance_list.append(distance)

        # Create new list copy of photoList with images in descending order by distance from target and pass
        # to update_results method including the image root filename
        unSortedList = list(zip(img_distance_list, self.imgFilename, self.photoList))
        sortedList = sorted(unSortedList, key=lambda pair: pair[0])
        sortedTup = [element[1:] for element in (tuple(x) for x in sortedList)]

        self.update_results(sortedTup)

    # Update the results window notebook with the sorted results.
    def update_results(self, sortedTup):
        cols = math.ceil(math.sqrt(self.images_per_page))

        # Ensure results window is blank to start and rebuild
        self.note.destroy()
        self.note = Notebook(self.resultWin)
        del self.tabs[:]
        self.tabs = []
        self.pages = int(math.ceil(len(self.imageList) / self.images_per_page))

        # iterate over the notebook pages and place images
        for n in range(self.pages):
            newFrame = Frame(self.note)
            photoRemain = sortedTup[(n * self.images_per_page): ((n + 1) * self.images_per_page)]
            rowPos = 0
            # place images on a frame and add frame to the notebook
            while photoRemain:
                photoRow = photoRemain[:cols]
                photoRemain = photoRemain[cols:]
                colPos = 0
                for (filename, img) in photoRow:
                    link = Button(newFrame, image=img, text=filename.strip('images\\.jpg'), compound=TOP)
                    handler = lambda f=filename: self.inspect_pic(f)
                    link.config(command=handler)
                    link.grid(column=colPos, row=rowPos, padx=self.xmax - img.width(), pady=self.ymax - img.height(),
                              ipadx=img.width() // 2, ipady=img.height() // 2, sticky=NW)
                    colPos += self.xmax

                rowPos += self.ymax

            self.tabs.append(newFrame)
            self.note.add(self.tabs[n], text="Image Result Set {} of {}".format(n + 1, self.pages))

        self.note.pack()
    
    # Open the picture with the default operating system image
    # viewer.
    def inspect_pic(self, filename):
        
        os.startfile(filename)


# Executable section.
if __name__ == '__main__':

    root = Tk()
    root.title('Image Analysis Tool')

    resultWin = Toplevel(root)
    resultWin.title('Result Viewer')
    resultWin.protocol('WM_DELETE_WINDOW', lambda: None)

    pixInfo = PixInfo(root)

    imageViewer = ImageViewer(root, pixInfo, resultWin)

    root.mainloop()

