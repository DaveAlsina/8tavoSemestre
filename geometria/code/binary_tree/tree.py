from node import Node, Node1D, Node2D 

class Tree():

    def __init__(self,
                 values: list,
                 sorted: bool = False, 
                 dimension: int = 1):

        if dimension == 1:
            self.list_of_nodes = Node1D.cast_to_nodes(values)
        elif dimension == 2:
            self.list_of_nodes = Node2D.cast_to_nodes(values)
        else:
            raise ValueError("dimension must be 1 or 2")

        self.sorted = sorted
        self.dimension = dimension
        self.build()


    def build(self): 
    
        self.root = self.list_of_nodes[0]
        
        #adds all the nodes
        for child in self.list_of_nodes[1:]:
            Tree.normal_insert(self.root, child)

    def inorder(self) -> list:

        """
            Reads the tree in inorder.
            and returns the list of values. Which should be ordered.
        """

        ordered_values = []
        Tree.inorder_recursion(self.root, ordered_values)

        return ordered_values
    
    def build_from_sorted_list(self, sorted_list: list):

        """
            Inserts the values from an ordered list.
            This is a more efficient way to build a tree.
        """
        self.root = Tree.build_from_sorted_list_recursion(sorted_list)

    @staticmethod
    def build_from_sorted_list_recursion(sorted_list: list):
        
        if len(sorted_list) == 0:
            return None
        
        #AAAAAAAAAAAAAAAAAA
        pass


    @staticmethod
    def inorder_recursion(root: Node, values: list):
        
        if root is None:
            return
        
        Tree.inorder_recursion(root.left, values)
        values.append(root.value)
        Tree.inorder_recursion(root.right, values)
    

    @staticmethod
    def normal_insert(root: Node, child: Node):
        
        if root is None:
            return
        
        #if the child is greater than the root, it goes to the right
        if (root < child):
            
            if root.right is None:
                root.right = child
                child.parent = root
            else:
                Tree.normal_insert(root.right, child)

        #if the child is less than or equal to the root, it goes to the left
        elif (root >= child):
            if root.left is None:
                root.left = child
                child.parent = root
            else:
                Tree.normal_insert(root.left, child)
    

        
