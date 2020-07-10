import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

current_dir = Path.cwd()

# ------------- INPUT (without extension of file) -------------------
list_of_profiles = ['Inn_Profile_2014', 'QP_2007_Fkm', 'Querprofile_2020_final']  # Profiles must be in same folder

markersize = [8, 4, 0]  # corresponding to the respective profiles
marker = [".", "^", "."]  # corresponding to the respective profiles

# (km section, lat, long, bed elevation) obs.: first column is always 0
output_folder = str(current_dir) + '/' + 'Inn_Profiles_2014_2007_2020'
# -------------------------------------------------------------------

# Create folder if it doesnt exist
Path(output_folder).mkdir(exist_ok=True)


# Practical Routines
def rename_columns(df):
    header = {df.columns[0]: 'lat', df.columns[1]: 'long', df.columns[2]: 'bedelevation'}
    df = df.rename(columns=header)
    return df


def split_float(x):
    before, after = str(x).split('.')
    return int(before), (int(after) * 10 if len(after) == 1 else int(after))


# Read Stamm punkte
path_banks = str(current_dir) + '/' + 'Inn_Stamm_2014.csv'  # Path to stamm punkte
corners = pd.read_csv(path_banks, skip_blank_lines=True, index_col=0, header=None)
corners.dropna(how='any', inplace=True, axis=0)
corners = rename_columns(corners)  # Standardize columns names

# Take list of all km sections
stamm_profiles = corners.index.drop_duplicates()

# Iterates through km sections
for sec in stamm_profiles:
    i=0
    for _file in list_of_profiles:
        path_profile = str(current_dir) + '/' + _file + '.csv'

        # Take the Stamm Punkte
        reference_banks = corners.loc[sec]

        # Read the DataFrame
        profile = pd.read_csv(path_profile, skip_blank_lines=True, index_col=0, header=None)
        profile.dropna(how='any', inplace=True, axis=0)

        # Standardize the columns
        profile = rename_columns(profile)

        try:  # tries to take section (if it exist in the dataset)

            # Take only points of the km (sec)
            points_in_section = profile.loc[sec]

            # Calculate the pitagoras of lat and long
            distances = (points_in_section.lat ** 2 + points_in_section.long ** 2) ** 0.5
            references = np.array((reference_banks.lat ** 2 + reference_banks.long ** 2) ** 0.5)

            # Boolan array to take only points inside the stamm punkte
            isinside = (distances <= references[1]) & (distances >= references[0]) | ((distances <= references[0])
                                                                                      & (distances >= references[1]))

            # Re-assign dataframes to take only points inside stammpunkte
            distances = distances[isinside]
            points_in_section = points_in_section[isinside]

            # Calculates the relative distance of the bathymetry having as reference point the left bank
            distances = abs(distances - references[0])
            references = abs(references - references[0])

            # Plots the km section
            plt.plot(distances, points_in_section.bedelevation, marker=marker[i],
                     markerfacecolor='black', markersize=markersize[i], label=_file)

            plt.legend(loc='upper center')

            # plt.scatter(references, reference_banks.bedelevation, marker="^", edgecolors='c', label='Stamm Punkte')
            i +=1
        except:  # skips the plot if the section doesnt exist
            message = "Could not save plot for " + _file + " in km section " + str(sec)
            print(message)
            pass

    # Get title and path of the section figure
    integer, decimal = split_float(sec)
    title = 'Cross section of km ' + str(sec)
    plt.xlabel('Distance from left bank [m]')
    plt.ylabel('Elevation [m.a.s.l]')
    plt.title(title)
    out = output_folder + '/' + 'km_' + str(integer) + '_' + str(decimal)

    # Save figure
    plt.savefig(out)
    plt.clf()
