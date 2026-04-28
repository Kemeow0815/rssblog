import json
import os
import time
import requests
# SOURCE_BASE = "https://gitee.com/caibingcheng/rssblog-source/raw/public/"
SOURCE_BASE = "https://raw.githubusercontent.com/Kemeow0815/rssblog-source/public/"
# SOURCE_BASE = "https://cdn.jsdelivr.net/gh/Kemeow0815/rssblog-source@public/"
SOURCE_URL = SOURCE_BASE + "stats.min.json"


class SimpleCache:
    """简单的缓存实现，替代 buffercache"""
    def __init__(self, timeout=1000*60*60*3):
        self.timeout = timeout
        self._data = None
        self._timestamp = 0
        self._getter = None
    
    def set_getter(self, getter):
        self._getter = getter
        return self
    
    def update(self):
        now = time.time() * 1000  # 转换为毫秒
        if self._data is None or (now - self._timestamp) > self.timeout:
            try:
                self._data = self._getter()
                self._timestamp = now
            except Exception as e:
                print(f"Cache update failed: {e}")
                if self._data is None:
                    raise
        return self
    
    def get(self):
        return self._data
    
    def immediate(self):
        """强制立即更新缓存"""
        self._timestamp = 0
        self.update()


class RssblogSource(object):
    def __init__(self):
        self._bc = SimpleCache(timeout=1000*60*60*3).set_getter(self._update)

    def _update(self):
        raw = requests.get(SOURCE_URL)
        print(f"get source {raw.status_code} from {SOURCE_URL}")
        if raw.status_code != 200:
            raise Exception("get source error")
        self._source_json = json.loads(raw.text)
        print("[{}] update rssblog source".format(os.getpid()), time.time())
        self._batch = self._source_json["batch"]
        self._url = self._source_json["urls"]

        self._url["source"] = self._source(self._url["source"])
        self._url["date"] = self._date(self._url["date"])
        for user in self._url["user"]:
            user["date"] = self._date(user["date"])
        return self._url, self._batch

    @staticmethod
    def _date(date_ls):
        year = []
        for date in date_ls:
            try:
                month = {}
                for m in date[1]:
                    month[int(m[0])] = int(m[1])
                year.append({
                    "year": int(date[0]),
                    "month": month,
                })
            except (ValueError, TypeError, IndexError) as e:
                # Skip malformed date entries
                print(f"Warning: Skipping malformed date entry: {date}, error: {e}")
                continue
        year.sort(key=lambda x: x.get('year', 0), reverse=True)
        return year

    @staticmethod
    def _source(sources):
        source_mp = {}
        for source in sources:
            source_mp[source[0]] = source[1]
        return source_mp

    def immediate(self):
        self._bc.immediate()

    @property
    def url(self):
        url, _ = self._bc.update().get()
        return url

    @property
    def batch(self):
        _, batch = self._bc.update().get()
        return batch
