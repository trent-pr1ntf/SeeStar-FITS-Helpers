# SeeStar-FITS-Helpers
Programmatically do stuff with FITS data. 

fits-total-time.py - Input a FITS file and output the total exposure time used in stacking

fits-exposure-sum.py - Input a working directory with a "lights" directory in it and total the number of light files and count all of the exposure/integration time. 

seestar-filter-sort.py - Input a directory with a bunch of mixed IRCUT and LP filter data for a single object, and separate them out into directories based on filters. 

seestar-sort-and-count.py - Input a directory full of light data, and it will automatically sort into directories based on filters used, and then count the exposure time. Made to be used everytime data is added to an object's folder. 
