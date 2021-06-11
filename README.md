# Description
MX-ONE call information logging (CIL) parsing using Python 3 and Pandas. Calculate calls statistics: total number of calls, condition codes and call durations distributions.

Python scripts:

| file | description |
| ---- | ----------- |
| call_log.py | main script |
| f_calls.py | functions for main script |
| cond_codes.yml | YAML file with condition codes descriptions |

Install python3 dependencies:
```
$ apt-get install pip3
$ pip3 install pandas tabulate pyyaml
```

Run script:
```
$ python3 ./call_log.py
```

# Preparations
MX-ONE commands to create call logging for LIM 1 to local directory `/var/opt/eri_sn/call_logging/` with CSV file type:
```
callinfo_output_set -output 0 -lim 1 -local -type file -dbname /var/opt/eri_sn/call_logging/lim1 -subtype commaseparated
callinfo_status_set -output 0 -lim 1 -state on
callinfo_status_print -lim 1 -output 0
```

Find call record details files `lim1.x.dat`, where`x` is the day of the week number:
```
mxone_admin@mx1:~> cd /var/opt/eri_sn/call_logging/

mxone_admin@mx1:/var/opt/eri_sn/call_logging> ll
total 17476
-rw-r----- 1 eri_sn_d eri_sn_g    3417 Jun  6 00:00 lim1.0.dat
-rw-r----- 1 eri_sn_d eri_sn_g    3417 Jun  7 00:00 lim1.1.dat
-rw-r----- 1 eri_sn_d eri_sn_g 1453639 Jun  8 23:49 lim1.2.dat
-rw-r----- 1 eri_sn_d eri_sn_g 5697519 Jun 10 00:00 lim1.3.dat
-rw-r----- 1 eri_sn_d eri_sn_g 5763712 Jun 10 23:59 lim1.4.dat
-rw-r----- 1 eri_sn_d eri_sn_g 4944028 Jun 11 17:00 lim1.5.dat
-rw-r----- 1 eri_sn_d eri_sn_g    3417 Jun  5 00:00 lim1.6.dat
```

Copy call logs from `remote-mx1` to local directory `dat` with python scripts:
```
$ rsync remote-mx1:/var/opt/eri_sn/call_logging/* ~/dat
```

You could put `cron` task for automatic sync every day at 3:15am:
```
$ crontab -e
15 3 * * * rsync remote-mx1:/var/opt/eri_sn/call_logging/* ~/dat
```

# Running script
Run script without parameter to analyze all `.dat` files in a local directory and finally print summary table:
```
$ python3 ./call_log.py
...

| file       | start                     | end                       |   calls |   non-zero calls % |   minutes |
|------------+---------------------------+---------------------------+---------+--------------------+-----------|
| lim1.0.dat | nan                       | nan                       |     nan |                nan |    nan    |
| lim1.1.dat | nan                       | nan                       |     nan |                nan |    nan    |
| lim1.2.dat | 2021-06-08 15:06:39 (MSK) | 2021-06-08 23:47:42 (MSK) |    4724 |                 38 |   2843.08 |
| lim1.3.dat | 2021-06-09 00:00:09 (MSK) | 2021-06-09 23:58:33 (MSK) |   18494 |                 38 |  10737.8  |
| lim1.4.dat | 2021-06-10 00:00:01 (MSK) | 2021-06-10 23:59:02 (MSK) |   18693 |                 36 |   9825.28 |
| lim1.5.dat | 2021-06-10 23:59:44 (MSK) | 2021-06-11 16:17:27 (MSK) |   15555 |                 37 |   7590.1  |
| lim1.6.dat | nan                       | nan                       |     nan |                nan |    nan    |

Totally: 30996 minutes
Done.
```

Run script with file name option to see details with calls distribution per condition codes and per call durations for particular file `lim1.4.dat` (4 - Thursday):
```
$ python3 ./call_log.py lim1.4.dat
Starting...
lim1.4.dat
Calls:  18693
Minutes: 9825 (Hours: 163)
|    |   Condition codes |   Frequency |   % | Reason                  |
|----+-------------------+-------------+-----+-------------------------|
|  0 |                10 |        6781 |  36 | Outgoing call           |
|  1 |                23 |         908 |   4 | Abandoned incoming call |
|  2 |                25 |           1 |   0 | Abandoned internal call |
|  3 |                28 |        9622 |  51 | Abandoned outgoing call |
|  4 |                29 |         388 |   2 | Calls to busy party     |
|  5 |                30 |         993 |   5 | Calls to vacant number  |

|    |   Minutes |   Frequency |   % |
|----+-----------+-------------+-----|
|  0 |         0 |       12017 |  64 |
|  1 |         1 |        4030 |  21 |
|  2 |         2 |        1342 |   7 |
|  3 |         3 |         553 |   2 |
|  4 |         4 |         239 |   1 |
|  5 |         5 |         157 |   0 |
|  6 |         6 |          97 |   0 |
|  7 |         7 |          58 |   0 |
|  8 |         8 |          62 |   0 |
|  9 |         9 |          26 |   0 |
| 10 |        10 |          26 |   0 |
| 11 |        11 |          13 |   0 |
| 12 |        12 |          21 |   0 |
| 13 |        13 |          10 |   0 |
| 14 |        14 |           6 |   0 |
| 15 |        15 |           7 |   0 |
| 16 |        16 |           3 |   0 |
| 17 |        17 |           3 |   0 |
| 18 |        18 |           3 |   0 |
| 19 |        19 |           1 |   0 |
| 20 |        21 |           4 |   0 |
| 21 |        22 |           1 |   0 |
| 22 |        23 |           3 |   0 |
| 23 |        24 |           1 |   0 |
| 24 |        27 |           1 |   0 |
| 25 |        29 |           1 |   0 |
| 26 |        30 |           1 |   0 |
| 27 |        33 |           1 |   0 |
| 28 |        36 |           1 |   0 |
| 29 |        39 |           1 |   0 |
| 30 |        44 |           1 |   0 |
| 31 |        52 |           1 |   0 |
| 32 |        57 |           1 |   0 |
| 33 |        84 |           1 |   0 |
...
```

You could see totally 18693 calls in example above including:

- 6781 calls (36%) with reason `Outgoing calls` lasts 9825 minutes;
- 9622 calls (51%) with reason `Abandoned outgoing call`;
- 12017 calls (64%) with 0 time duration.
