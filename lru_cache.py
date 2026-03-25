

import heapq
import time


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}     
        self.heap = []      
        self.time = 0  
    
    def get(self, key):
        if key in self.cache:
            value, _ = self.cache[key]
            self.time += 1
            self.cache[key] = (value, self.time)
            heapq.heappush(self.heap, (self.time, key))
            return value
        else:
            return -1
    
    def put(self, key, value):
        self.time += 1
        
        if key in self.cache:
            self.cache[key] = (value, self.time)
            heapq.heappush(self.heap, (self.time, key))
        else:
            if len(self.cache) >= self.capacity:
                self._evict_lru()
            
            self.cache[key] = (value, self.time)
            heapq.heappush(self.heap, (self.time, key))
    
    def _evict_lru(self):
        while self.heap:
            timestamp, key = heapq.heappop(self.heap)
            if key in self.cache and self.cache[key][1] == timestamp:
                del self.cache[key]
                print(f"⚠️  Evicted Key: {key}")
                break
    
    def get_cache_state(self):
        print("📊 Cache state:")
        for key, (value, timestamp) in sorted(self.cache.items()):
            print(f"   Key: {key}, Value: {value}, Time: {timestamp}")


print("=== LRU Cache Test ===\n")

cache = LRUCache(2)  

print("PUT(1, 10)")
cache.put(1, 10)
cache.get_cache_state()

print("\nPUT(2, 20)")
cache.put(2, 20)
cache.get_cache_state()

print("\nGET(1)")
result = cache.get(1)
print(f"✅ Key found → Output: {result}")
cache.get_cache_state()

print("\nPUT(3, 30)")
cache.put(3, 30)
print("⚠️  Cache full → Evicting LRU item")
cache.get_cache_state()

print("\nGET(2)")
result = cache.get(2)
if result == -1:
    print(f"❌ Key not found → Output: {result}")
else:
    print(f"✅ Key found → Output: {result}")
cache.get_cache_state()

print("\nGET(3)")
result = cache.get(3)
print(f"✅ Key found → Output: {result}")
cache.get_cache_state()

