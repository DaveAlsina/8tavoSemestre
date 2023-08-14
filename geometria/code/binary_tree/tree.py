from typing import Union, List
from node import Node, Node1D, Node2D 

class Tree():

    def __init__(self,
                 values: List[Union[float, Node1D, Node2D]],
                 sorted: bool = False, 
                 dimension: int = 1):

        if dimension == 1:
            #if the values are not nodes, cast them to nodes
            if not isinstance(values[0], Node1D):
                self.list_of_nodes = Node1D.cast_to_nodes(values)
            else:
                self.list_of_nodes = values
            
        elif dimension == 2:
            #if the values are not nodes, cast them to nodes
            if not isinstance(values[0], Node2D):
                self.list_of_nodes = Node2D.cast_to_nodes(values)
            else:
                self.list_of_nodes = values
        else:
            raise ValueError("dimension must be 1 or 2")

        self.sorted = sorted
        self.dimension = dimension
        self.build()

    def build(self) -> None:
        """
            Builds the tree from the list of nodes.
        """
        self.root = self.list_of_nodes[0]
        
        #adds all the nodes
        for child in self.list_of_nodes[1:]:
            Tree.normal_insert(self.root, child)

    def inorder(self) -> List[Union[Node1D, Node2D]]:

        """
            Reads the tree in inorder.
            and returns the list of values. Which should be ordered.
        """

        ordered_values = []
        Tree.inorder_recursion(self.root, ordered_values)

        if self.dimension == 1:
            ordered_values = Node1D.cast_to_nodes(ordered_values)
        elif self.dimension == 2:
            ordered_values = Node2D.cast_to_nodes(ordered_values)

        return ordered_values
    
    def build_from_sorted_list(self, sorted_list: list)-> 'Tree':

        """
            Inserts the values from an ordered list.
            This is a more efficient way to build a tree.
        """
        root = Tree.build_from_sorted_list_recursion(sorted_list)

        #builds the new tree
        tree = Tree(sorted_list, sorted=True, dimension=self.dimension)
        tree.root = root

        return tree

    @staticmethod
    def build_from_sorted_list_recursion(sorted_list: list) -> Union[Node1D, Node2D]:
        """
            Inserts the values from an ordered list, in ascending order.
        """
        
        if len(sorted_list) == 0:
            return None
        
        elif len(sorted_list) == 1:
            return sorted_list[0]
        
        elif len(sorted_list) == 2:
            root = sorted_list[1]
            root.left = sorted_list[0]
            return root
        
        middle = len(sorted_list) // 2
        root = sorted_list[middle]

        root.left = Tree.build_from_sorted_list_recursion(sorted_list[:middle])
        root.right = Tree.build_from_sorted_list_recursion(sorted_list[middle+1:])

        return root
        
    @staticmethod
    def inorder_recursion(root: Node, values: list) -> None:
        
        if root is None:
            return
        
        Tree.inorder_recursion(root.left, values)
        values.append(root.value)
        Tree.inorder_recursion(root.right, values)
    

    @staticmethod
    def normal_insert(root: Node, child: Node) -> None:
        
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
    