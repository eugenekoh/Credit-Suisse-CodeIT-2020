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
    
    graph_map = {}
    graph_map[originName] = []

    for name, genome in clusters.items():
        if name == originName:
            continue
        min_nodes = []
        min_diff = sys.maxsize
        dist_dict = {} 
        for name_other, genome_other in clusters.items():
            
            if name != name_other:
                diff_genome, non_silent = compare_diff(genome, genome_other)
                dist_dict[name_other] = [diff_genome, non_silent]
                if diff_genome <= min_diff and diff_genome != 0:
                    min_diff = diff_genome

        for dist_name, details in dist_dict.items():
            if details[0] == min_diff:
                min_nodes.append([dist_name, details[1]])
        graph_map[name] = min_nodes



    infected_map = []
    dist_dict = {} 
    min_diff = sys.maxsize
    for name, genome in clusters.items():
        diff_genome, non_silent = compare_diff(genome, infectedGenome)
        dist_dict[name] = [diff_genome, non_silent]
        if diff_genome <= min_diff:
            min_diff = diff_genome

    for name, details in dist_dict.items():
        if details[0] == min_diff:
            infected_map.append([name, details[1]])


    graph_map[infectedName] = infected_map
    paths = []

    next_nodes = infected_map
    for node in infected_map:
        paths.append([[infectedName], node])
        
    temp = paths.copy()
    sol = []

    while len(temp) > 0:
        for index in range(len(paths)):
            path = paths[index]
            last_node = path[-1]
            
            if type(last_node) == str: 
                next_nodes = graph_map[last_node]
            else:
                next_nodes = graph_map[last_node[0]]

            if len(next_nodes) == 0: 
                sol.append(path)
                temp.remove(path)
            elif len(next_nodes) == 1:
                
                path.append(next_nodes[0])
                temp[index] = path

            else:
                path.append(next_nodes[0])
                for node in next_nodes[1:]:
                    new_path = path.copy()
                    new_path.append(node)
                    temp.append(new_path)

        paths = temp.copy()
    

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

    # graph = {}
    # graph[originName] = []
    # # build graph of minimum clusters
    # for clusterName, clusterGenome in clusters.items():
    #     # do not process origin
    #     if clusterName == originName:
    #         continue
    #     minimunClusters = []
    #     minDiff = sys.maxsize
    #     distanceBtwClusters = {}
    #     for nextName, nextGenome in clusters.items():
    #         # skip own cluster
    #         if clusterName != nextName:
    #             thisGenome, thisSilent = compare_diff(clusterGenome, nextGenome)
    #             distanceBtwClusters[nextName] = [thisGenome, thisSilent]
    #             if thisGenome <= minDiff and thisGenome != 0:
    #                 minDiff = thisGenome

    #     # iterate the distance between clusters to append to minimum clusters
    #     for name, detailArr in distanceBtwClusters.items():
    #         if detailArr[0] == minDiff:
    #             minimunClusters.append([name,detailArr[1]])
    #     graph[clusterName] = minimunClusters

    
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
    diff = 0
    silent = True
    silentCount = 0
    for i in range(len(x)):
        if x[i] != y[i]:
            for c in range(len(clusterGenome[i])):
                if clusterGenome[i][c] != infectedGenome[i][c]:
                    if c == 0:
                        silentCount += 1
                    if c != 0:
                        silent = False
                    diff += 1
        if silentCount <= 1:
            silent = False
    return diff, silent

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





