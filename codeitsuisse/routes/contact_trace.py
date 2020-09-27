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
    # add all cluster into a map including origin
    clusters[originName] = originGenome
    for n in cluster:
        clusterGenome = n.get("genome").split("-")
        clusterName = n.get("name")
        clusters[clusterName] = clusterGenome
    
    graph = {}
    graph[originName] = []

    for name, genome in clusters.items():
        if name == originName:
            continue
        minClusters = []
        minDiff = sys.maxsize
        distanceHashMap = {} 
        for nextName, nextGenome in clusters.items():
            
            if name != nextName:
                diffGenome, silent = compare_diff(genome, nextGenome)
                distanceHashMap[nextName] = [diffGenome, silent]
                if diffGenome <= minDiff and diffGenome != 0:
                    minDiff = diffGenome

        for name, details in distanceHashMap.items():
            if details[0] == minDiff:
                minClusters.append([name, details[1]])
        graph[name] = minClusters



    infectedGraph = []
    distanceHashMap = {} 
    minDiff = sys.maxsize
    for name, genome in clusters.items():
        diffGenome, silent = compare_diff(genome, infectedGenome)
        distanceHashMap[name] = [diffGenome, silent]
        if diffGenome <= minDiff:
            minDiff = diffGenome

    for name, details in distanceHashMap.items():
        if details[0] == minDiff:
            infectedGraph.append([name, details[1]])


    graph[infectedName] = infectedGraph
    traces = []

    nextCluster = infectedGraph
    for n in infectedGraph:
        traces.append([[infectedName], n])
        
    copyTrace = traces.copy()
    sol = []

    while len(copyTrace) > 0:
        for index in range(len(traces)):
            trace = traces[index]
            lastCluster = trace[-1]
            
            if type(lastCluster) == str: 
                nextCluster = graph[lastCluster]
            else:
                nextCluster = graph[lastCluster[0]]

            if len(nextCluster) == 0: 
                sol.append(trace)
                copyTrace.remove(trace)
            elif len(nextCluster) == 1:
                
                trace.append(nextCluster[0])
                copyTrace[index] = trace

            else:
                trace.append(nextCluster[0])
                for node in nextCluster[1:]:
                    new_path = trace.copy()
                    new_path.append(node)
                    copyTrace.append(new_path)

        traces = copyTrace.copy()
    

    for s in sol:
        res = ""
        for n in s:
            if len(n) == 1:
                res += n[0]
            else:
                if n[1] == True:
                    res = "{}*".format(res)
                res = "{} -> {}".format(res, n[0])
        response.add(res)

    
    # startGraph = []
    # distanceBtwClusters = {}
    # minDiff = sys.maxsize
    
    # # put to the starting point from first infected node
    # for nextName, nextGenome in clusters.items():
    #     diffNum, silent = compare_diff(nextGenome, infectedGenome)
    #     distanceBtwClusters[nextName] = [diffNum, silent]
    #     if diffNum <= minDiff:
    #         minDiff = min(diffNum, minDiff)

    # for name, details in distanceBtwClusters.items():
    #     if details[0] == minDiff:
    #         startGraph.append([name, details[1]])

    # graph[infectedName] = startGraph
    # possibleTraces = []
    # nextClusters = startGraph

    # for cluster in startGraph:
    #     possibleTraces.append([[infectedName], cluster])

    # iterateTraces = possibleTraces.copy()
    # sol = []

    # while len(iterateTraces) > 0:
    #     for i in range(len(possibleTraces)):
    #         trace = possibleTraces[i]
    #         if type(trace[-1]) == str:
    #             nextClusters = graph[trace[-1]]
    #         else:
    #             nextClusters = graph[trace[-1][0]]
    #         if len(trace[-1]) == 0:
    #             sol.append(trace)
    #             iterateTraces[i] = trace
    #         elif len(trace[-1]) == 1:
    #             trace.append(trace[-1][0])
    #             iterateTraces[i] = trace
    #         else:
    #             trace.append(trace[-1][0])
    #             for n in trace[-1][1:]:
    #                 newTraces = trace.copy()
    #                 newTraces.append(n)
    #                 iterateTraces.append(newTraces)
    #     possibleTraces = iterateTraces.copy()

    #     for s in sol:
    #         res = ""
    #         for n in s:
    #             if len(n) == 1:
    #                 res += n[0]
    #             else:
    #                 if n[1] == True:
    #                     res = "{}*".format(res)
    #                 res = "{} -> {}".format(res, n[0])
    #         response.add(res)


                
        
    # firstEntriesGenome, firstEntriesSilent, nextEntriesDiff = compare_minDiff(infectedName, infectedGenome, clusters)
    # for i in range(len(firstEntriesGenome)):
    #     clusterName = firstEntriesGenome[i]
    #     clusterSilent = firstEntriesSilent[i]
    #     # means end of the trace as ends with origin
    #     if clusterName == originName:
    #         if clusterSilent:
    #             s = "{}* -> {}".format(infectedName, originName)
    #             response.add(s)
    #         else:
    #             s = "{} -> {}".format(infectedName, originName)
    #             response.add(s)
    #     # not end of the trace so need continue tracing 
    #     else:
    #         element = clusters.get(clusterName)
    #         s = ""
    #         if clusterSilent:
    #             s = "{}* -> {}".format(infectedName, clusterName)
    #         else:
    #             s = "{} -> {}".format(infectedName, clusterName)
    #         if element == originGenome:
    #             response.add(s)
    #             continue
    #         # find all possibleTraces starting with clusterName
    #         find_trace(clusterName, originName, originGenome, element, clusters, s, response)
    #         # add back cluster name for next iteration
    #         # clusters[clusterName] = element
    
    logging.info("My result :{}".format(response))
    return jsonify(list(response))


def compare_diff(x, y):
    diffGenome = 0 
    first_char_diff_genome = 0 
    silent = False

    for index in range(len(x)):
        if x[index] != y[index]:
            x_instr = list(x[index])
            y_instr = list(y[index])

            # compare number of difference in instructions
            diff = 0
            first_char_diff = 0

            for char_index in range(len(instr1)):
                
                if instr1[char_index] != instr2[char_index]:
                    if char_index == 0:
                        first_char_diff += 1
                    diff += 1
            diff_instr = [diff, first_char_diff]
            diff_instr = compare_instr(x_instr, y_instr)
            diffGenome += diff_instr[0]
            first_char_diff_genome += diff_instr[1]
    if first_char_diff_genome > 1:
        silent = True
    
    return diffGenome, silent


# def find_trace(name, originName, originGenome, node, clusters, s, response):
#     nextEntriesGenome, nextEntriesSilent, nextEntriesDiff = compare_minDiff(name, node, clusters)
#     for i in range(len(nextEntriesGenome)):
#         clusterName = nextEntriesGenome[i]
#         clusterSilent = nextEntriesSilent[i]
#         if nextEntriesDiff == 0:
#             continue
#         # means end of the trace as ends with origin
#         if clusterName == originName:
#             if clusterSilent:
#                 sol = "{}* -> {}".format(s, originName)
#                 response.add(sol)
#             else:
#                 sol = "{} -> {}".format(s, originName)
#                 response.add(sol)
#         # not end of the trace so need continue tracing 
#         else:
#             if node == originGenome:
#                 response.addd(s)
#                 continue
#             # element = clusters.pop(clusterName)
#             if clusterSilent:
#                 s = "{}* -> {}".format(s, clusterName)
#             else:
#                 s = "{} -> {}".format(s, clusterName)
#             # find all possibleTraces starting with clusterName
#             find_trace(originName, originGenome, element, clusters, s, response)
#             # add back cluster name for next iteration
#             # clusters[clusterName] = element




# def compare_minDiff(infectedName, infectedGenome, comparators):
#     minDiff = sys.maxsize 
#     minGenome = []
#     minSilent = []
#     diffArr = []
#     for clusterName, clusterGenome in comparators.items():
#         if clusterName == infectedName:
#             continue
#         diff = 0
#         silent = True
#         silentCount = 0
#         for i in range(len(clusterGenome)):
#             if clusterGenome[i] != infectedGenome[i]:
#                 for c in range(len(clusterGenome[i])):
#                     if clusterGenome[i][c] != infectedGenome[i][c]:
#                         if c == 0:
#                             silentCount += 1
#                         if c != 0:
#                             silent = False
#                         diff += 1
#         if diff < minDiff:
#             minDiff = diff
#             minGenome = [clusterName]
#             if silentCount <= 1:
#                 silent = False
#             if not silent:
#                 minSilent = [False]
#             else:
#                 minSilent = [True]
#             diffArr.append(diff)
#         elif diff == minDiff:
#             if silentCount <= 1:
#                 silent = False
#             minGenome.append(clusterName)
#             if not silent:
#                 minSilent.append(False)
#             else:
#                 minSilent.append(True)
#             diffArr.append(diff)
#     return minGenome, minSilent, diffArr
        


    
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





