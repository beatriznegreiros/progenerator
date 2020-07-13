# progenerator

Repository with routines to generate river profiles for numerical model evaluation and bathymetry change analsys.


## Capabilities

The module ``profiles_generator.py`` can plot hundreds of profiles automatically having as input file the following:
- The limit of the right and left bank in .csv format.
- The bed elevation profiles in .csv format, the input .csv must be in the following format:
	- 1st column: Section (river chainage) to which the point belongs
	- 2nd column: Latitude
	- 3rd column: Longitude
	- 4th column: Bed elevation


## User's manual

The safest way to use ``progenerator`` is to clone this GitHub repository and open the file ``profiles_generator``, there
you will find a code block with name INPUT.

- In ``list_of_profiles`` insert the name of the files which you want to be part of the sections plots. Important: leave out
the file extension. Please note: the files should be in the same folder as the code.
- In ``bank_limits`` insert the name of the file which contains the points of the right and left banks.
- In ``marker_size`` insert the size of the markers of each of the respective files
- For plotting with different marker types, change the list ``marker`` accoridng to your preferences. Marker types can be 
found [here](https://matplotlib.org/3.1.1/api/markers_api.html)
- Finally, choose the name of the folder which will store all profile images in ``name_output_folder``. The folder will be automatically
created inside the current directory.


	
	