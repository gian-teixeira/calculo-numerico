
class Node():
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value

class OrderedSet():
    def __init__(self, base = None):
        self.root = None
        self.elementCount = 0

    def __len__(self):
        return self.elementCount

    def findPosition(self, element):
        left = 0
        right = len(self) - 1
        while left < right:
            middle = (left+right+1)/2
            if self.elements[middle] < element: left = middle + 1
            elif self.elements[middle] < element: right = middle - 1
            else: return middle
        return left

    def insert(self, value):
        newNode = Node(value)
        if self.root is None: self.root = newNode
        else:
            traverser = self.root
            while traverser is not None:
                if traverser.value < value: 
                    if traverser.right: traverser = traverser.right
                    else:
                        traverser.right = newNode
                        self.elementCount += 1
                        return True
                if traverser.value > value: 
                    if traverser.left: traverser = traverser.left
                    else:
                        traverser.left = newNode
                        self.elementCount += 1
                        return True
                else: return False
    
    
            