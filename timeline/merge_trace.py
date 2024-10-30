#!/usr/bin/env python3
import json
import argparse
import sys
import glob
from timeline.timeline_trace import TorchTimelineTrace, TimelineTrace, combineTimelineTrace, PFWTimelineTrace, UnitraceTimelineTrace

def main():
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
    if args.file_list is not None:
        a = [TraceObj(f) for f in args.file_list]
        combine = combineTimelineTrace(a)
        combine.write(args.output)
    else:
        raise Exception(f"Please provide the list of files to be merged --file-list")

if __name__=="__main__":
    main()
