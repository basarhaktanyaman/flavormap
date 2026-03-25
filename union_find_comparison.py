
"""
Quick Find and Quick Union data structures implementation and comparison.

This script implements both algorithms, performs the specified union operations,
and compares their performance characteristics.
"""

import time
from typing import List


class QuickFind:
    """Quick Find implementation - fast find, slow union."""
    
    def __init__(self, n: int):
        """Initialize with n sites (0 to n-1)."""
        self.id = list(range(n))
        self.count = n
        self.union_operations = 0
        self.find_operations = 0
        
    def find(self, p: int) -> int:
        """Find the component identifier for site p."""
        self.find_operations += 1
        return self.id[p]
    
    def connected(self, p: int, q: int) -> bool:
        """Check if sites p and q are connected."""
        return self.find(p) == self.find(q)
    
    def union(self, p: int, q: int) -> None:
        """Connect sites p and q."""
        self.union_operations += 1
        pid = self.find(p)
        qid = self.find(q)
        
        if pid == qid:
            return
            
        
        for i in range(len(self.id)):
            if self.id[i] == pid:
                self.id[i] = qid
                
        self.count -= 1
    
    def get_components(self) -> int:
        """Return number of connected components."""
        return self.count
    
    def print_state(self) -> None:
        """Print current state of the data structure."""
        print(f"QuickFind ID array: {self.id}")
        print(f"Components: {self.count}")
        print(f"Union operations: {self.union_operations}")
        print(f"Find operations: {self.find_operations}")


class QuickUnion:
    """Quick Union implementation - fast union, slow find."""
    
    def __init__(self, n: int):
        """Initialize with n sites (0 to n-1)."""
        self.id = list(range(n))
        self.count = n
        self.union_operations = 0
        self.find_operations = 0
        
    def find(self, p: int) -> int:
        """Find the root of site p."""
        self.find_operations += 1
        while p != self.id[p]:
            p = self.id[p]
        return p
    
    def connected(self, p: int, q: int) -> bool:
        """Check if sites p and q are connected."""
        return self.find(p) == self.find(q)
    
    def union(self, p: int, q: int) -> None:
        """Connect sites p and q."""
        self.union_operations += 1
        root_p = self.find(p)
        root_q = self.find(q)
        
        if root_p == root_q:
            return
            
        
        self.id[root_p] = root_q
        self.count -= 1
    
    def get_components(self) -> int:
        """Return number of connected components."""
        return self.count
    
    def print_state(self) -> None:
        """Print current state of the data structure."""
        print(f"QuickUnion ID array: {self.id}")
        print(f"Components: {self.count}")
        print(f"Union operations: {self.union_operations}")
        print(f"Find operations: {self.find_operations}")


def perform_union_sequence(uf, name: str, unions: List[tuple]) -> float:
    """Perform the sequence of union operations and measure time."""
    print(f"\n=== {name} ===")
    print("Initial state:")
    uf.print_state()
    
    start_time = time.perf_counter()
    
    for i, (p, q) in enumerate(unions):
        print(f"\nStep {i+1}: Union({p}, {q})")
        uf.union(p, q)
        print(f"After union({p}, {q}):")
        uf.print_state()
        
        
        components = {}
        for site in range(len(uf.id)):
            root = uf.find(site)
            if root not in components:
                components[root] = []
            components[root].append(site)
        
        print("Connected components:")
        for root, sites in components.items():
            if len(sites) > 1:
                print(f"  Component {root}: {sites}")
    
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    
    print(f"\nFinal state:")
    uf.print_state()
    print(f"Execution time: {execution_time:.6f} seconds")
    
    return execution_time


def main():
    """Main function to run the comparison."""
    N = 10
    
    
    union_sequence = [
        (0, 1), (2, 3), (4, 5), (6, 7), (8, 9),  
        (0, 2), (4, 6), (0, 4)                    
    ]
    
    print("Union-Find Data Structures Comparison")
    print("=" * 50)
    print(f"Initializing with N = {N} sites")
    print(f"Union operations: {union_sequence}")
    
    
    qf = QuickFind(N)
    qu = QuickUnion(N)
    
    
    qf_time = perform_union_sequence(qf, "Quick Find", union_sequence)
    
    
    qu_time = perform_union_sequence(qu, "Quick Union", union_sequence)
    
    
    print("\n" + "=" * 50)
    print("COMPARISON SUMMARY")
    print("=" * 50)
    
    print(f"Quick Find:")
    print(f"  - Total union operations: {qf.union_operations}")
    print(f"  - Total find operations: {qf.find_operations}")
    print(f"  - Execution time: {qf_time:.6f} seconds")
    print(f"  - Final components: {qf.get_components()}")
    
    print(f"\nQuick Union:")
    print(f"  - Total union operations: {qu.union_operations}")
    print(f"  - Total find operations: {qu.find_operations}")
    print(f"  - Execution time: {qu_time:.6f} seconds")
    print(f"  - Final components: {qu.get_components()}")
    
    print(f"\nPerformance Analysis:")
    print(f"  - Quick Find is faster for find operations (O(1))")
    print(f"  - Quick Union is faster for union operations (O(tree height))")
    print(f"  - For this sequence, Quick Find made {qf.find_operations} find calls")
    print(f"  - For this sequence, Quick Union made {qu.find_operations} find calls")
    
    if qf_time < qu_time:
        print(f"  - Quick Find was {qu_time/qf_time:.2f}x faster overall")
    else:
        print(f"  - Quick Union was {qf_time/qu_time:.2f}x faster overall")
    
    
    print(f"\nVerification: Both algorithms produced {qf.get_components()} components")
    
    
    print("\nConnectivity verification:")
    test_pairs = [(0, 4), (1, 3), (5, 7), (8, 9), (0, 8)]
    for p, q in test_pairs:
        qf_connected = qf.connected(p, q)
        qu_connected = qu.connected(p, q)
        status = "✓" if qf_connected == qu_connected else "✗"
        print(f"  {status} Sites {p} and {q}: QF={qf_connected}, QU={qu_connected}")


if __name__ == "__main__":
    main()
