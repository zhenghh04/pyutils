#!/usr/bin/env python3
import json
import argparse
import sys
import glob
from timeline.timeline_trace import TorchTimelineTrace, TimelineTrace, combineTimelineTrace, PFWTimelineTrace, UnitraceTimelineTrace

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", action="extend", nargs="+", type=str)
    parser.add_argument("--output", type=str, default="combine.json")
    args = parser.parse_args()
    def get_trace(f):
        if f.split(".")[-1] == "pfw":
            TraceObj = PFWTimelineTrace
        elif f.split(".")[-1] == "json":
            TraceObj = TorchTimelineTrace
        elif f.split(".")[-1] == "unitrace":
            TraceObj = UnitraceTimelineTrace
        else:
            raise Exception("Unknown trace format")
        return TraceObj(f)
    if args.file_list is not None:
        a = [get_trace(f) for f in args.file_list]
        combine = combineTimelineTrace(a)
        combine.write(args.output)
    else:
        raise Exception(f"Please provide the list of files to be merged --inputs")

if __name__=="__main__":
    main()
