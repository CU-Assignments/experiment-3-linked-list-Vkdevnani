from collections import defaultdict, OrderedDict

class LFUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.freq_map = defaultdict(OrderedDict)
        self.min_freq = 0

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self._update_freq(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
        if key in self.cache:
            self.cache[key] = value
            self._update_freq(key)
        else:
            if len(self.cache) >= self.capacity:
                self._evict()
            self.cache[key] = value
            self._update_freq(key)

    def _update_freq(self, key: int) -> None:
        freq = self._get_freq(key)
        self.freq_map[freq].pop(key, None)
        if not self.freq_map[self.min_freq]:
            self.min_freq += 1
        self.freq_map[freq + 1][key] = None

    def _evict(self) -> None:
        key, _ = self.freq_map[self.min_freq].popitem(last=False)
        del self.cache[key]

    def _get_freq(self, key: int) -> int:
        for freq, keys in self.freq_map.items():
            if key in keys:
                return freq
        return 0
