from os.path import abspath, exists


MAX_SIZE = 10**8  # One hundred million lines max, a little safety.
CACHES = {}


def get_cache(path):
  path = abspath(path)
  try:
    return CACHES[path]
  except KeyError:
    CACHES[path] = cache = LocalCache(path)
    return cache


class LocalCache(dict):

  def __init__(self, path):
    self.path = path = abspath(path)
    self.inverted = {}
    if exists(path):
      with open(path) as data:
        for tag, url in self.read(data):
          self._set(tag, url)

  def __setitem__(self, url, tag):
    if url not in self:
      self._set(tag, url)
      if len(self) < MAX_SIZE:
        with open(self.path, 'a') as data:
          print >> data, tag, url

  def _set(self, tag, url):
    dict.__setitem__(self, url, tag)
    self.inverted[tag] = url

  @staticmethod
  def read(lines):
    for line in lines:
      try:
        tag, url = line.split()
      except:
        continue
      yield tag, url
