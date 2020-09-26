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
    response = set()

    clusters = {}
    clusters[originName] = originGenome
    for node in cluster:
        clusterGenome = node.get("genome").split("-")
        clusterName = node.get("name")
        clusters[clusterName] = clusterGenome
    # find the first point of entry first
    # graph = {}
    # graph[originName] = []
    # # build graph of minimum clusters
    # for clusterName, clusterGenome in clusters.items():
    #     # do not process origin
    #     if name == originName:
    #         continue
    #     minimunClusters = []
    #     minDiff = sys.maxsize
    #     distanceBtwClusters = {}
    #     for nextName, nextGenome in clusters.items():
    #         # skip own cluster
    #         if clusterName != nextName:
    #             thisGenome, thisSilent = compare_min_diff(clusterGenome, nextGenome)
    #             distanceBtwClusters[nextName] = [thisGenome, thisSilent]
    #             if thisGenome <= minDiff and thisGenome != 0:
    #                 minDiff = thisGenome

    #     # iterate the distance between clusters to append to minimum clusters
    #     for name, detailArr in distanceBtwClusters.items():
    #         if 
                
        
    firstEntriesGenome, firstEntriesSilent, nextEntriesDiff = compare_min_diff(infectedName, infectedGenome, clusters)
    for i in range(len(firstEntriesGenome)):
        clusterName = firstEntriesGenome[i]
        clusterSilent = firstEntriesSilent[i]
        # means end of the trace as ends with origin
        if clusterName == originName:
            if clusterSilent:
                s = "{}* -> {}".format(infectedName, originName)
                response.add(s)
            else:
                s = "{} -> {}".format(infectedName, originName)
                response.add(s)
        # not end of the trace so need continue tracing 
        else:
            element = clusters.get(clusterName)
            s = ""
            if clusterSilent:
                s = "{}* -> {}".format(infectedName, clusterName)
            else:
                s = "{} -> {}".format(infectedName, clusterName)
            if element == originGenome:
                response.add(s)
                continue
            # find all paths starting with clusterName
            find_path(clusterName, originName, originGenome, element, clusters, s, response)
            # add back cluster name for next iteration
            # clusters[clusterName] = element
    
    logging.info("My result :{}".format(response))
    return jsonify(list(response))

def find_path(name, originName, originGenome, node, clusters, s, response):
    nextEntriesGenome, nextEntriesSilent, nextEntriesDiff = compare_min_diff(name, node, clusters)
    for i in range(len(nextEntriesGenome)):
        clusterName = nextEntriesGenome[i]
        clusterSilent = nextEntriesSilent[i]
        if nextEntriesDiff == 0:
            continue
        # means end of the trace as ends with origin
        if clusterName == originName:
            if clusterSilent:
                sol = "{}* -> {}".format(s, originName)
                response.add(sol)
            else:
                sol = "{} -> {}".format(s, originName)
                response.add(sol)
        # not end of the trace so need continue tracing 
        else:
            if node == originGenome:
                response.addd(s)
                continue
            # element = clusters.pop(clusterName)
            if clusterSilent:
                s = "{}* -> {}".format(s, clusterName)
            else:
                s = "{} -> {}".format(s, clusterName)
            # find all paths starting with clusterName
            find_path(originName, originGenome, element, clusters, s, response)
            # add back cluster name for next iteration
            # clusters[clusterName] = element




def compare_min_diff(infectedName, infectedGenome, comparators):
    minDiff = sys.maxsize 
    minGenome = []
    minSilent = []
    diffArr = []
    for clusterName, clusterGenome in comparators.items():
        if clusterName == infectedName:
            continue
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
            diffArr.append(diff)
        elif diff == minDiff:
            if silentCount <= 1:
                silent = False
            minGenome.append(clusterName)
            if not silent:
                minSilent.append(False)
            else:
                minSilent.append(True)
            diffArr.append(diff)
    return minGenome, minSilent, diffArr
        


    
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



