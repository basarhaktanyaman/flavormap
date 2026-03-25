#!/usr/bin/env python3
"""
Union-Find Data Structures Summary

This script demonstrates all the major union-find algorithms:
1. Quick Find
2. Quick Union
3. Weighted Quick Union
4. Weighted Quick Union with Path Compression

Each algorithm is implemented and tested with the specific sequence
requested in the original problem.
"""

class QuickFind:
    """Quick Find: O(1) find, O(N) union"""
    def __init__(self, n):
        self.id = list(range(n))
        self.count = n

    def find(self, p):
        return self.id[p]

    def union(self, p, q):
        pid, qid = self.find(p), self.find(q)
        if pid == qid: return
        for i in range(len(self.id)):
            if self.id[i] == pid:
                self.id[i] = qid
        self.count -= 1

    def connected(self, p, q):
        return self.find(p) == self.find(q)


class QuickUnion:
    """Quick Union: O(tree height) find and union"""
    def __init__(self, n):
        self.id = list(range(n))
        self.count = n

    def find(self, p):
        while p != self.id[p]:
            p = self.id[p]
        return p

    def union(self, p, q):
        root_p, root_q = self.find(p), self.find(q)
        if root_p == root_q: return
        self.id[root_p] = root_q
        self.count -= 1

    def connected(self, p, q):
        return self.find(p) == self.find(q)


class WeightedQuickUnion:
    """Weighted Quick Union: O(log N) amortized"""
    def __init__(self, n):
        self.id = list(range(n))
        self.size = [1] * n
        self.count = n

    def find(self, p):
        while p != self.id[p]:
            p = self.id[p]
        return p

    def union(self, p, q):
        root_p, root_q = self.find(p), self.find(q)
        if root_p == root_q: return
        # Attach smaller tree to larger tree
        if self.size[root_p] < self.size[root_q]:
            self.id[root_p] = root_q
            self.size[root_q] += self.size[root_p]
        else:
            self.id[root_q] = root_p
            self.size[root_p] += self.size[root_q]
        self.count -= 1

    def connected(self, p, q):
        return self.find(p) == self.find(q)


class WeightedQuickUnionPathCompression:
    """Weighted Quick Union with Path Compression: O(log N) amortized"""
    def __init__(self, n):
        self.id = list(range(n))
        self.size = [1] * n
        self.count = n

    def find(self, p):
        if p != self.id[p]:
            self.id[p] = self.find(self.id[p])  # Path compression
        return self.id[p]

    def union(self, p, q):
        root_p, root_q = self.find(p), self.find(q)
        if root_p == root_q: return
        # Attach smaller tree to larger tree
        if self.size[root_p] < self.size[root_q]:
            self.id[root_p] = root_q
            self.size[root_q] += self.size[root_p]
        else:
            self.id[root_q] = root_p
            self.size[root_p] += self.size[root_q]
        self.count -= 1

    def connected(self, p, q):
        return self.find(p) == self.find(q)


def run_specific_test():
    """Run the specific test case requested"""
    print("Union-Find Algorithms with Your Specific Test Case")
    print("=" * 55)

    N = 10
    operations = [
        (0, 1), (2, 3), (4, 5), (6, 7), (8, 9),  # First round
        (0, 2), (4, 6), (0, 4)                    # Second round
    ]

    algorithms = [
        ("Quick Find", QuickFind),
        ("Quick Union", QuickUnion),
        ("Weighted Quick Union", WeightedQuickUnion),
        ("Weighted QU + Path Compression", WeightedQuickUnionPathCompression)
    ]

    results = []

    for name, alg_class in algorithms:
        print(f"\n=== {name} ===")
        uf = alg_class(N)

        for i, (p, q) in enumerate(operations):
            print(f"Step {i+1}: Union({p}, {q})")
            uf.union(p, q)
            print(f"  Array: {uf.id}")
            print(f"  Components: {uf.count}")

        results.append((name, uf.count, uf.id.copy()))

        # Test connectivity
        print("  Connectivity tests:")
        test_pairs = [(0, 4), (1, 3), (5, 7), (8, 9), (0, 8)]
        for p, q in test_pairs:
            connected = uf.connected(p, q)
            print(f"    Sites {p} and {q}: {'Connected' if connected else 'Not connected'}")

    # Summary
    print("\n" + "=" * 55)
    print("FINAL RESULTS COMPARISON")
    print("=" * 55)

    print(f"{'Algorithm':<35} {'Components':<12} {'Final Array'}")
    print("-" * 55)

    for name, components, array in results:
        print(f"{name:<35} {components:<12} {array}")

    print("\nKey Points:")
    print("- All algorithms produce the same final connectivity result")
    print("- Quick Find: O(1) find, O(N) union - good for many find operations")
    print("- Quick Union: O(tree height) find/union - good for many union operations")
    print("- Weighted Quick Union: Balanced trees, O(log N) amortized")
    print("- Weighted QU + Path Compression: Optimal for most applications")


if __name__ == "__main__":
    run_specific_test()
