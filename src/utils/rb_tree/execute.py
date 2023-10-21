"""
Red black Tree implementation

All the nodes to the left will be greater than the current node
All the nodes to the right will be less than or equal to current node
"""

from utils.rb_tree.node import Node


class RedBlackExecuter:
    def __init__(self) -> None:
        self.__nil_leaf = Node(None, None)
        self.__nil_leaf.convert_to_black()
        self.__root = self.__nil_leaf

    @property
    def root(self) -> Node:
        return self.__root

    def insert(self, key, value) -> Node:
        """
        :param key: object to insert into the RB Tree
        :param value: comparator which will decide the order of insertion
        :return: newly added RB tree node

        Insertion will be similar to normal BST.
        If node is greater than root, it will move to left branch
        If node is less than or equal to root, it will move to right branch
        """
        node = Node(key, value)
        current = self.__root
        parent = None

        while current and current != self.__nil_leaf:
            parent = current
            if current.value < value:
                current = current.left

            else:
                current = current.right

        if parent is None:
            self.__root = node

        elif parent.value > value:
            parent.right = node

        else:
            parent.left = node

        node.parent = parent

        if node.parent is None:
            node.convert_to_black()

        self.__fix_insert(node)
        return node

    def __fix_insert(self, node: Node) -> None:
        """
        :param node: newly added node
        :return:none

        This function will fix the RB tree tio make it more balanced
        """
        current = node
        while current != self.__root and current.parent.is_red():
            parent = current.parent
            g_parent = parent.parent
            if g_parent is None:
                break
            if parent == g_parent.left:
                uncle = g_parent.right

                if uncle and uncle.is_red():
                    uncle.convert_to_black()
                    parent.convert_to_black()
                    g_parent.convert_to_red()
                    current = g_parent

                else:
                    if current == parent.right:
                        current = parent
                        self.__left_rotate(current)
                    current.parent.convert_to_black()
                    current.parent.parent.convert_to_red()
                    self.__right_rotate(current.parent.parent)

            elif parent == g_parent.right:
                uncle = g_parent.left

                if uncle and uncle.is_red():
                    parent.convert_to_black()
                    uncle.convert_to_black()
                    g_parent.convert_to_red()
                    current = g_parent

                else:
                    if current == parent.left:
                        current = parent
                        self.__right_rotate(current)
                    current.parent.convert_to_black()
                    current.parent.parent.convert_to_red()
                    self.__left_rotate(current.parent.parent)

        self.__root.convert_to_black()

    def __left_rotate(self, node: Node) -> None:
        """
        :param node: Node around which tree will be rotated
        :return:
        """
        right_child = node.right
        node.right = right_child.left
        if right_child.left and right_child.left != self.__nil_leaf:
            right_child.left.parent = node
        right_child.parent = node.parent
        if node.parent is None:
            self.__root = right_child
        elif node == node.parent.left:
            node.parent.left = right_child
        else:
            node.parent.right = right_child
        right_child.left = node
        node.parent = right_child

    def __right_rotate(self, node: Node) -> None:
        """
        :param node: Node around which tree will be rotated
        :return:
        """
        left_child = node.left
        node.left = left_child.right
        if left_child.right and left_child.right != self.__nil_leaf:
            left_child.right.parent = node
        left_child.parent = node.parent
        if node.parent is None:
            self.__root = left_child
        elif node == node.parent.right:
            node.parent.right = left_child
        else:
            node.parent.left = left_child
        left_child.right = node
        node.parent = left_child

    def retrieve_for_a_period(self, value1, value2) -> list:
        """
        :param value1: first value of the node
        :param value2: last value of the node
        :return: list of instances from value 1 to value 2
        This function is used to fetch a list of node.instances where value is between value1 and value2
        """
        result = []
        if self.__root == self.__nil_leaf:
            return []
        stack = [self.__root]

        while len(stack) > 0:
            current = stack.pop()
            if value1 <= current.value <= value2:
                if current.right:
                    stack.append(current.right)
                if current.left:
                    stack.append(current.left)
                result.append(current.instance)
            elif (current.value < value1) and current.left:
                stack.append(current.left)
            elif (current.value > value2) and current.right:
                stack.append(current.right)

        return result

    def search(self, value):
        """

        :param value: value to search for (RBTree node.value)
        :return: returns the object (RBTree node.instance)
        """
        if self.__root == self.__nil_leaf:
            return False

        current = self.__root
        while current:
            if current.value < value:
                current = current.left
            elif current.value > value:
                current = current.right
            else:
                return current.instance
        return False
