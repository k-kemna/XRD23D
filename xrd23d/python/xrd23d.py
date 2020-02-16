# -*- coding: utf-8 -*-
# @Author: kiliankemna
# @Date:   2020-02-13T16:42:57+01:00
# @Email:  kilian.kemna@rub.de
# @Project: XRD23D
# @Filename: xrd23d.py
# @Last modified by:   kiliankemna
# @Last modified time: 2020-02-13T16:43:41+01:00
# Script to combine XRD files into single .csv file with associated height as third column.

import csv
import fnmatch
import os
import warnings
import tkinter as tk
from tkinter import filedialog


def _read_loc_dict(loc_csv):

    loc_dict = {}

    with open(loc_csv, 'r') as file:

        dialect = csv.Sniffer().sniff(file.readline())
        reader = csv.reader(file, dialect)
        # Iterate over rows and write to dictionary
        for row in reader:
            if not fnmatch.fnmatch(row[0], "*sample"):
                loc_dict[row[0]] = row[1]
    return loc_dict


def _read_xrd_files(csv_file_list, loc_dict):

    xrd_master_list = []

    # Iterate over csv files and append master_list
    for xrd_csv_file in csv_file_list:

        # Get Sample ID from file name
        sample_id = os.path.split(xrd_csv_file)[-1].split(".")[0]

        # Get location of sample
        loc = [item for key, item in loc_dict.items() if fnmatch.fnmatchcase(
            key.replace(" ", "").lower(), sample_id.lower())]
        if len(loc) == 0:
            continue
        elif len(loc) == 1:
            loc = loc[0]

        else:
            raise ValueError("Sample ID has to heights. Check and correct!")

        # Try first to use utf-8 encoding. Otherwise fall back to latin1
        try:
            with open(xrd_csv_file, 'r', encoding="utf-8") as xrd_file:

                # Read .csv file
                reader_xrd = csv.reader(xrd_file, delimiter=";")
                # Rewrite into list
                row_list = [row for row in reader_xrd]
                pass

        except UnicodeDecodeError:

            with open(xrd_csv_file, 'r', encoding="latin1") as xrd_file:
                # Read .csv file
                reader_xrd = csv.reader(xrd_file, delimiter=";")
                # Rewrite into list
                row_list = [row for row in reader_xrd]
                pass

        # Get idx where measurment values start
        data_idx = [row[0] for row in row_list].index("Angle") + 1

        # Rewrite XRD file into list formt
        xrd_list_tmp = [[row[0], row[1], loc] for row in row_list[data_idx:]]
        xrd_master_list.extend(xrd_list_tmp)

        # except Exception as e:
        #     warnings.warn("Cannot read {}".format(xrd_csv_file))

        continue

    return xrd_master_list


def _check_cons(loc_dict, csv_file_list,log_list):

    msg = "+ Check consistency between XRD files and location file"
    print(msg)
    log_list.append(msg)

    # Generate list with ids from csv_file_list
    xrd_id_list = [os.path.split(file)[-1].split(".")[0]
                   for file in csv_file_list]

    # Get list with location ID list
    loc_id_list = list(loc_dict.keys())
    # Compare lists and get differences. First xrd measruments with no location
    xrd_no_loc = [
        id_xrd for id_xrd in xrd_id_list if id_xrd not in loc_id_list]

    # Location with no XRD measruement
    loc_no_xrd = [
        id_loc for id_loc in loc_id_list if id_loc not in xrd_id_list]

    if len(xrd_no_loc) == 0 and len(loc_no_xrd) == 0:
        msg = "+ Everything looks good :-)\n"
        log_list.append(msg)
        print(msg)

    if len(xrd_no_loc) != 0:
        msg = "+\tWARNING: XRD measurement(s) with ID(s) {} has/have no location(s). Measurement(s) will be exculded in the following\n".format(
            ",".join(xrd_no_loc))
        log_list.append(msg)
        print(msg)

    if len(loc_id_list) != 0:

        msg = "+\tWARNING:Location with ID(s) {} has/have no XRD measurement(s). Location will not be used in the following\n".format(
            ",".join(loc_no_xrd))
        print(msg)
        log_list.append(msg)

    return log_list


def main():

    log_list = []
    msg = "Script to combine XRD files and associate each file with a given location\n"
    print(msg)
    log_list.append(msg)

    # Get dirs and filename for height association
    root = tk.Tk()
    root.withdraw()

    print("Please select folder with .csv files containing XRD measurements")
    xrd_csv_file_dir = filedialog.askdirectory(
        title="Select folder with XRD measurements")

    print("\n")
    print("Please select .csv file with location of each measurment")
    loc_csv = filedialog.askopenfilename(title="Select .csv file with locations", filetypes=(
        ("Location .csv file", "*.csv"), ("all files", "*.*")))

    print("\n")
    print("Please select output folder")
    output_dir = filedialog.askdirectory(title="Select output folder")

    print("Thanks!")

    # Read .csv file with location information into dictionary
    loc_dict = _read_loc_dict(loc_csv)
    msg = "+ Done - Read file with location. {} samples available".format(
        len(loc_dict.keys()))
    print(msg)
    log_list.append(msg)

    # Get list of .csv xrd files
    csv_file_list = [os.path.join(xrd_csv_file_dir, file) for file in os.listdir(
        xrd_csv_file_dir) if fnmatch.fnmatch(file, "*csv")]

    msg = "+ {} XRD .csv files available".format(len(csv_file_list))
    print(msg)
    log_list.append(msg)

    # Run consistency check between csv files and location file
    _check_cons(loc_dict, csv_file_list,log_list)
    msg = "+ Start to combine .csv files and associate location"
    print(msg)
    log_list.append(msg)

    # Generate master list with xrd measruements and location
    csv_master_list = _read_xrd_files(csv_file_list, loc_dict)

    # Write .csv file
    with open(os.path.join(output_dir, "combined_xrd_3d.csv"), 'w', newline='') as out_file:
        writer = csv.writer(out_file)

        # Write Header
        writer.writerow(["Alpha", "Intensity", "Location"])

        # Write body
        writer.writerows(csv_master_list)

    # Write log file

    msg = "+\tDone - Saved .csv file with {} lines in {} ".format(len(csv_master_list),output_dir)
    print(msg)
    log_list.append(msg)

    with open(os.path.join(output_dir, "xrd23d_log.txt"), 'w', newline='') as log_file:
        log_file.write("\n".join(log_list))

    input("Press any key to close")


if __name__ == '__main__':
    main()
