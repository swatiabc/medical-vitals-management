import unittest

from utils.rb_tree.execute import RedBlackExecuter


class TestRedBlackTree(unittest.TestCase):
    def test_insertion(self):
        rb_tree = RedBlackExecuter()
        rb_tree.insert(5, 1)
        rb_tree.insert(3, 2)
        rb_tree.insert(7, 3)
        rb_tree.insert(2, 4)
        rb_tree.insert(4, 5)

        # Validate the Red-Black Tree properties
        root = rb_tree.root
        self.assertEqual(root.is_black(), True)

        # Validate the color of children
        self.assertTrue(root.left.is_black())
        self.assertTrue(root.right.is_black())
        self.assertTrue(root.left.left.is_red())
        self.assertTrue(root.left.right.is_red)

        # Validate the parent-child relationships
        self.assertEqual(root.left.parent, root)
        self.assertEqual(root.right.parent, root)
        self.assertEqual(root.left.left.parent, root.left)
        self.assertEqual(root.left.right.parent, root.left)

    def test_retrieval(self):
        rb_tree = RedBlackExecuter()
        rb_tree.insert(5, 1)
        rb_tree.insert(3, 2)
        rb_tree.insert(7, 3)
        rb_tree.insert(2, 4)
        rb_tree.insert(4, 5)

        # Test retrieval within a range
        result = rb_tree.retrieve_for_a_period(3, 5)
        self.assertEqual(result, [2, 4, 7])

        # Test retrieval with no values within the range
        result = rb_tree.retrieve_for_a_period(8, 10)
        self.assertEqual(result, [])

        # Test retrieval where the range includes only one value
        result = rb_tree.retrieve_for_a_period(4, 4)
        self.assertEqual(result, [2])

    def test_empty_tree(self):
        rb_tree = RedBlackExecuter()

        # Test retrieval on an empty tree
        result = rb_tree.retrieve_for_a_period(1, 10)
        self.assertEqual(result, [])

    def test_single_node_tree(self):
        rb_tree = RedBlackExecuter()
        rb_tree.insert(5, 1)

        # Test retrieval on a tree with a single node
        result = rb_tree.retrieve_for_a_period(1, 7)
        self.assertEqual(result, [5])

    def test_search(self):
        rb_tree = RedBlackExecuter()
        rb_tree.insert({5, 4}, 1)
        rb_tree.insert({3, 2}, 2)
        rb_tree.insert({7, 8}, 3)
        rb_tree.insert({5, 2}, 4)
        rb_tree.insert({4, 6}, 5)

        result = rb_tree.search(3)
        self.assertEqual({8, 7}, result)

    def test_search_empty(self):
        rb_tree = RedBlackExecuter()
        result = rb_tree.search(3)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
