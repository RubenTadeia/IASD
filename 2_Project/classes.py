class Tree():
    """ Defines tree class """

    def __init__(self, root):

        if isinstance(root, tuple):

            if len(root) == 2:
                self.data = root[0]
                self.left = Tree(root[1])
                self.right = None

            elif len(root) == 3:
                self.data = root[0]
                self.left = Tree(root[1])
                self.right = Tree(root[2])

            elif len(root) > 3:
                print("Illegal sentence")
                exit()

        elif isinstance(root, str):
            self.data = root
            self.left = None
            self.right = None

        elif isinstance(root, Tree):
            self.data = root.data
            self.left = root.left
            self.right = root.right

    def insert_left(self, new_node):
        """ Inserts """
        if self.left is None:
            self.left = Tree(new_node)
        else:
            aux_tree = Tree(new_node)
            aux_tree.left = self.left
            self.left = aux_tree

    def insert_right(self, new_node):
        """ Inserts """
        if self.right is None:
            self.right = Tree(new_node)
        else:
            aux_tree = Tree(new_node)
            aux_tree.left = self.right
            self.right = aux_tree

    def change_root_data(self, obj):
        """ Changes the valu of the root """
        self.data = obj

    def get_root_data(self):
        """ Returns the value of the data """
        return self.data

    def get_root_left(self):
        """ Returns the left tree """
        return self.left

    def get_root_right(self):
        """ Returns the right tree """
        return self.right

    def print_tree(self, level):
        """ Prints the whole tree """

        print("Level: ", level)
        print("Root is: ", self.data)

        if isinstance(self.left, Tree):
            print("Left child is: ", self.left.get_root_data())
        else:
            print("Left child is: ", self.left)

        if isinstance(self.right, Tree):
            print("Right child is: ", self.right.get_root_data())
        else:
            print("Right child is: ", self.right)

        if isinstance(self.left, Tree):
            self.left.print_tree(level+1)
        if isinstance(self.right, Tree):
            self.right.print_tree(level+1)
