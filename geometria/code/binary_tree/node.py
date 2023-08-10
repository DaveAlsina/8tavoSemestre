class Node():

    def __init__(self, value):
        self.value = value
        self.parent = None
        self.left = None
        self.right = None

    def __repr__(self):
        return f"Node({self.value})"

    #classes inheriting from this class must implement these methods
    def __gt__(self, other):
        raise NotImplementedError
    
    def __lt__(self, other):
        raise NotImplementedError
    
    def __eq__(self, other):
        raise NotImplementedError
    
    def __ge__(self, other):
        raise NotImplementedError
    
    def __le__(self, other):
        raise NotImplementedError
    
    @staticmethod
    def cast_to_nodes(values: list) -> list:
        raise NotImplementedError


class Node1D(Node):

    def __init__(self, value: int):
        self.value = value
        self.parent = None
        self.left = None
        self.right = None


    #=====================================
    #       order comparison methods
    #=====================================
    def __gt__(self, other: 'Node1D'):
        return self.value > other.value

    def __lt__(self, other: 'Node1D'):
        return self.value < other.value

    def __eq__(self, other: 'Node1D'):
        return self.value == other.value

    def __ge__(self, other: 'Node1D'):
        return self.value >= other.value
    
    def __le__(self, other: 'Node1D'):
        return self.value <= other.value

    @staticmethod
    def cast_to_nodes(values: list) -> list:
        return [Node1D(v) for v in values]

class Node2D(Node):
    
        def __init__(self, value: tuple):
            """
                Creates a node with a value of 2 elements.

                value: tuple of 2 elements, where the first element is the x coordinate 
                and the second element is the y coordinate.
            """

            self.value = value
            self.parent = None
            self.left = None
            self.right = None
    
        #=====================================
        #       order comparison methods
        #=====================================
        def __gt__(self, other: 'Node2D'):
            if self.value[1] > other.value[1]:
                return True
            elif self.value[1] == other.value[1]:
                return self.value[0] > other.value[0]
    
        def __lt__(self, other: 'Node2D'):
            
            if self.value[1] > other.value[1]:
                return True
            elif self.value[1] == other.value[1]:
                return self.value[0] < other.value[0]
    
        def __eq__(self, other: 'Node2D'):
            return self.value == other.value
    
        def __ge__(self, other: 'Node2D'):
            return (self > other) or (self == other)
        
        def __le__(self, other: 'Node2D'):
            return (self < other) or (self == other)
    
        @staticmethod
        def cast_to_nodes(values: list) -> list:
            return [Node2D(v) for v in values]
