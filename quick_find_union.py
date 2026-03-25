#!/usr/bin/env python3

class QuickFind:
    def __init__(self, n):
        self.id = list(range(n))
        self.count = n
        
    def find(self, p):
        return self.id[p]
    
    def connected(self, p, q):
        return self.find(p) == self.find(q)
    
    def union(self, p, q):
        pid = self.find(p)
        qid = self.find(q)
        
        if pid == qid:
            return
            
        for i in range(len(self.id)):
            if self.id[i] == pid:
                self.id[i] = qid
                
        self.count -= 1
    
    def print_array(self):
        print("QuickFind array:", self.id)


class QuickUnion:
    def __init__(self, n):
        self.id = list(range(n))
        self.count = n
        
    def find(self, p):
        while p != self.id[p]:
            p = self.id[p]
        return p
    
    def connected(self, p, q):
        return self.find(p) == self.find(q)
    
    def union(self, p, q):
        root_p = self.find(p)
        root_q = self.find(q)
        
        if root_p == root_q:
            return
            
        self.id[root_p] = root_q
        self.count -= 1
    
    def print_array(self):
        print("QuickUnion array:", self.id)


# Initialize with N=10 sites
print("Initializing both data structures with N=10 sites")
qf = QuickFind(10)
qu = QuickUnion(10)

print("\nInitial state:")
qf.print_array()
qu.print_array()

# Perform union operations: (0,1), (2,3), (4,5), (6,7), (8,9)
operations = [(0,1), (2,3), (4,5), (6,7), (8,9)]
print("\nPerforming first round of unions:", operations)

for p, q in operations:
    qf.union(p, q)
    qu.union(p, q)
    print(f"After union({p},{q}):")
    qf.print_array()
    qu.print_array()
    print()

# Perform second round: (0,2), (4,6), (0,4)
operations2 = [(0,2), (4,6), (0,4)]
print("Performing second round of unions:", operations2)

for p, q in operations2:
    qf.union(p, q)
    qu.union(p, q)
    print(f"After union({p},{q}):")
    qf.print_array()
    qu.print_array()
    print()

print("Final results:")
print(f"QuickFind components: {qf.count}")
print(f"QuickUnion components: {qu.count}")

# Test connectivity
print("\nConnectivity tests:")
test_pairs = [(0,4), (1,3), (5,7), (8,9), (0,8)]
for p, q in test_pairs:
    qf_conn = qf.connected(p, q)
    qu_conn = qu.connected(p, q)
    print(f"Sites {p} and {q}: QuickFind={qf_conn}, QuickUnion={qu_conn}")
