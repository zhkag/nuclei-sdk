#!/bin/env python3

import os
import sys
import argparse
from prettytable import *
import json

HPM_EVENTS= [
        ["Cycle count", "Retired instruction count", "Integer load instruction (includes LR)",
         "Integer store instruction (includes SC)", "Atomic memory operation (do not include LR and SC)",
         "System instruction", "Integer computational instruction(excluding multiplication/division/remainder)",
         "Conditional branch", "Taken conditional branch", "JAL instruction", "JALR instruction", "Return instruction",
         "Control transfer instruction (CBR+JAL+JALR)", "-", "Integer multiplication instruction",
         "Integer division/remainder instruction", "Floating-point load instruction", "Floating-point store instruction",
         "Floating-point addition/subtraction", "Floating-point multiplication",
         "Floating-point fused multiply-add (FMADD, FMSUB, FNMSUB, FNMADD)", "Floating-point division or square-root",
         "Other floating-point instruction", "Conditional branch prediction fail", "JAL prediction fail", "JALR prediction fail"],
        ["Icache miss", "Dcache miss", "ITLB miss", "DTLB miss", "Main TLB miss"]
]

HPM_MEVENT_ENABLE = 0x8
HPM_SEVENT_ENABLE = 0x4
HPM_UEVENT_ENABLE = 0x1


def get_hpm_evmode(ena):
    evmode = ""
    if ena & HPM_MEVENT_ENABLE:
        evmode += "M"
    if ena & HPM_SEVENT_ENABLE:
        evmode += "S"
    if ena & HPM_UEVENT_ENABLE:
        evmode += "U"
    return evmode

def get_hpm_event(sel, idx):
    if sel >= len(HPM_EVENTS):
        return "INVAILD"
    if idx >= len(HPM_EVENTS[sel]):
        return "INVAILD"
    return HPM_EVENTS[sel][idx]

def parse_hpm(logfile):
    if os.path.isfile(logfile) == False:
        return dict()
    hpmrecords = dict()
    with open(logfile, "r") as lf:
        for line in lf.readlines():
            if line.startswith("HPM"):
                hpmkey, proc, hpmcount = line.split(",")
                hpmkey = hpmkey.strip()
                proc = proc.strip()
                hpmcount = hpmcount.strip()
                if proc not in hpmrecords:
                    hpmrecords[proc] = dict()
                hpmrecords[proc][hpmkey] = hpmcount
    return hpmrecords

def analyze_hpm(records):
    x = PrettyTable()
    x.set_style(MARKDOWN)
    x.field_names = ["Process", "HPM", "Mode", "Event", "Counts"]
    parsed_hpm = dict()
    for proc in records:
        parsed_hpm[proc] = dict()
        for hpmkey in records[proc]:
            hpmcounter, hpmevent = hpmkey.split(":")
            hpmevent = int(hpmevent, 16)
            event_sel = hpmevent & 0xF
            event_idx = (hpmevent >> 4) & 0xF
            event_ena = (hpmevent >> 28) & 0xF
            event_name = get_hpm_event(event_sel, event_idx)
            event_mode = get_hpm_evmode(event_ena)
            event_count = int(records[proc][hpmkey])
            x.add_row([proc, hpmcounter, event_mode, event_name, event_count])
            if hpmcounter not in parsed_hpm[proc]:
                parsed_hpm[proc][hpmcounter] = list()
            parsed_hpm[proc][hpmcounter].append((event_mode, event_name, event_count))
    return parsed_hpm, x

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Nuclei SDK HPM Log Parsing")
    parser.add_argument('--logfile', required=True, help="log file of hpm running")

    args = parser.parse_args()

    hpmrecords = parse_hpm(args.logfile)
    if len(hpmrecords) == 0:
        print("None records found in %s!" % (args.logfile))
        sys.exit(1)
    parsedhpm, table = analyze_hpm(hpmrecords)
    print(table)

    hpmresult = {"records": hpmrecords, "parsed": parsedhpm}
    hpmrstfile = args.logfile + ".json"
    with open(hpmrstfile, "w") as cf:
        json.dump(hpmresult, cf, indent=4)

    print("\nParsed HPM event saved into %s" %(hpmrstfile))
    sys.exit(0)

