import numpy as np
from pathlib import Path

current_dir = Path.cwd()
filename = 'Inn_Querprofile_GKZone_DHHN12_korr_2' # OBS: not file extension!!

pathfile = str(current_dir) + '/' + filename + '.csv'

data = np.genfromtxt(pathfile,  delimiter="_")
print(data)

cut_array = np.empty(np.shape(data[:, 1]), dtype=np.float)

for i, entry in np.ndenumerate(data[:, 1]):
    cut_array[i[0]] = entry/1000

np.savetxt('Queprofile_2020_korr.csv', cut_array, delimiter=',')
