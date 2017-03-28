#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
import sys

# -----------------------------------------------------------------------------------------------------------------------
# instance of mealy machine accepted by this utility:
#
# digraph DFA {
# 0 [label="0"];
# 	0 -> 1 [label="1 / 1"];
# 	0 -> 0 [label="0 / 2"];
# 	0 -> 2 [label="2 / 0"];
# 1 [label="1"];
# 	1 -> 1 [label="0 / 2"];
# 	1 -> 2 [label="1 / 0"];
# 	1 -> 2 [label="2 / 1"];
# 2 [label="2"];
# 	2 -> 0 [label="1 / 0"];
# 	2 -> 0 [label="2 / 1"];
# 	2 -> 2 [label="0 / 2"];
# }
#-----------------------------------------------------------------------------------------------------------------------


# regex for extracting state id (sid)
STATE_REGEX = "(?P<sid>[^\s-]+) \[.*\];"
# regex for extracting source state id (ssid), destination state id (dsid), input symbol (ins), and output symbol (ous)
TRANSITION_REGEX = "(?P<ssid>[^\s-]+) -> (?P<dsid>[^\s-]+) \[label=\"(?P<ins>.+) / (?P<ous>.+)\"\];"


def from_dot(path):
    # Path is a path to a dot file.
    # It loads the corresponding mealy machine in memory.
    # It assumes the first state encountered into the dot file is the starting state.
    # It assumes that all state definitions occur before the transition definitions into the dot file.
    ra = {"starting_state": None, "input_alpha": set(), "output_alpha": set(), "transitions": {}, "states": set()}
    with open(path, "r") as mh:
        for line in mh:
            match = re.search(TRANSITION_REGEX, line)
            if match is not None:
                ssid = match.group("ssid")
                if "__start" not in ssid:
                    dsid = match.group("dsid")
                    ins = match.group("ins")
                    if ins not in ra["input_alpha"]:
                        ra["input_alpha"].add(ins)
                    ous = match.group("ous").replace(";", "")
                    if ous not in ra["output_alpha"]:
                        ra["output_alpha"].add(ous)
                    # updating the model
                    if ssid not in ra["transitions"]:
                        ra["transitions"][ssid] = []
                        if ra["starting_state"] is None:
                            ra["starting_state"] = ssid
                        if ssid not in ra["states"]:
                            ra["states"].add(ssid)
                    if dsid not in ra["transitions"]:
                        ra["transitions"][dsid] = []
                        if ra["starting_state"] is None:
                            ra["starting_state"] = dsid
                        if dsid not in ra["states"]:
                            ra["states"].add(dsid)
                    ra["transitions"][ssid].append((dsid, ins, ous))
            else:
                match = re.search(STATE_REGEX, line)
                if match is not None:
                    sid = match.group("sid")
                    # updating the model
                    if sid not in ra["transitions"] and "__start" not in sid:
                        ra["transitions"][sid] = []
                        if ra["starting_state"] is None:
                            ra["starting_state"] = sid
                        if sid not in ra["states"]:
                            ra["states"].add(sid)
    return ra


def to_fmbt(model, path):
    # model is a mealy machine obtained by running "from_dot()".
    # path is the path where it will export the translation in AAL.
    # in this first version it just represents the state machine in fmbt format (without any additional variable)
    with open(path, "w") as ah:
        ah.write("# preview-depth: 20")
        ah.write("\nlanguage \"python\" {}")
        ah.write("\nvariables { current_state }")
        ah.write("\n\tinitial_state {")
        ah.write("\n\tcurrent_state = \"" + model["starting_state"] + "\"")
        ah.write("\n}")
        # body
        for ins in model["input_alpha"]:
            # generate a new test step
            ah.write("\ninput \"" + ins + "\" {")
            ah.write("\n\tguard {}")
            ah.write("\n\tbody {")
            states = list(model["states"])
            # considering middle states inf form of elif
            i = 0
            for state in states:
                if i == 0:
                    ah.write("\n\tif current_state == \"" + state + "\":")
                elif i == len(states) - 1:
                    ah.write("\n\telse:")
                else:
                    ah.write("\n\telif current_state == \"" + state + "\":")
                # looking for the right destnation state
                rstate, rous = None, None
                for dstate, nins, nous in model["transitions"][state]:
                    if nins == ins:
                        rstate = dstate
                        rous = nous
                        break
                ah.write("\n\t\tcurrent_state = \"" + str(rstate) + "\"")
                i += 1
            # closing braces
            ah.write("\n\t}")
            ah.write("\n}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("usage: python translate mealy_machne.dot mealy_machne.aal")
    mp, ap = sys.argv[1], sys.argv[2]
    m = from_dot(mp)
    to_fmbt(m, ap)