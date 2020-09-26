import logging
import json
import sys

from flask import request, jsonify;

from codeitsuisse import app;


logger = logging.getLogger(__name__)

@app.route('/contact_trace', methods=['POST'])
def evaluate_contact_tracing():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    infected = data.get("infected")
    origin = data.get("origin")
    cluster = data.get("cluster")
    infectedName = infected.get("name")
    infectedGenome = infected.get("genome").split("-")
    originName = origin.get("name")
    originGenome = origin.get("genome").split("-")
    response = []

    clusters = {}
    clusters[originName] = originGenome
    for node in cluster:
        clusterGenome = node.get("genome").split("-")
        clusterName = node.get("name")
        clusters[clusterName] = clusterGenome
    # find the first point of entry first
    firstEntriesGenome, firstEntriesSilent = compare_min_diff(infectedGenome, clusters)
    for i in range(len(firstEntriesGenome)):
        clusterName = firstEntriesGenome[i]
        clusterSilent = firstEntriesSilent[i]
        # means end of the trace as ends with origin
        if clusterName == originName:
            if clusterSilent:
                s = "{}* -> {}".format(infectedName, originName)
                response.append(s)
            else:
                s = "{} -> {}".format(infectedName, originName)
                response.append(s)
        # not end of the trace so need continue tracing 
        else:
            element = clusters.pop(clusterName)
            s = ""
            if clusterSilent:
                s = "{}* -> {}".format(infectedName, clusterName)
            else:
                s = "{} -> {}".format(infectedName, clusterName)
            # find all paths starting with clusterName
            find_path(originName, originGenome, element, clusters, s, response)
            # add back cluster name for next iteration
            clusters[clusterName] = element
    
    logging.info("My result :{}".format(response))
    return jsonify(response)

def find_path(originName, originGenome, node, clusters, s, response):
    nextEntriesGenome, nextEntriesSilent = compare_min_diff(node, clusters)
    for i in range(len(nextEntriesGenome)):
        clusterName = nextEntriesGenome[i]
        clusterSilent = nextEntriesSilent[i]
        # means end of the trace as ends with origin
        if clusterName == originName:
            if node == originGenome:
                response.append(s)
                continue
            if clusterSilent:
                s = "{}* -> {}".format(s, originName)
                response.append(s)
            else:
                s = "{} -> {}".format(s, originName)
                response.append(s)
        # not end of the trace so need continue tracing 
        else:
            element = clusters.pop(clusterName)
            if clusterSilent:
                s = "{}* -> {}".format(s, clusterName)
            else:
                s = "{} -> {}".format(s, clusterName)
            # find all paths starting with clusterName
            find_path(clusterName, originName, clusters, s)
            # add back cluster name for next iteration
            clusters[clusterName] = element




def compare_min_diff(infectedGenome, comparators):
    minDiff = sys.maxsize 
    minGenome = []
    minSilent = []
    for clusterName, clusterGenome in comparators.items():
        diff = 0
        silent = True
        silentCount = 0
        for i in range(len(clusterGenome)):
            if clusterGenome[i] != infectedGenome:
                for c in range(len(clusterGenome[i])):
                    if clusterGenome[i][c] != infectedGenome[i][c]:
                        if c == 0:
                            silentCount += 1
                        if c != 0:
                            silent = False
                        diff += 1
        if diff < minDiff:
            minDiff = diff
            minGenome = [clusterName]
            if silentCount <= 1:
                silent = False
            if not silent:
                minSilent = [False]
            else:
                minSilent = [True]
        elif diff == minDiff:
            minGenome.append(clusterName)
            if not silent:
                minSilent.append(False)
            else:
                minSilent.append(True)
    return minGenome, minSilent
        


    # minDiff = sys.maxsize 
    # minGenome = ""
    # minSilent = True
    # clusters = {}
    # clusters[originName] = originGenome
    # for node in cluster:
    #     clusterGenome = node.get("genome").split("-")
    #     clusterName = node.get("name")
    #     clusters[clusterName] = clusterGenome
    
    # while len(clusters) > 0:
    #     for clusterName, clusterGenome in clusters.items():
    #         if clusterGenome == infectedGenome:
    #             s = "{} -> {}".format(infectedName, clusterName)
    #             response.append(s)
    #             clusters.pop(clusterName)
    #             continue
    #         diff = 0
    #         silent = True
    #         silentCount = 0
    #         for i in range(len(clusterGenome)):
    #             if clusterGenome[i] != infectedGenome:
    #                 for c in range(len(clusterGenome[i])):
    #                     if clusterGenome[i][c] != infectedGenome[i][c]:
    #                         if c == 0:
    #                             silentCount += 1
    #                         if c != 0:
    #                             silent = False
    #                         diff += 1
    #         if diff < minDiff:
    #             minDiff = diff
    #             minGenome = clusterName
    #             if silentCount <= 1:
    #                 silent = False
    #             if silent:
    #                 minSilent = False



   
    # for node in cluster:
    #     clusterName = node.get("name")
    #     clusters.pop(clusterName)
    #     clustersMinimums[clusterName], clustersSilence[clusterName] = compare_min_diff(node, clusters)
    #     clusters[clusterName] = clusterGenome



