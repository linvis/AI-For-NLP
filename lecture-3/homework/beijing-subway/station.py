

class Station:
    def __init__(self):
        self.line = []
        self.name = ''
        self.conn = []
        self.dis = {}

    def add_line(self, line):
        if line not in self.line:
            self.line.append(line)

    def set_name(self, name):
        self.name = name

    def add_conn(self, name, dis):
        self.conn.append(name)
        self.dis[name] = dis

    def get_conn_dis(self, conn_name):
        return self.dis[conn_name]
