import numpy as np
from pathlib import Path

current_dir = Path.cwd()
filename = 'Inn_Querprofile_GKZone_DHHN12_2020'  # OBS: not file extension!!

pathfile = str(current_dir) + '/' + filename + '.csv'
data = np.genfromtxt()
