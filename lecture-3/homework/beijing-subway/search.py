import re
import networkx as nx
import matplotlib.pyplot as plt
from subway_spider import SpiderBaidu, SpiderOffice
from station import Station


baidu_url = 'https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%81/408485#2_1'
office_url = 'http://www.bjsubway.com/station/zjgls/'


def init_stations(url, spider):
    if spider == 'baidu':
        spider = SpiderBaidu(url)
    if spider == 'office':
        spider = SpiderOffice(url)

    return spider.process()


def get_station_by_name(name, all_stations):
    for sta in all_stations:
        if name == sta.name:
            return sta

    return None


def put_station_in_list(all_stations, *args):

    dis_unit_trans = lambda dis : dis / 1000 if dis > 10 else dis

    if len(args) < 4:
        return

    name = args[0]
    line = args[1]
    conn = args[2]
    dis = args[3]

    if get_station_by_name(name, all_stations) == None:
        station = Station()
        station.add_line(line)
        station.set_name(name)

        dis = dis_unit_trans(float(dis.group()))

        station.add_conn(conn, dis)
        all_stations.append(station)
    else:
        station = get_station_by_name(name, all_stations)
        station.add_line(line)

        dis = dis_unit_trans(float(dis.group()))

        station.add_conn(conn, dis)



def format_station(all_lines):
    all_stations = []

    for line, nodes in all_lines.items():
        if nodes == None:
            continue

        for conn_node in nodes:
            # get start and end
            node = re.search("([\u4e00-\u9fff]+).*[～|~|——]([\u4e00-\u9fff]+)", str(conn_node[0]))
            dis = re.search("(\d+|[0-9]{1,}[.][0-9]*)", str(conn_node[1]))
            if node and dis:

                name = node.group(1)
                put_station_in_list(all_stations, name, line, node.group(2), dis)

                name = node.group(2)
                put_station_in_list(all_stations, name, line, node.group(1), dis)

            # print(conn_node[0])
            # print(conn_node[1])
            # new_station = Station(line)
    return all_stations


def show_graph(all_stations, show):
    all_conn_nodes = {}
    plt.interactive(False)

    for sta in all_stations:
        all_conn_nodes[sta.name] = sta.conn

    g = nx.Graph(all_conn_nodes)
    if show:
        nx.draw(g)
        plt.show()

    return all_conn_nodes


def less_distance(path):

    sum_dis = 0.0
    for i in range(len(path) - 1):
        station= get_station_by_name(path[i], ALL_STATIONS)
        sum_dis += station.get_conn_dis(path[i + 1])

    return sum_dis


def less_lines(path):
    latest_line = []
    latest_station = None

    for i in range(len(path)):
        station = get_station_by_name(path[i], ALL_STATIONS)
        if latest_station == None:
            latest_station = station
        else:
            line = list(set(station.line) & set(latest_station.line))[0]
            if line not in latest_line:
                latest_line.append(line)
            latest_station = station

    return len(latest_line), latest_line


def navigation(start, end, graph, *strategy):
    pathes = [[start], ]
    seen = []

    if len(strategy) > 2:
        print("too many strategy")

    while pathes:
        path = pathes.pop(0)
        # print("current path: {}".format(path))

        node = path[-1]

        if node in seen: continue

        # print("looking for {}".format(node))

        next_nodes = graph[node]

        for n in next_nodes:
            if n == end:
                path.append(n)
                print("sum distance {}".format(less_distance(path)))
                print("sum lines {}".format(less_lines(path)))
                return path
            pathes.append(path + [n])

        # python not supported between instances of 'generator' and 'generator'
        # pathes = sorted(pathes, key=lambda p :(strat(p) for strat in strategy)) is not allowed
        if len(strategy) > 1:
            pathes = sorted(pathes, key=lambda p :(strategy[0](p), strategy[1](p)))
        else:
            pathes = sorted(pathes, key=lambda p :(strategy[0](p)))

        seen.append(node)


# all_lines = init_stations(baidu_url, 'baidu')
all_lines = init_stations(office_url, 'office')
# print(all_lines)
# for line, sta in all_lines.items():
#     print(line)
#     print(sta)
ALL_STATIONS = format_station(all_lines)
# for sta in ALL_STATIONS:
#     print("name is {}".format(sta.name))
#     print("conn is {}".format(sta.conn))
#     print("line is {}".format(sta.line))

graph = show_graph(ALL_STATIONS, False)

# less stations transfer
print("----------less stations transfer-----------")
print(navigation('霍营', '亮马桥', graph, len))
# less distances
print("----------less distances-----------")
print(navigation('霍营', '亮马桥', graph, less_distance))
# less lines transfer
print("----------less lines transfer-----------")
print(navigation('霍营', '亮马桥', graph, less_lines))
# less lines transfer and less distance
# so this is the best one
print("----------less lines transfer and less distance-----------")
print(navigation('霍营', '亮马桥', graph, less_lines, less_distance))
