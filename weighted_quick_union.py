

class WeightedQuickUnion:
    def __init__(self, n):
        self.id = list(range(n))  
        self.size = [1] * n       
        self.count = n            
        self.find_operations = 0
        self.union_operations = 0

    def find(self, p):
        self.find_operations += 1
        root = p
        while root != self.id[root]:
            root = self.id[root]

        while p != root:
            next_p = self.id[p]
            self.id[p] = root
            p = next_p

        return root

    def connected(self, p, q):
        return self.find(p) == self.find(q)

    def union(self, p, q):
        self.union_operations += 1
        root_p = self.find(p)
        root_q = self.find(q)

        if root_p == root_q:
            return

        if self.size[root_p] < self.size[root_q]:
            self.id[root_p] = root_q
            self.size[root_q] += self.size[root_p]
        else:
            self.id[root_q] = root_p
            self.size[root_p] += self.size[root_q]

        self.count -= 1

    def get_components(self):
        return self.count

    def get_tree_height(self, p):   
        root = self.find(p)
        height = 0
        current = root
        while current != self.id[current]:
            height += 1
            current = self.id[current]
        return height

    def print_state(self):
        print(f"Parent array: {self.id}")
        print(f"Tree sizes: {self.size}")
        print(f"Components: {self.count}")
        print(f"Union operations: {self.union_operations}")
        print(f"Find operations: {self.find_operations}")


class StandardQuickUnion:
    def __init__(self, n):
        self.id = list(range(n))
        self.count = n
        self.union_operations = 0
        self.find_operations = 0

    def find(self, p):
        self.find_operations += 1
        while p != self.id[p]:
            p = self.id[p]
        return p

    def connected(self, p, q):
        return self.find(p) == self.find(q)

    def union(self, p, q):
        self.union_operations += 1
        root_p = self.find(p)
        root_q = self.find(q)

        if root_p == root_q:
            return

        self.id[root_p] = root_q
        self.count -= 1

    def get_components(self):
        return self.count

    def print_state(self):
        print(f"Parent array: {self.id}")
        print(f"Components: {self.count}")
        print(f"Union operations: {self.union_operations}")
        print(f"Find operations: {self.find_operations}")



import time

def run_comparison():
    print("Weighted Quick Union vs Standard Quick Union Comparison")
    print("=" * 60)

    N = 10
    operations = [
        (0, 1), (2, 3), (4, 5), (6, 7), (8, 9),  
        (0, 2), (4, 6), (0, 4)                   
    ]

    
    print("\n=== Weighted Quick Union with Path Compression ===")
    wqu = WeightedQuickUnion(N)

    start_time = time.perf_counter()
    for i, (p, q) in enumerate(operations):
        print(f"\nStep {i+1}: Union({p}, {q})")
        wqu.union(p, q)
        wqu.print_state()

        
        components = {}
        for site in range(N):
            root = wqu.find(site)
            if root not in components:
                components[root] = []
            components[root].append(site)

        print("Connected components:")
        for root, sites in components.items():
            if len(sites) > 1:
                print(f"  Component {root}: {sites}")

    wqu_time = time.perf_counter() - start_time

    
    print("\n" + "=" * 60)
    print("=== Standard Quick Union (for comparison) ===")
    squ = StandardQuickUnion(N)

    start_time = time.perf_counter()
    for i, (p, q) in enumerate(operations):
        print(f"\nStep {i+1}: Union({p}, {q})")
        squ.union(p, q)
        squ.print_state()

    squ_time = time.perf_counter() - start_time

    
    print("\n" + "=" * 60)
    print("PERFORMANCE COMPARISON")
    print("=" * 60)

    print(f"Weighted Quick Union:")
    print(f"  - Execution time: {wqu_time:.6f} seconds")
    print(f"  - Union operations: {wqu.union_operations}")
    print(f"  - Find operations: {wqu.find_operations}")
    print(f"  - Final components: {wqu.get_components()}")

    print(f"\nStandard Quick Union:")
    print(f"  - Execution time: {squ_time:.6f} seconds")
    print(f"  - Union operations: {squ.union_operations}")
    print(f"  - Find operations: {squ.find_operations}")
    print(f"  - Final components: {squ.get_components()}")

    
    print("\nTree heights after all operations:")
    for site in range(N):
        height = wqu.get_tree_height(site)
        print(f"  Site {site}: height = {height}")

    if wqu_time < squ_time:
        print(f"\nWeighted Quick Union was {squ_time/wqu_time:.2f}x faster")
    else:
        print(f"\nStandard Quick Union was {wqu_time/squ_time:.2f}x faster")


if __name__ == "__main__":
    run_comparison()
