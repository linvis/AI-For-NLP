import re
import networkx as nx
import matplotlib.pyplot as plt
from subway_spider import BJSubwaySpider
from station import Station


base_url = 'https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%81/408485#2_1'


def init_stations(url):
    spider = BJSubwaySpider(url)
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
        station.set_line(line)
        station.set_name(name)

        dis = dis_unit_trans(float(dis.group()))

        station.add_conn(conn, dis)
        all_stations.append(station)
    else:
        station = get_station_by_name(name, all_stations)

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


def show_graph(all_stations):
    all_conn_nodes = {}
    plt.interactive(False)

    for sta in all_stations:
        all_conn_nodes[sta.name] = sta.conn

    # g = nx.Graph(all_conn_nodes)
    # nx.draw(g)
    # plt.show()

    return all_conn_nodes


all_lines = init_stations(base_url)
for line, sta in all_lines.items():
    print(line)
    print(sta)
ALL_STATIONS = format_station(all_lines)
# for sta in ALL_STATIONS:
#     print(sta.conn)
#     print(sta.name)
#     print(sta.line)

graph = show_graph(ALL_STATIONS)


def my_navigation(start, end, graph):
    pathes = [[start], ]
    seen = []

    # at first, I put `path = []` here, it is wrong, path should be refresh in every loop

    while pathes:
        path = pathes.pop(0)
        print("current path: {}".format(path))

        node = path[-1]

        if node in seen: continue

        print("looking for {}".format(node))

        next_nodes = graph[node]

        for n in next_nodes:
            if n == end:
                path.append(n)
                return path
            pathes.append(path + [n])

        pathes = sorted(pathes, key=len)

        seen.append(node)





# print(get_station_by_name('俸伯', ALL_STATIONS).name)
print(graph['霍营'])
print(my_navigation('霍营', '亮马桥', graph))
