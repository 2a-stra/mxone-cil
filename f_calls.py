#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
MX-ONE call information logging parse
2021 June

2A-STRA blog

function definitions for "call_log.py"
'''
import re
import math

import pandas as pd
import yaml
from yaml.loader import SafeLoader

with open("cond_codes.yml") as fn:  # condition codes list
    codes = yaml.load(fn, Loader=SafeLoader)


def get_dat(fname):

    num = 6  # line 7 with col names

    with open(fname) as fp:
        for i, line in enumerate(fp):
            if i == num:
                line_n = line.strip()
                break

    line_n = line_n[2:]
    col_names = line_n.split(", ")
    calls = pd.read_csv(fname, comment='#', names=col_names)

    return calls


def f_codes(Series):
    try:
        return codes[str(Series)]
    except:
        return "Pls see '3_15519-ANF90114.pdf' description for details"


def f_condition(calls):

    cond = calls["condition code"]
    cond_table = cond.value_counts().sort_index().reset_index().reset_index(drop=True)
    cond_table.columns = ["Condition codes", "Frequency"]
    cond_table["%"] = cond_table["Frequency"] / calls.shape[0] * 100
    cond_table["%"] = cond_table["%"].astype(int)
    cond_table["Reason"] = cond_table["Condition codes"].apply(f_codes)

    return cond_table


def f_dur(Series):

    days, hours, minutes, sec = re.findall(r"(\d{1})d(\d{2}):(\d{2}):(\d{2})", Series)[0]
    secs = int(days) * 24 * 60 *60 + int(hours) * 60 * 60 + int(minutes) * 60 + int(sec)

    return secs

def d_minutes(calls):

    dur = pd.DataFrame(calls["duration"], columns = ["duration"])
    dur["sec"] = dur["duration"].apply(f_dur)
    dur["minutes"] = dur["sec"] / 60

    return dur


def f_duration(calls, dur):

    dur_table = dur["minutes"].apply(math.ceil).value_counts().sort_index().reset_index().reset_index(drop=True)
    dur_table.columns = ["Minutes", "Frequency"]
    dur_table["%"] = dur_table["Frequency"] / calls.shape[0] * 100
    dur_table["%"] = dur_table["%"].astype(int)

    return dur_table


def vacant(calls):

    vac_df = calls[calls["condition code"] == 30]
    #import pdb; pdb.set_trace()
    try:
        vac = set(vac_df["dialed number"].astype(int))
    except:
        vac = set(vac_df["dialed number"].astype(str).map(str.strip))
    
    print("Vacant: %s numbers" % len(vac))
    return sorted(vac)

