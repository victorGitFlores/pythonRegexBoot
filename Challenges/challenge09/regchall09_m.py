# regchall09_m.py

# [2025-01-16 08:15:30] INFO: System booted successfully.
# timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
# MY TASK: 
# Extract all lines with the word ERROR that occurred between 09:00:00 and 10:30:00

import re
import datetime

#--------------------------------------------------------------------------------------
def check_for_warnings(input_tups, ts_from, ts_to): # retruns True if any warnings found
    for tup in input_tups:
        msg_ts_str  = tup[0]
        msg_typ     = tup[1]
        msg_txt     = tup[2]
        msg_ts = datetime.datetime.strptime(msg_ts_str, "%Y-%m-%d %H:%M:%S")
        if (msg_ts >= ts_from and msg_ts <= ts_to and msg_typ == "WARNING"):
            return True
    return False
#--------------------------------------------------------------------------------------

def main():

    patt = r"\[(\d{4}\-\d{2}\-\d{2}\s\d{2}\:\d{2}\:\d{2})\]\s(\w+)\:\s(.+)"
    tot_err = 0
    ts_from = datetime.datetime.strptime("2025-01-16 09:00:00", "%Y-%m-%d %H:%M:%S")
    ts_to   = datetime.datetime.strptime("2025-01-16 10:30:00", "%Y-%m-%d %H:%M:%S")
    infile  = "system_logs.txt"
    outfile = "filtered_errors.txt"
    my_tups = []


    with open(infile,"r") as input:
        my_tups = [
            (match.group(1), match.group(2), match.group(3))
            for line in input
            if (match := re.search(patt, line))
        ]
    # for each tuple...break into fields...if in meets condition, print.
    with open(outfile,"w") as output:
        for tup in my_tups:
            msg_ts_str  = tup[0]
            msg_typ     = tup[1]
            msg_txt     = tup[2]
            msg_ts = datetime.datetime.strptime(msg_ts_str, "%Y-%m-%d %H:%M:%S")
            if (msg_ts >= ts_from and msg_ts <= ts_to and msg_typ == "ERROR"):
                print(f"{msg_ts} {msg_typ} {msg_txt}")
                tot_err += 1
                # write to outfile
                outline = f"{msg_ts} {msg_typ} {msg_txt}\n"
                output.write(outline)

    print(f"Total Errors: {tot_err}")
    print(f"File written: {outfile}")
    # lastly, any errors in the datetime range?
    if check_for_warnings(my_tups, ts_from, ts_to):
        print("Warnings found in the datetime range.")
    else:
        print("No warnings found in the datetime range.")


#--------------------------------------------------------------------------------------
if __name__ == "__main__":
    main()
#--------------------------------------------------------------------------------------

""" actual output:
PS C:\_home\learning\python ai bootcamp 2025\challenges> python regchall09_m.py
2025-01-16 09:05:45 ERROR Disk space critically low.
2025-01-16 10:00:00 ERROR Failed to write to log file.
2025-01-16 10:20:30 ERROR Database connection timeout.
Total Errors: 3
File written: filtered_errors.txt
Warnings found in the datetime range.
"""
