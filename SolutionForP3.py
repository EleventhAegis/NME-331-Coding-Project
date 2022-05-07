from Traversals import bfs_path
import heapq
from collections import deque
from Simulator import Simulator
import sys

class Solution:

    def __init__(self, problem, isp, graph, info):
        self.problem = problem
        self.isp = isp
        self.graph = graph
        self.info = info

    def output_paths(self):
        """
        This method must be filled in by you. You may add other methods and subclasses as you see fit,
        but they must remain within the Solution class.
        """
        paths, bandwidths, priorities = {}, {}, {}
        # Note: You do not need to modify all of the above. For Problem 1, only the paths variable needs to be modified.
        # If you do modify a variable you are not supposed to, you might notice different revenues outputted by the
        # Driver locally since the autograder will ignore the variables not relevant for the problem.

        paths = bfs_path(self.graph, self.isp, self.info["list_clients"])

        # try just updating bandwidths so all can get through
        for client, path in paths.items():
            for router in path:
                if router not in bandwidths:
                    bandwidths[router] = 1
                else:
                    bandwidths[router] += 1


        # newBandwidths = {}
        if(len(bandwidths) != len(self.info["bandwidths"])):
            print("ah fuck")
        # check new bandwidths against old, keep higher
        for router, band in self.info["bandwidths"].items():
            if router not in bandwidths:
                bandwidths[router] = band

            inputBandwidth = bandwidths[router]

            if inputBandwidth > band:
                bandwidths[router] = inputBandwidth
            else:
                bandwidths[router] = band

        # bandwidths = self.info["bandwidths"]


        # WARNING: DO NOT MODIFY THE LINE BELOW, OR BAD THINGS WILL HAPPEN
        return (paths, bandwidths, priorities)

