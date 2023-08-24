from typing import Union, List
from node import Node, Node1D, Node2D 

class Tree():

    def __init__(self,
                 values: List[Union[float, Node1D, Node2D]],
                 sorted: bool = False, 
                 dimension: int = 1, 
                 need_cast: bool = False):

        """
            Builds a tree from a list of values.

            Args:
            --------------
                values: list of values to be inserted in the tree.
                sorted: if the values are already sorted.
                dimension: dimension of the values. It can be 1 or 2.
                need_cast: if the values are not nodes, cast them to nodes.
            
            Returns:
            --------------
                tree: the tree.
        """

        if dimension == 1:
            #if the values are not nodes, cast them to nodes
            if need_cast:
                self.list_of_nodes = Node1D.cast_to_nodes(values)
            else:
                self.list_of_nodes = values
            
        elif dimension == 2:
            #if the values are not nodes, cast them to nodes
            if need_cast:
                self.list_of_nodes = Node2D.cast_to_nodes(values)
            else:
                self.list_of_nodes = values

        else:
            raise ValueError("dimension must be 1 or 2")

        self.root = None
        self.sorted = sorted
        self.dimension = dimension

        if not sorted:
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
            and returns the list of Nodes in ascending order, following 
            the order overloads of the Node class.
        """
        return Tree.inorder_recursion(self.root)

    def insert(self, node: Union[Node1D, Node2D]) -> None:
        """
            Inserts a node in the tree.
        """
        Tree.normal_insert(self.root, node)
    
    def build_from_sorted_list(self, sorted_list: List[Union[Node1D, Node2D]])-> 'Tree':

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
        
        middle = int(len(sorted_list)/2) #it's ok for both, even and odd lenght because python starts counting at 0
        root = sorted_list[middle]

        root.left = Tree.build_from_sorted_list_recursion(sorted_list[:middle])
        root.right = Tree.build_from_sorted_list_recursion(sorted_list[middle+1:])

        return root
        
        
    @staticmethod
    def inorder_recursion(root: Node) -> List[Union[Node1D, Node2D]]:
        """
            Reads the tree in inorder.
            and returns the list of Nodes in ascending order, following 
            the order overloads of the Node class.
        """

        if root is None:
            return []

        if root.left is None and root.right is None:
            return [root,]

        return Tree.inorder_recursion(root.left) + [root,] + Tree.inorder_recursion(root.right)
    

    @staticmethod
    def normal_insert(root: Node, child: Node) -> None:
        
        if root is None:
            return
        
        #if the child is greater than the root, it goes to the right
        if (root < child):
            
            if root.right is None:
                root.right = child
            else:
                Tree.normal_insert(root.right, child)

        #if the child is less than or equal to the root, it goes to the left
        elif (root >= child):
            if root.left is None:
                root.left = child
            else:
                Tree.normal_insert(root.left, child)