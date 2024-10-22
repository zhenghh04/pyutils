#!/usr/bin/env python
import json
class TimelineTrace(object):
    def __init__(self, fname):
        print(f"Reading Trace from {fname}")
        self.fname = fname
        self.json = {}
    def get_json(self):
        return self.json
    def write(self, fname):
        print(f"Writing Trace to {fname}")
        with open(fname, "w") as fout:
            fout.write(json.dumps(self.json))
        
class TorchTimelineTrace(TimelineTrace):
    def __init__(self, fname):
        super().__init__(fname)
        with open(fname, "r") as fin:
            self.json = json.load(fin)
        self.rank = self._get_rank()
        self.world_size = self._get_world_size()
        self.num_devices = self._get_num_devices()
        self.rename_process_name()
        self.type = "torch"
    def _get_rank(self):
        return self.json["distributedInfo"]["rank"]
    def _get_num_devices(self):
        return len(self.json["deviceProperties"])
    def _get_world_size(self):
        return self.json["distributedInfo"]["world_size"]
    def rename_process_name(self):
        trace = self.json["traceEvents"]
        for i in range(len(trace)):
            a = trace[i]
            if a["name"] == "PyTorch Profiler (0)":
                a["pid"] = f"Spans {self.rank}"
            if a["name"] == "process_name":
                if a["pid"] < 100:
                    if a["pid"] == self.rank%self.num_devices:
                        a["args"]["name"] = f"Rank-{self._get_rank()}-DEVICE"
                else:
                    a["args"]["name"] = f"Rank-{self._get_rank()}-HOST"
            if a["pid"] == self.rank%self.num_devices:
                a["pid"] = 100*self.rank + a["pid"]
            self.json["traceEvents"][i] = a

class UniTraceTimelineTrace(TimelineTrace):
    def __init__(self, fname):
        super().__init__(fname)
        with open(fname, "r") as fin:
            self.json = json.load(fin)
        self.type = "unitrace"
    def json(self):
        return self.json
    def write(self, fname):
        with open(fname, "w") as fout:
            fout.write(json.dumps(self.json))
            
class PFWTimelineTrace(TimelineTrace):
    def __init__(self, fname):
        super().__init__(fname)
        self.json["traceEvents"] = []
        with open(fpfw, "r") as fin:
            f = fin.readlines()
            start_line = 0
            end_line = len(f)
            if f[0].split()[0]=="[":
                start_line = 1
            if f[-1].split()[0]=="]":
                end_line = -1
            for l in f[start_line:end_line]:
                self.json.append(l)

        
def combineTimelineTrace(trace_list):
    combine_trace = trace_list[0].get_json()
    for a in trace_list[1:]:
        combine_trace["traceEvents"] += a.json["traceEvents"]
    trace_list[0].json = combine_trace
    return trace_list[0]
    
