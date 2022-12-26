#!/usr/bin/env python  # A shebang at the top
"""Counts the pre-dominant chords in a file. 

This script counts the last pre-dominant chord before the dominant in 
Perfect Authentic Cadences (PACs) and Imperfect Authentic Cadences (IACs). 
It then writes a new output file with the associated counts, as well as 
an output file with select information about the pre-dominant/cadence pairs. 
"""  # Script by Rebecca Moranis.

import argparse
import csv


def main(args: argparse.Namespace) -> None:
    # info about K number, mvt, and year of completion of each work
    metadata = []
    with open("/Users/rebeccamoranis/finalproj/mozart_piano_sonatas-main/metadata.tsv") as source:
        reader = csv.reader(source, delimiter="\t")
        for line in reader:
            metadata.append(line)

    i = 1  # setting the index to be the 2nd row, since 1st row is column headers
    temp_str = "K" + str(args.k) + "-" + str(args.mvt)
    if metadata[i][0] != temp_str:
        while metadata[i][0] != temp_str:  # increase the row if the mvt hasn't been found yet in the metadata
            i += 1
    year_end = metadata[i][20]  # year the composition was completed (column index is fixed)
    print("OPUS, MVT, YEAR END")
    print(args.k, args.mvt, year_end)

    full_list = []  # empty list for a copy of the tsv file, now in list form (a list of lists)
    with open(args.input) as source:
        reader = csv.reader(source, delimiter="\t")
        for line in reader:
            full_list.append(line)

    # including line numbers on each line of the list to have a stable record of lines
    i = 1  # index for line numbers in list. begins at 1. column headers are considered as line 1.
    for line in full_list:
        temp = "{}{}".format('line ', str(i))
        line.insert(0, temp)
        i += 1
    # print the full list
    # for line in full_list:
    #     print(line)

    # find the column indices, since these are not fixed across all tsv files
    mn_index = 0
    for item in full_list[0]:  # find mn
        if item == "mn":
            break
        mn_index += 1

    mn_on_index = 0
    for item in full_list[0]:  # find mn onset
        if item == "mn_onset":
            break
        mn_on_index += 1

    loc_k_index = 0
    for item in full_list[0]:  # find local key
        if item == "localkey":
            break
        loc_k_index += 1

    ch_index = 0
    for item in full_list[0]:  # find chord
        if item == "chord":
            break
        ch_index += 1

    num_index = 0
    for item in full_list[0]:  # find numeral
        if item == "numeral":
            break
        num_index += 1

    cad_index = 0
    for item in full_list[0]:  # find cadence
        if item == "cadence":
            break
        cad_index += 1

    i = 0  # reset index
    new_list_cads = []
    for line in full_list:
        if i:  # boolean coercion, making sure current row isn't the first row (i != 0)
            if line[cad_index] == "PAC" or line[cad_index] == "IAC":  # only want PAC and IAC cadences
                # look for the PD row
                j = i - 1  # do not need to check current row, since cad row won't be PD row
                while full_list[j][num_index] == "V" or full_list[j][num_index] == "I" or \
                        full_list[j][num_index] == "v" or full_list[j][num_index] == "i":
                    j = j - 1  # backwards the index if V or I or v or i are the numeral of the row
                new_list_cads.append(full_list[j])  # append the PD row
                new_list_cads.append(full_list[i])  # append the cadence row
        i += 1  # increment the index
    print("PD-CADENCE PAIRS")
    for line in new_list_cads:
        print(line)

    # storing only selected info about the PD and cadence pairs
    i = 0  # reset index
    useful_list = []
    for line in full_list:
        if not i:  # boolean coercion, if line is the first line
            # append the titles to the list
            temp = [line[0], line[mn_index], line[mn_on_index], line[loc_k_index], line[ch_index], line[num_index],
                    line[cad_index]]  # line number, mn, mn_onset, local key, chord, numeral, cadence
            useful_list.append(temp)
        elif line[cad_index] == "PAC" or line[cad_index] == "IAC":  # if not first line, check if cadence is PAC or IAC
            # look for the PD row
            j = i - 1
            while full_list[j][num_index] == "V" or full_list[j][num_index] == "I" or \
                    full_list[j][num_index] == "v" or full_list[j][num_index] == "i":
                j = j - 1  # backwards the index
            # temp PD row
            temp = [full_list[j][0], full_list[j][mn_index], full_list[j][mn_on_index],
                    full_list[j][loc_k_index], full_list[j][ch_index], full_list[j][num_index], full_list[j][cad_index]]
            # line number, mn, mn_onset, local key, chord, numeral, cadence
            useful_list.append(temp)  # append the PD row
            # temp cadence row
            temp = [full_list[i][0], full_list[i][mn_index], full_list[i][mn_on_index],
                    full_list[i][loc_k_index], full_list[i][ch_index], full_list[i][num_index], full_list[i][cad_index]]
            # line number, mn, mn_onset, local key, chord, numeral, cadence
            useful_list.append(temp)  # append the cadence row
        i += 1
    print("CONDENSED INFO ABOUT CADENCES")
    for line in useful_list:
        print(line)

    # write the condensed cadence info to tsv
    name_str = "cad_info" + str(args.k) + "-" + str(args.mvt) + ".tsv"  # uses args
    with open(name_str, "w") as sink:
        writer = csv.writer(sink, delimiter="\t")
        for row in useful_list:
            writer.writerow(row)

    # count the frequency of PD types in this movement
    # parity of the line number helps to identify whether the current line is a PD or cadence
    # in each PD/cad line pair from useful_list. the odd numbered rows are the PDs
    temp_dict = {}
    i = 0  # reset index
    for line in useful_list:
        if i % 2:  # want only the odd-numbered rows, as these are the PDs
            if line[4] not in temp_dict:  # there is no dict entry yet for this PD chord
                temp_dict[line[4]] = 1  # create a key-value pair
            else:  # there already is a dict key-value pair for this PD chord
                temp_dict[line[4]] += 1  # increment the value
        i += 1
    # sort the above dictionary so that PD chords frequencies are ranked from highest to lowest.
    print("SORTED PD CHORD COUNTS")
    sorted_pds = sorted(temp_dict.items(), key=lambda x: x[1], reverse=True)
    print(sorted_pds)

    # write the sorted PD counts to tsv
    name_str = "pd" + str(args.k) + "-" + str(args.mvt) + ".tsv"  # uses args
    with open(name_str, "w") as sink:
        writer = csv.writer(sink, delimiter="\t")
        for row in sorted_pds:
            writer.writerow(row)


if __name__ == "__main__":  # A main-guard which parses the arguments using argparse and then passes them to main.
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument("input", help="input file path")
    parser.add_argument("--k", type=int, required=True, help="Mozart K number")
    parser.add_argument("--mvt", type=int, required=True, help="mvt number")
    main(parser.parse_args())
