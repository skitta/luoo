import urllib.request as request
import threading


LOCK = threading.RLock()


class Download(threading.Thread):

    def __init__(self, url, start_size, end_size, file):
        threading.Thread.__init__(self)
        self.url = url
        self.start_size = start_size
        self.end_size = end_size
        self.file = file

    def run(self):
        req = request.Request(self.url)
        req.headers['Range'] = 'bytes=%s-%s' % (self.start_size, self.end_size)
        offset = self.start_size
        res = request.urlopen(req)
        while 1:
            block = res.read()
            if not block:
                break
            with LOCK:
                self.file.seek(offset)
                self.file.write(block)


def multi_download(url, fb, thread=3):
    try:
        req = request.urlopen(url)
    except Exception as error:
        print(error)
    else:
        info = str(req.info()).split()
        size = int(info[info.index('Content-Length:') + 1])
        avg_size, pad_size = divmod(size, thread)
        task_list = []
        for i in range(thread):
            start_size = i * avg_size
            end_size = start_size + avg_size
            if i == thread:
                end_size = start_size + pad_size
            task = Download(url, start_size, end_size, fb)
            task.start()
            task_list.append(task)
        for i in task_list:
            i.join()
