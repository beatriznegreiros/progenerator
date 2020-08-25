try:
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from pathlib import Path
    import matplotlib.ticker as ticker
except:
    print('ModuleNotFoundError: Missing fundamental packages (required: numpy, pandas and matplotlib')


# Practical Routines
def rename_columns(df):
    header = {df.columns[0]: 'lat', df.columns[1]: 'long', df.columns[2]: 'bedelevation'}
    df = df.rename(columns=header)
    return df


def split_float(x):
    before, after = str(x).split('.')
    return int(before), (int(after) * 10 if len(after) == 1 else int(after))


def profiles_generator(path_banks, list_of_profiles, header, markersize, marker, titles, output_folder, xspacing,
                       yspacing, delete_outside=None):
    """
    :param path_banks: str, text file in *.csv format, file which delimits the points inside a river profile
    :param list_of_profiles: list of str, text files in *.csv format for the profiles to be generated
    :param header: None or integer, number of lines where the input data has headers
    :param markersize: list of str, markersizes to the respective profiles
    :param marker: list of str, markers to the respective profiles
    :param titles: list of str, titles as identifiers for each dataset appering in the plots
    :param output_folder: folder to which save the generated images
    :param xspacing: float or int, spacing for the x labels
    :param yspacing: float or int, spacing for the y labels
    #TODO under construction:
    :kwarg plot_beyond_until: float, distance beyond the most extreme points (right and left bank) of one chosen
    reference profile ('from_profile') to which plot all points inside it.
    :kwarg from_profile: str, referred to plot_beyond_until

    :output: saves images of every section for all list_of_profiles
    """

    corners = pd.read_csv(path_banks, skip_blank_lines=True, index_col=0, header=None)
    corners.dropna(how='any', inplace=True, axis=0)
    corners = rename_columns(corners)  # Standardize columns names

    # Take list of all km sections
    stamm_profiles = corners.index.drop_duplicates()

    # Iterates through km sections
    for sec in stamm_profiles:
        i = 0
        f, ax = plt.subplots()
        ax.xaxis.set_major_locator(ticker.MultipleLocator(xspacing))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(yspacing))
        plt.grid(True)
        
        for _file in list_of_profiles:

            # Take the Stamm Punkte
            reference_banks = corners.loc[sec]

            # Read the DataFrame
            profile = pd.read_csv(_file, skip_blank_lines=True, index_col=0, header=header)
            profile.dropna(how='any', inplace=True, axis=0)

            # Standardize the columns
            profile = rename_columns(profile)

            try:  # tries to take section (if it exist in the dataset)

                # Take only points of the km (sec)
                points_in_section = profile.loc[sec]

                # Calculate the pitagoras of lat and long
                distances = (points_in_section.lat ** 2 + points_in_section.long ** 2) ** 0.5
                references = np.array((reference_banks.lat ** 2 + reference_banks.long ** 2) ** 0.5)

                if delete_outside is None:
                    # Boolean array to take only points inside a certain range of interest
                    isinside = (distances <= references[1]) & (distances >= references[0]) | (
                            (distances <= references[0])
                            & (distances >= references[1]))

                    # Re-assign dataframes to take only points inside stammpunkte
                    points_in_section = points_in_section[isinside]

                elif delete_outside is not None and delete_outside is not _file:
                    delete_points_outside = pd.read_csv(delete_outside, skip_blank_lines=True, index_col=0,
                                                        header=header)
                    delete_points_outside.dropna(how='any', inplace=True, axis=0)
                    delete_points_outside = rename_columns(delete_points_outside)
                    delete_points_outside = delete_points_outside.loc[sec]
                    dist_delete = (delete_points_outside.lat ** 2 + delete_points_outside.long ** 2) ** 0.5
                    delete = np.array([np.max(dist_delete), np.min(dist_delete)])

                    isinside = ((distances <= delete[1]) & (distances >= delete[0]) | (
                            (distances <= delete[0])
                            & (distances >= delete[1]))) & ((distances <= references[1]) & (distances >= references[0]) | (
                            (distances <= references[0])
                            & (distances >= references[1])))

                    points_in_section = points_in_section[isinside]

                # Calculates the relative distance of the bathymetry having as reference point the left bank
                plot_distances = abs(((points_in_section.lat - reference_banks['lat'].iloc[0]) ** 2 + (
                        points_in_section.long - reference_banks['long'].iloc[0]) ** 2) ** 0.5)

                # Plots the km section
                ax.plot(plot_distances, points_in_section.bedelevation, marker=marker[i],
                        markerfacecolor='black', markersize=markersize[i], label=titles[i])

                ax.legend(loc='upper center')
                # plt.xlim(0, 180)

                # plt.scatter(references, reference_banks.bedelevation, marker="^", edgecolors='c', label='Stamm Punkte')
                i += 1

            except:  # skips the plot if the section doesnt exist
                message = "Could not save plot for " + _file + " in km section " + str(sec)
                print(message)
                pass

        # Get title and path of the section figure
        integer, decimal = split_float(sec)
        ax.tick_params(axis='both', labelsize='large')
        ax.set_xlabel(xlabel='Distance from left bank [m]')
        ax.set_ylabel(ylabel='Elevation [m.a.s.l]')
        # ax.tick_params(axis='x', width=20)
        ax.set_title(label='Cross section of km ' + str(sec))
        out = output_folder + '/' + 'km_' + str(integer) + '_' + str(decimal)

        # Save figure
        f.savefig(out)
        plt.clf()


if __name__ == '__main__':
    current_dir = Path.cwd()

    # ------------- INPUT ----------------------------------------------------

    # Path for the profiles to be plotted
    # (km section, lat, long, bed elevation) obs.: first column is always 0
    profiles = [str(current_dir / 'Profiles_Mesh_2007') + '.csv',
                str(current_dir / 'QP_2007_Fkm') + '.csv'
                ]

    # Path to stamm punkte
    # (km section, lat, long, bed elevation) obs.: first column is always 0
    bank_limits = str(current_dir) + '/' + 'Inn_Stamm_2014' + '.csv'

    # Titles of the legend in the plots
    title_list = ['Bed elevation in 2007 (Mesh)',
                  'Bed elevation in 2007 (Measurements)']

    # Spacing for the x labels
    del_x = 20  # every 20 m
    del_y = 1  # every 1 m

    # If the .csv files have header, please inser tthe number of header lines
    header = None

    markersize = [8, 4]  # corresponding to the respective profiles
    marker = [".", "^"]  # corresponding to the respective profiles

    # Folder to save all images
    output_folder = str(current_dir) + '/' + 'Inn_Profiles_2007_mesh_vs_meas_02'

    # -------------------------------------------------------------------

    # Create folder if it doesnt exist
    Path(output_folder).mkdir(exist_ok=True)
    profiles_generator(bank_limits, profiles, header, markersize, marker, title_list, output_folder, xspacing=del_x,
                       yspacing=del_y, delete_outside=str(current_dir / 'Profiles_Mesh_2007') + '.csv')
