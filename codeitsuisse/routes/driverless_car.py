# import logging
# import json
# import networkx
# from flask import request, jsonify
# from shapely import LineString
# from codeitsuisse import app
# import networkx as nx
# logger = logging.getLogger(__name__)

# @app.route('/driverless-car', methods=['POST'])
# def evaluate_driverless_car():
#     data = request.get_json()
#     logging.info("data sent for evaluation {}".format(data))
#     vehicle = data["vehicle"]
#     roads = data["roads"]
#     start = data["start"]
#     end = data["end"]
#     graph = constructGraph(roads)
#     results = {}
#     logging.info("result :{}".format(results))

#     return jsonify(results)


# def constructGraph(roads,start,end):
#     G = nx.Graph()

#     for i in range(len(roads)):
#         r1_name = roads[i]["name"]
#         r1x1 = roads[i]['from']['x']
#         r1y1 = roads[i]['from']['y']
#         r1x2 = roads[i]['to']['x']
#         r1y2 = roads[i]['to']['y']
#         r1_type = roads[i]['type']
#         max_speed1 = roads[i]['maxSpeed']
#         if r1_type == "street":
#             length1 = abs(r1y2 - r1y1)
#         else:
#             length1 = abs(r1x2 - r1x1)
#         r1 = LineString([(r1x1, r1y1),(r1x2,r1y2)])
#         G.add_node((r1_name,{"type":r1_type,"length":length1, "maxSpeed":max_speed1, "zones": roads[i]['zones']}))
#         for j in range(i+1,len(roads)):
#             r2_name = roads[j]['name']
#             r2x1 = roads[j]['from']['x']
#             r2y1 = roads[j]['from']['y']
#             r2x2 = roads[j]['to']['x']
#             r2y2 = roads[j]['to']['y']
#             r2_type = roads[j]['type']
#             max_speed2 = roads[j]['maxSpeed']
#             if r2_type == "street":
#                 length2 = abs(r2y2 - r2y1)
#             else:
#                 length2 = abs(r2x2 - r2x1)
#             r2 = LineString([(r2x1,r2y1),(r2x2,r2y2)])
#             G.add_node((r2_name,{"type":"street","length":length2, "maxSpeed":max_speed2, "zones": roads[j]['zones']}))

#             if r1.intersects(r2):
#                 G.add_edge(r1_name,r2_name)
#     return G

# def getDistFromSpeedAcc(u, v, a):
#     s = (v**2 - u**2) / (2*a)

# def computeTime(node, acc, dec, topSpeed):

#     getDistFromSpeedAcc

# def processZones(x1, x2, zones):
#     zone_tuples = []
#     for zone in zones:
#         x1, y1, x2, y2 = zone['from']['x'], zone['from']['y'], zone['to']['x'], zone['to']['y']
#         u = zone['maxSpeed']
#         zone_tuples.append((x1,y1,x2,y2,u))
        

