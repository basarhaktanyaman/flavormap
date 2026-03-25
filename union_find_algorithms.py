#!/usr/bin/env python3
"""
Complete Union-Find Algorithms Implementation and Comparison

This script implements and compares:
1. Quick Find (slow union, fast find)
2. Quick Union (fast union, slow find)
3. Weighted Quick Union (balanced trees)
4. Weighted Quick Union with Path Compression (optimal)
"""

import time
import random
from typing import List


class QuickFind:
    """Quick Find: O(1) find, O(N) union"""
    def __init__(self, n: int):
        self.id = list(range(n))
        self.count = n
        self.ops = {'union': 0, 'find': 0}

    def find(self, p: int) -> int:
        self.ops['find'] += 1
        return self.id[p]

    def union(self, p: int, q: int) -> None:
        self.ops['union'] += 1
        pid, qid = self.find(p), self.find(q)
        if pid == qid: return
        for i in range(len(self.id)):
            if self.id[i] == pid:
                self.id[i] = qid
        self.count -= 1


class QuickUnion:
    """Quick Union: O(tree height) find and union"""
    def __init__(self, n: int):
        self.id = list(range(n))
        self.count = n
        self.ops = {'union': 0, 'find': 0}

    def find(self, p: int) -> int:
        self.ops['find'] += 1
        while p != self.id[p]:
            p = self.id[p]
        return p

    def union(self, p: int, q: int) -> None:
        self.ops['union'] += 1
        root_p, root_q = self.find(p), self.find(q)
        if root_p == root_q: return
        self.id[root_p] = root_q
        self.count -= 1


class WeightedQuickUnion:
    """Weighted Quick Union: O(log N) amortized"""
    def __init__(self, n: int):
        self.id = list(range(n))
        self.size = [1] * n
        self.count = n
        self.ops = {'union': 0, 'find': 0}

    def find(self, p: int) -> int:
        self.ops['find'] += 1
        while p != self.id[p]:
            p = self.id[p]
        return p

    def union(self, p: int, q: int) -> None:
        self.ops['union'] += 1
        root_p, root_q = self.find(p), self.find(q)
        if root_p == root_q: return
        # Weighted union: attach smaller tree to larger
        if self.size[root_p] < self.size[root_q]:
            self.id[root_p] = root_q
            self.size[root_q] += self.size[root_p]
        else:
            self.id[root_q] = root_p
            self.size[root_p] += self.size[root_q]
        self.count -= 1


class WeightedQuickUnionPathCompression:
    """Weighted Quick Union with Path Compression: O(log N) amortized"""
    def __init__(self, n: int):
        self.id = list(range(n))
        self.size = [1] * n
        self.count = n
        self.ops = {'union': 0, 'find': 0}

    def find(self, p: int) -> int:
        self.ops['find'] += 1
        if p != self.id[p]:
            # Path compression: make every node point to its root
            self.id[p] = self.find(self.id[p])
        return self.id[p]

    def union(self, p: int, q: int) -> None:
        self.ops['union'] += 1
        root_p, root_q = self.find(p), self.find(q)
        if root_p == root_q: return
        # Weighted union: attach smaller tree to larger
        if self.size[root_p] < self.size[root_q]:
            self.id[root_p] = root_q
            self.size[root_q] += self.size[root_p]
        else:
            self.id[root_q] = root_p
            self.size[root_p] += self.size[root_q]
        self.count -= 1


def generate_random_unions(n: int, num_operations: int) -> List[tuple]:
    """Generate random union operations."""
    operations = []
    for _ in range(num_operations):
        p, q = random.randint(0, n-1), random.randint(0, n-1)
        operations.append((p, q))
    return operations


def benchmark_algorithm(algorithm_class, n: int, operations: List[tuple]) -> dict:
    """Benchmark a union-find algorithm."""
    uf = algorithm_class(n)

    start_time = time.perf_counter()
    for p, q in operations:
        uf.union(p, q)
    end_time = time.perf_counter()

    return {
        'algorithm': algorithm_class.__name__,
        'final_components': uf.count,
        'execution_time': end_time - start_time,
        'union_ops': uf.ops['union'],
        'find_ops': uf.ops['find'],
        'total_ops': uf.ops['union'] + uf.ops['find']
    }


def run_comprehensive_comparison():
    """Run comprehensive comparison of all algorithms."""
    print("Union-Find Algorithms Comprehensive Comparison")
    print("=" * 60)

    sizes = [100, 1000, 5000, 10000]
    operations_per_size = [1000, 5000, 10000, 20000]

    algorithms = [
        QuickFind,
        QuickUnion,
        WeightedQuickUnion,
        WeightedQuickUnionPathCompression
    ]

    results = []

    for n, ops_count in zip(sizes, operations_per_size):
        print(f"\nTesting with N={n}, {ops_count} operations")
        print("-" * 40)

        operations = generate_random_unions(n, ops_count)

        for alg_class in algorithms:
            result = benchmark_algorithm(alg_class, n, operations)
            results.append(result)

            alg_name = result['algorithm']
            components = result['final_components']
            exec_time = result['execution_time']
            union_ops = result['union_ops']
            find_ops = result['find_ops']

            print(f"{alg_name:30} | Components: {components:4} | Time: {exec_time:12.6f}s | Union: {union_ops:5} | Find: {find_ops:5}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    print(f"{'Algorithm':<30} {'Size':<8} {'Time (s)':<12} {'Speedup'}")
    print("-" * 60)

    for result in results:
        size_idx = results.index(result) % len(sizes)
        print(f"{result['algorithm']:<30} {sizes[size_idx]:<8} {result['execution_time']:<12.6f}")

    # Find fastest algorithm for each size
    print("\nFastest algorithm by size:")
    for i, size in enumerate(sizes):
        size_results = [r for r in results if sizes[results.index(r) % len(sizes)] == size]
        fastest = min(size_results, key=lambda x: x['execution_time'])
        print(f"  N={size:<5}: {fastest['algorithm']:<35} ({fastest['execution_time']:.6f}s)")


if __name__ == "__main__":
    run_comprehensive_comparison()
