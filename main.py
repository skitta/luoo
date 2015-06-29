import os
import re
import urllib.request as request

from scripts import database, spider, download


class Luoo():

    def __init__(self, user_id, save_path='./download/'):
        self.base = database.Base('db.sqlite3')
        self.source = spider.Spider(user_id)
        self.save_path = save_path
        if not os.path.isdir(save_path):
            os.mkdir(save_path)

    def scan_mp3(self):
        # 扫描下载目录，获取已下载的曲目列表
        dirs = os.listdir(self.save_path)
        names = [os.path.splitext(file)[0] for file in dirs]
        return names

    def update_database(self):
        # 更新数据库
        vols = self.base.scan()
        last_vol = self.source.get_last_vol()
        target = [str(i).zfill(3) for i in range(1, int(last_vol)+1)]
        print('Updating database, please wait...')
        for vol in target:
            if vol in vols:
                pass
            else:
                print('Updating data %s' % vol)
                data = self.source.get_data(vol)
                for d in data:
                    self.base.insert(d)
        print('Update completed')

    def get_queue(self):
        work_queue = []
        favorite = self.source.get_favorite([1, 2, 3])
        has_downloaded = self.scan_mp3()
        for item in favorite:
            if item[0] not in has_downloaded:
                track_name = item[0]
                track_url = self.source.get_download_link(
                    track_name, self.base)
                img_url = item[1]
                work_queue.append((track_name, track_url, img_url))
        return work_queue

    def download_track(self, queue):
        url = queue[1]
        img = queue[2]
        ruler = r"[\/\\\:\*\?\"\<\>\|]"
        name = re.sub(ruler, '', queue[0])
        save_path = self.save_path + name + '.mp3'

        print('Downloading [%s]' % name)
        with open(save_path, 'wb') as fb:
            if url:
                download.multi_download(url, fb, 5)
                try:
                    req = request.urlopen(img)
                except IOError:
                    print('IOError')
                else:
                    res = req.read()
                    print(res)
                    print('Complete')
                    # TODO 嵌入专辑图片
            else:
                print('download link not found')
                fb.close()
                os.remove(save_path)


# TODO 列队下载功能
if __name__ == '__main__':
    task = Luoo('28049')
    task.update_database()
    work = task.get_queue()
    for i in work:
        task.download_track(i)
