#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
MX-ONE call information logging parse
2021 June

2A-STRA blog
'''
import sys
import os

import pandas as pd
from tabulate import tabulate

import f_calls

print("Starting...")

if len(sys.argv) > 1:
    fn = sys.argv[1]

dat_list = []
if len(sys.argv) == 1:
    flist = os.listdir("./")
    for each in flist:
        if ".dat" in each[-4:]:
            dat_list.append(each)
else:
    dat_list.append(fn)

total = pd.DataFrame(columns=["file", "start", "end", "calls", "non-zero calls %", "minutes"])
total["file"] = dat_list
total.set_index("file", inplace=True)

for fname in dat_list:

    calls = f_calls.get_dat(fname)

    if not calls.empty:

        print(fname)
        cond_table = f_calls.f_condition(calls)
        
        calls_num = calls.shape[0]

        if not calls_num == 0:
            print("Calls: ", calls_num)
            total.loc[fname, "calls"] = calls_num
            total.loc[fname, "start"] = calls.loc[0, "start time local"]
            total.loc[fname, "end"] = calls.loc[calls_num - 1, "start time local"]

        dur = f_calls.d_minutes(calls)
        minutes = dur["minutes"].sum()
        print("Minutes: %d (Hours: %d)" % (minutes, minutes/60))
        total.loc[fname, "minutes"] = dur["minutes"].sum()

        dur_table = f_calls.f_duration(calls, dur)
        total.loc[fname, "non-zero calls %"] = 100 - dur_table.loc[0, "%"]

        print(tabulate(cond_table, headers="keys", tablefmt="orgtbl"))
        print()
        print(tabulate(dur_table, headers="keys", tablefmt="orgtbl"))

print()
total.sort_values(by="start", inplace=True)
print(tabulate(total, headers="keys", tablefmt="orgtbl"))
print("\nTotally: %d minutes" % total["minutes"].sum())

print("Done.")

#import pdb; pdb.set_trace()
