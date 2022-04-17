#!/usr/bin/env python3

import pybgpstream
import re

"""Code file for CS 6250 BGPM Project

Edit this file according to the provided docstrings and assignment description. 
Do not change the existing function name or arguments.
You may add additional functions but they need to be contained entirely in this file.
"""

def calculateUniquePrefixes(cache_files):
    """Retrieve the number of unique IP prefixes from input BGP data files.

    Args:
        cache_files: A list of files.

    Returns:
        A list containing the number of unique IP prefixes for each input file.
        For example: [2, 5]
    """
    soln = list()
    for cache_file in cache_files:
        stream = pybgpstream.BGPStream(data_interface = "singlefile", filter = "ipv 4")
        unique_ips = set()
        stream.set_data_interface_option("singlefile", "rib-file", cache_file)
        for rec in stream.records():
            for elem in rec: 
                pfx = elem.fields["prefix"]
                unique_ips.add(pfx)
        soln.append(len(unique_ips))
    return soln



def split_helper(path):
    soln = set()
    s = ""
    i = 0
    while i < len(path):
        if path[i] == ' ':
            if s != "":
                soln.add(s)
            s = ""
        elif path[i] == '{':
            i+=1
            while path[i] != '}' and i < len(path):
                s+=path[i]
                i+=1
            soln.add(s)
            s = ""
        else:
            s += path[i]
        i+=1
    return soln
                

def calculateUniqueAses(cache_files):
    """Retrieve the number of unique ASes from input BGP data files.

    Args:
        cache_files: A list of files.

    Returns:
        A list containing the number of the number of unique AS for each input file.
        For example: [2, 5]
    """
    soln = list()
    for cache_file in cache_files:
        unique_ases = set()
        stream = pybgpstream.BGPStream(data_interface = "singlefile", filter = "ipv 4")
        stream.set_data_interface_option("singlefile", "rib-file", cache_file)
        for rec in stream.records():
            for elem in rec: 
                # path1 = elem.fields["as-path"]
                # unique_ases.update(split_helper(path1))
                result = re.search('{(.\*)}', elem.fields["as-path"])
                if result != None:
                    unique_ases.add(result.group(1))
                    elem.fields["as-path"] = re.sub(result.group(0), "", elem.fields["as-path"])
                pfx = elem.fields["as-path"].split(" ")
                if len(pfx) > 1:
                    for i in pfx:
                        unique_ases.add(i)
        soln.append(len(unique_ases))  
    return soln



# unique = list()
#     for cache in cache_files:
    
#         stream = pybgpstream.BGPStream(data_interface="singlefile", filter = "ipv 4")
#         stream.set_data_interface_option("singlefile", "rib-file", cache)
#         em = set()
#         for rec in stream.records():
#             for elem in rec:

#                 result = re.search('{(.\*)}', elem.fields["as-path"])
#                 if result != None:

#                     em.add(result.group(1))
#                     elem.fields["as-path"] = re.sub(result.group(0), "", elem.fields["as-path"])
#                 pfx = elem.fields["as-path"].split(" ")
#                 if len(pfx) > 1:
#                     for i in pfx:
#                         em.add(i)
#         unique.append(len(em))














def examinePrefixes(cache_files):
    """A list of the top 10 origin ASes according to percentage increase of the advertised prefixes.

    Args:
        cache_files: A list of files.

    Returns:
        A list of the top 10 origin ASes according to percentage increase of the advertised prefixes from lowest to highest.
        For example: ["777", "1", "6"]
        corresponds to AS "777" as having the smallest percentage increase (of the top ten) and AS "6" having the highest increase (of the top ten).
        AS numbers should be strings.
    """
    # soln = list()
    # results = dict()
    # for cache_file in cache_files:
    #     stream = pybgpstream.BGPStream(data_interface = "singlefile", filter = "ipv 4")
    #     stream.set_data_interface_option("singlefile", "rib-file", cache_file)
    #     prefix_origin = defaultdict(set)
    #     for rec in stream.records():
    #         for elem in rec:
    #             # Get the prefix
    #             pfx = elem.fields["prefix"]
    #             # Get the list of ASes in the AS path
    #             ases = elem.fields["as-path"].split(" ")
    #             if len(ases) > 0:
    #                 # Get the origin ASn (rightmost)
    #                 origin = ases[-1]
    #                 # Insert the origin ASn in the set of
    #                 # origins for the prefix
    #                 prefix_origin[pfx].add(origin)

    #     # Print the list of MOAS prefix and their origin ASns
    #     for pfx in prefix_origin:
    #         if results.get(pfx) == None
    #             results[pfx] = 1
    #         else
    #             results[pfx] = results[pfx] + 1

    # {k: v for k, v in sorted(x.items(), key=lambda item: item[1])}
    # for i in range(0,10):
    #     soln.add(results.popitem())

    # return soln


def calculateShortestPath(cache_files):
    """Compute the shortest AS path length for every origin AS from input BGP data files.

    Retrieves the shortest AS path length for every origin AS for every input file.
    Your code should return a dictionary where every key is the AS string and every value associated with the key is
    a list of the shortest path lengths for that AS.

    Note: For any AS that is not present in every input file, fill the corresponding entry in its list with a zero.
    Every value in the dictionary should have the same length.

    Args:
        cache_files: A list of files.

    Returns:
        A dictionary where every key is the AS and every value associated with the key is a list of the shortest path
        lengths for that AS, for every input file.
        For example: {"455": [4, 2, 3], "533": [4, 1, 2]}
        corresponds to the AS "455" with the shortest path lengths 4, 2 and 3 and the AS "533" with the shortest paths 4, 1 and 2.
        AS numbers should be strings.
    """

    return {}


def calculateRTBHDurations(cache_files):
    """Identify blackholing events and compute the duration of all RTBH events from input BGP data files.

    Identify events where the IPV4 prefixes are tagged with at least one Remote Triggered Blackholing (RTBH) community.

    Args:
        cache_files: A list of files.

    Returns:
        A dictionary where each key is a peerIP and each value is another dictionary with key equal to a prefix and each
        value equal to a list of explicit RTBH event durations.
        For example: {"127.0.0.1": {"12.13.14.0/24": [4.0, 1.0, 3.0]}}
        corresponds to the peerIP "127.0.0.1", the prefix "12.13.14.0/24" and event durations of 4.0, 1.0 and 3.0.
        AS numbers should be strings.
    """

    return {}


def calculateAWDurations(cache_files):
    """Identify Announcement and Withdrawal events and compute the duration of all explicit AW events in the input data.

    Args:
        cache_files: A list of files.

    Returns:
        A dictionary where each key is a peerIP and each value is another dictionary with key equal to a prefix and each
        value equal to a list of explicit AW event durations.
        For example: {"127.0.0.1": {"12.13.14.0/24": [4.0, 1.0, 3.0]}}
        corresponds to the peerIP "127.0.0.1", the prefix "12.13.14.0/24" and event durations of 4.0, 1.0 and 3.0.
        AS numbers should be strings.
    """

    return {}

# The main function will not be run during grading.
# You may use it however you like during testing.
#
# NB: make sure that check_solution.py runs your
#     solution without errors prior to submission
if __name__ == '__main__':
    # do nothing
    pass
