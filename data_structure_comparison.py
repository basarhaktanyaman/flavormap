"""
Data Structure Comparison: Dynamic Array vs Linked List
"""


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class DynamicArrayStructure:
    def __init__(self):
        self.data = []
    
    def insert_at_beginning(self, value):
        self.data.insert(0, value)
    
    def insert_at_end(self, value):
        self.data.append(value)
    
    def delete_from_beginning(self):
        if self.data:
            return self.data.pop(0)
        return None
    
    def delete_from_end(self):
        if self.data:
            return self.data.pop()
        return None
    
    def display(self):
        return self.data


class LinkedListStructure:
    def __init__(self):
        self.head = None
    
    def insert_at_beginning(self, value):
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node
    
    def insert_at_end(self, value):
        new_node = Node(value)
        if not self.head:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    
    def delete_from_beginning(self):
        if not self.head:
            return None
        value = self.head.value
        self.head = self.head.next
        return value
    
    def delete_from_end(self):
        if not self.head:
            return None
        if not self.head.next:
            value = self.head.value
            self.head = None
            return value
        current = self.head
        while current.next.next:
            current = current.next
        value = current.next.value
        current.next = None
        return value
    
    def display(self):
        result = []
        current = self.head
        while current:
            result.append(current.value)
            current = current.next
        return result


def main():
    print("=" * 50)
    print("  Data Structure Comparison")
    print("=" * 50)
    
    # Version A: Dynamic Array
    print("\n🔷 VERSION A - Dynamic Array (Python List)")
    print("-" * 50)
    array = DynamicArrayStructure()
    
    array.insert_at_end(10)
    array.insert_at_end(20)
    array.insert_at_beginning(5)
    print(f"After inserts: {array.display()}")
    
    array.delete_from_beginning()
    print(f"After delete from beginning: {array.display()}")
    
    array.delete_from_end()
    print(f"After delete from end: {array.display()}")
    
    # Version B: Linked List
    print("\n🔶 VERSION B - Singly Linked List")
    print("-" * 50)
    linked = LinkedListStructure()
    
    linked.insert_at_end(10)
    linked.insert_at_end(20)
    linked.insert_at_beginning(5)
    print(f"After inserts: {linked.display()}")
    
    linked.delete_from_beginning()
    print(f"After delete from beginning: {linked.display()}")
    
    linked.delete_from_end()
    print(f"After delete from end: {linked.display()}")
    
    # Time Complexity Analysis
    print("\n" + "=" * 50)
    print("⏱️  Time Complexity Analysis")
    print("=" * 50)
    print("\nDynamic Array:")
    print("  insert_at_beginning: O(n) - requires shifting")
    print("  insert_at_end: O(1) - direct append")
    print("  delete_from_beginning: O(n) - requires shifting")
    print("  delete_from_end: O(1) - direct pop")
    
    print("\nLinked List:")
    print("  insert_at_beginning: O(1) - just update head")
    print("  insert_at_end: O(n) - traverse to end")
    print("  delete_from_beginning: O(1) - just update head")
    print("  delete_from_end: O(n) - traverse to end")
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()

