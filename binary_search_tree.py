

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None
    
    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node, value):
        if value < node.value:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(node.left, value)
        else:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(node.right, value)
    
    def find_maximum(self):
        if self.root is None:
            return None
        
        current = self.root
        while current.right is not None:
            current = current.right
        return current.value
    
    def find_minimum(self):
        if self.root is None:
            return None
        
        current = self.root
        while current.left is not None:
            current = current.left
        return current.value
    
    def find_height(self):
        return self._height_recursive(self.root)
    
    def _height_recursive(self, node):
        if node is None:
            return 0
        
        left_height = self._height_recursive(node.left)
        right_height = self._height_recursive(node.right)
        
        return max(left_height, right_height) + 1


bst = BinarySearchTree()
values = [50, 30, 70, 20, 40, 60, 80]

print("Inserting values:", values)
for value in values:
    bst.insert(value)

print(f"\nMaximum value: {bst.find_maximum()}")
print(f"Minimum value: {bst.find_minimum()}")
print(f"Height of tree: {bst.find_height()}")

print("\n--- Additional Test ---")
bst2 = BinarySearchTree()
bst2.insert(10)
bst2.insert(5)
bst2.insert(15)
bst2.insert(3)
bst2.insert(7)

print("Tree values: [10, 5, 15, 3, 7]")
print(f"Maximum value: {bst2.find_maximum()}")
print(f"Minimum value: {bst2.find_minimum()}")
print(f"Height of tree: {bst2.find_height()}")

