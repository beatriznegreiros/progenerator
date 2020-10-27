# progenerator

Repository with routines to generate river profiles for numerical model evaluation and bathymetry change analsys.


## Capabilities

The module ``profiles_generator.py`` can plot hundreds of profiles automatically having as input file the following:
- The limits of the right and left bank in .csv format.
- The bed elevation profiles in .csv format, the input .csv must be in the following format:
	- 1st column: Section (river chainage) to which the point belongs
	- 2nd column: Latitude
	- 3rd column: Longitude
	- 4th column: Bed elevation


## Quick start

The easiest way to use ``progenerator`` is to clone this GitHub repository and open the standalone code ``progenerator.py``; the method profiles_generator takes as input the following:

- In ``path_banks`` insert the name of the file which contains the points of the right and left banks.
- In ``list_of_profiles`` insert the name of the files which you want to be part of the sections plots. Important: leave out
the file extension. Please note: the files should be in the same folder as the code.
- Note: If your files have headers either delete it or entry it at the variable ``header`` at the INPUT block.
- In ``marker_size`` insert the size of the markers of each of the respective files
- For plotting with different marker types, change the list ``marker`` according to your preferences. Marker types can be 
found [here](https://matplotlib.org/3.1.1/api/markers_api.html)
- ``x-`` and ``yspacing`` can be float of int; they are the spacing for the x and y labels.
- At the argument ``titles`` one can insert the identifier to each respective data set (it will appear on the final plots)
- Finally, choose the path of the folder which will store all profile images in ``name_output_folder``. The folder will be automatically
created inside the selected directory.

	
## Dependencies
``progenerator.py`` is a pure Python code. The following packages are dependencies of this repository:
- numpy
- pandas
- matplotlib
- pathlib

Navigate with ``anaconda prompt`` to the the cloned repository and type ``conda env create -f environment.yml`` to create a conda environment with the above necessary packages.


