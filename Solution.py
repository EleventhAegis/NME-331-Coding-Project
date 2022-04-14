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

        # get the initial paths and bandwidths
        test = bfs_path(self.graph, self.isp, self.info["list_clients"])
        paths = bfs_path(self.graph, self.isp, self.info["list_clients"])

        # ####################################property to sort by################################################
        property_to_sort = "alphas"
        # #######################################################################################################

        # sort the initial returned client paths based on the property
        sorted_clients = self.sort_paths(paths, self.info[property_to_sort])

        # create temporary paths for storing final paths and graph so as not to damage the object's
        paths_temp = {}
        temp_bandwidths = self.info["bandwidths"]
        graph_temp = self.graph
        breakout = 0

        # run until all clients have received their packets
        while len(sorted_clients) != 0:

            # scan through each path of the clients and as each client uses a router subtract one from its bandwidth
            for client in sorted_clients:

                # go through all routers in the path and subtract 1 from band width
                for router in paths[client]:

                    # if a router's bandwidth were to drop below zero, remove router from graph and exit
                    if temp_bandwidths[router] == 0:
                        del graph_temp[client]
                        breakout = 1
                        break

                    # if bandwidth >= 0 then subtract 1
                    else:
                        temp_bandwidths[router] -= 1

                # if a router hits negative bandwidth
                if breakout == 1:
                    break

                # subtract the client from sorted clients and add to temp paths indicating packet is delivered
                sorted_clients.remove(client)
                paths_temp[client] = paths[client]

            # get new paths and bandwidths
            paths = bfs_path(graph_temp, self.isp, sorted_clients)
            temp_bandwidths = self.info["bandwidths"]
            print("calculating new bfs")

        # write temp_paths to paths for output
        paths = paths_temp

        # Note: You do not need to modify all of the above. For Problem 1, only the paths variable needs to be modified.
        # If you do modify a variable you are not supposed to, you might notice different revenues outputted by the
        # driver locally since the autograder will ignore the variables not relevant for the problem.
        # WARNING: DO NOT MODIFY THE LINE BELOW, OR BAD THINGS WILL HAPPEN

        return (test, bandwidths, priorities)

    # paths is the remaining paths to be sorted, trait is the parameter to be sorted by from the info structure
    def sort_paths(self, paths, trait):
        # create a list of all the routers being used
        routers = []
        for path in paths:
            for router in paths[path]:
                if router not in routers:
                    routers.append(router)

        # ############################need to finish this sorting algorithm#####################################

        # list to hold sorted values
        sorted_routers = []

        # temporary value to store router with smallest trait value
        smallest_router = 0
        smallest_router_value = -1

        # suuuuper basic sorting algorithm, loop until all routers removed from routers
        while len(routers) != 0:

            # loop over all routers left in routers
            for router in routers:

                # check if its a client or a router
                if router not in self.info["list_clients"]:
                    # if only a router remove from routers and continue
                    routers.remove(router)
                    continue

                # if no smallest value has been stored yet then store this value
                if smallest_router_value == -1:
                    smallest_router = router
                    smallest_router_value = trait[router]

                # otherwise compare router to previous smallest
                else:

                    # if smaller in regards to trait then replace previous best
                    if trait[router] < smallest_router_value:
                        smallest_router = router
                        smallest_router_value = trait[router]

            # append the router to smallest routers, which will sort them in ascending order
            # if you want the order in descending simply reverse order after sorting
            sorted_routers.append(smallest_router)
            routers.remove(smallest_router)
            smallest_router_value = -1

            # sorted_routers = sorted_routers[::-1]

        return sorted_routers
