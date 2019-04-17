from bs4 import BeautifulSoup
import requests
import re

SESSIONS_HEADER='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'

class BJSubwaySpider():
    def __init__(self, url):
        self.url = url

    def get_html(self, url, encoding):
        session = requests.Session()
        session.headers['User-Agent'] = SESSIONS_HEADER
        html = session.get(url)
        html.encoding = encoding
        return html.text

    def get_all_station(self, lines):
        pass

    def process(self):
        pass


class SpiderBaidu(BJSubwaySpider):
    def __init__(self, url):
        BJSubwaySpider.__init__(self, url)

    def get_html(self, url):
        return BJSubwaySpider.get_html(self, url, 'utf-8')

    def get_subway_lines(self, html):
        lines = {}
        soup = BeautifulSoup(html, "html.parser")
        contents = soup.find_all('a', {"target": "_blank"})
        for content in contents:
            ret = re.search("a href=\"(.*)\" target=\"_blank\">(北京地铁.*线)<\/a>", str(content))
            if ret:
                lines[ret.group(2)] = ret.group(1)
                # print(ret.group(1) + ret.group(2))
        return lines

    def get_station_distances(self, html):
        distances = []
        soup = BeautifulSoup(html, "html.parser")
        contents = soup.find_all('table')
        target_content = ''
        for content in contents:
            if re.search("(.*相邻站间距信息统计表.*|.*站区间.*)", str(content)):
                target_content = str(content)
                break
        # print(target_content)
        if target_content == '':
            return None

        pattern = ">([^\x00-\xff]*[～|~|——].*?)<.*?>(\d+|\d+米|[0-9]{1,}[.][0-9]*)<\/td>"
        distances = re.findall(pattern, target_content)
        if distances:
            return distances
        else:
            return None

    # all_lines = {line:[("sta-sta",dis)...]}
    def get_all_station(self, lines):
        all_lines = {}
        for line, link in lines.items():
            url = 'https://baike.baidu.com' + link
            html = self.get_html(url)
            station_distances = self.get_station_distances(html)
            all_lines[line] = station_distances
        return all_lines


    def process(self):
        html = self.get_html(self.url)
        # print(html[:500])
        lines = self.get_subway_lines(html)
        return self.get_all_station(lines)


# base_url = 'https://baike.baidu.com/item/%E5%8C%97%E4%BA%AC%E5%9C%B0%E9%93%81/408485#2_1'
# spider = BJSubwaySpider(base_url)
# print(spider.process())


class SpiderOffice(BJSubwaySpider):
    def __init__(self, url):
        BJSubwaySpider.__init__(self, url)

    def get_html(self, url):
        return BJSubwaySpider.get_html(self, url, 'gbk')

    def get_all_station(self, lines):
        all_lines = {}
        html = lines
        soup = BeautifulSoup(html, "html.parser")
        contents = soup.find_all('div', {"class": "con_text"})
        for content in contents:
            ret = re.findall(">(.*)相邻站间距信息统计表<.|\n*([\u4e00-\u9fff|\w]*——[\u4e00-\u9fff|\w]*).*\n.*?(\d+)<\/td>",
                             str(content))
            if ret:
                stations = []
                for i in range(1, len(ret)):
                    stations.append((ret[i][1], ret[i][2]))
                all_lines[ret[0][0]] = stations

        return all_lines

    def process(self):
        html = self.get_html(self.url)
        return self.get_all_station(html)

