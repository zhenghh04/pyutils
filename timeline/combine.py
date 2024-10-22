#!/usr/bin/env python3
import json
import argparse
import sys
import glob
from timeline_trace import TorchTimelineTrace, TimelineTrace, combineTimelineTrace
parser = argparse.ArgumentParser()
parser.add_argument("--file-list", action="extend", nargs="+", type=str)
parser.add_argument("--output", type=str, default="combine.json")
args = parser.parse_args()

flist = args.file_list
a = [TorchTimelineTrace(f) for f in args.file_list]
combine = combineTimelineTrace(a)
combine.write(args.output)
