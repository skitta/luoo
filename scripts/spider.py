import urllib.request as request
import re


class Spider():

    def __init__(self, user_id):
        self.home = 'http://www.luoo.net/music'
        self.favorite = 'http://www.luoo.net/user/singles/%s/' % user_id
        self.music = 'http://luoo.800edu.net/low/luoo/radio%s/%s.mp3'

    def get_favorite(self, page_list):
        # 获取用户收藏中到所有歌曲
        data = []
        for page in page_list:
            url = '%s?p=%s' % (self.favorite, page)
            try:
                res = request.urlopen(url)
            except Exception as error:
                print(error)
            else:
                content = res.read().decode()
                track_patten = re.compile(
                    r'<a href.*?class="trackname btn-play".*?</a>'
                )
                img_patten = re.compile(
                    r'data-img=".*?albums.*?"'
                )
                track = [
                    i.split('>')[1].split('<')[0]
                    for i in track_patten.findall(content)
                ]
                img = [
                    i.split('"')[1]
                    for i in img_patten.findall(content)
                ]
                data += [(a, b) for a, b in zip(track, img)]
        return data

    def get_last_vol(self):
        # 获取最新期刊号
        content = request.urlopen(self.home).read().decode()
        patten = re.compile(r'<a href=.*?class="name".*?</a>')
        result = patten.findall(content)
        total_vol = result[0].split('>')[1].split()[0].split('.')[1]
        return total_vol

    def get_data(self, vol):
        # 获取指定期刊的期刊号、序列、曲名
        url = '%s/%s' % (self.home, vol)
        try:
            req = request.urlopen(url)
        except Exception as error:
            print(error)
        else:
            content = req.read().decode()
            patten = re.compile(r'<a href.*?class="trackname btn-play".*?</a>')
            data = []
            for i in patten.findall(content):
                temp = i.split('>')[1].split('<')[0].split('. ')
                data.append((vol, temp[0], temp[1]))
            return data

    def get_download_link(self, name, base):
        # 获取指定曲目的下载地址
        record = base.search(name)
        if record:
            url = self.music % (record[0], record[1])
            return url
