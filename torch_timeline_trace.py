#!/usr/bin/env python
import json
class TorchTimelineTrace:
    def __init__(self, fname):
        self.fname = fname
        with open(fname, "r") as fin:
            self.json = json.load(fin)
        self.rank = self._get_rank()
        self.world_size = self._get_world_size()
        self.num_devices = self._get_num_devices()
        self.rename_process_name()
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
            if a["name"] == "process_name":
                if a["pid"] < 100:
                    if a["pid"] == self.rank%self.num_devices:
                        a["args"]["name"] = f"Rank-{self._get_rank()}-DEVICE"
                else:
                    a["args"]["name"] = f"Rank-{self._get_rank()}-HOST"
            if a["pid"] == self.rank%self.num_devices:
                a["pid"] = 100*self.rank + a["pid"]
            self.json["traceEvents"][i] = a
    def write(self, fname):
        with open(fname, "w") as fout:
            fout.write(json.dumps(self.json))
                
                
        
        
