#!/usr/bin/env python3
import json
import argparse
import sys
import glob
from torch_timeline_trace import TorchTimelineTrace
parser = argparse.ArgumentParser()
parser.add_argument("--file-list", action="extend", nargs="+", type=str)
parser.add_argument("--output", type=str, default="combine.json")
args = parser.parse_args()


flist = args.file_list
a = TorchTimelineTrace(flist[0]).json
for f in flist[1:]:
    b = TorchTimelineTrace(f).json
    a["traceEvents"] += b["traceEvents"]
with open(args.output, "w") as fout:
    fout.write(json.dumps(a, indent=4))
