#!/usr/bin/env python3
import json
import argparse
import sys
import glob
from timeline_trace import TorchTimelineTrace, TimelineTrace, combineTimelineTrace, PFWTimelineTrace, UnitraceTimelineTrace
parser = argparse.ArgumentParser()
parser.add_argument("--file-list", action="extend", nargs="+", type=str)
parser.add_argument("--output", type=str, default="combine.json")
parser.add_argument("--type", default="torch", type=str)
args = parser.parse_args()

TraceObj = None
if args.type == "torch":
    TraceObj = TorchTimelineTrace
elif args.type == "pfw":
    TraceObj = PFWTimelineTrace
elif args.type == "unitrace":
    TraceObj = UnitraceTimelineTrace
else:
    raise Exception(f"Unknown trace type {args.type}")
a = [TraceObj(f) for f in args.file_list]
combine = combineTimelineTrace(a)
combine.write(args.output)
