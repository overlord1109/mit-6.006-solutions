import sys

class AVLNode(object):
	def __init__(self, key):
		self.key = key
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1
		self.subtree_height = 1

	def find(self, key):
		if(key == self.key):
			return self
		elif(key < self.key):
			if(self.left == None):
				return None
			else:
				return self.left.find(key)
		else:
			if(self.right == None):
				return None
			else:
				return self.right.find(key)

	def min(self):
		node = self
		while(node.left is not None):
			node = node.left
		return node

	def successor(self):
		if(self.right is not None):
			return self.right.min()
		else:
			node = self
			parent = self.parent
			while(parent is not None and node == parent.right):
				node = node.parent
				parent = parent.parent
			return parent

	def insert(self, key):
		self.subtree_height += 1
		if(key <= self.key):
			if(self.left == None):
				new_node = AVLNode(key)
				self.left = new_node
				new_node.parent = self
				return new_node
			else:
				return self.left.insert(key)
		else:
			if(self.right == None):
				new_node = AVLNode(key)
				self.right = new_node
				new_node.parent = self
				return new_node
			else:
				return self.right.insert(key)

	def delete(self):
		if(self.left == None or self.right == None):
			if(self.parent.right == self):
				self.parent.right = self.left or self.right
				if(self.parent.right is not None):
					self.parent.right.parent = self.parent
			else:
				self.parent.left = self.left or self.right
				if(self.parent.left is not None):
					self.parent.left.parent = self.parent
				if(self.parent.left is not None):
					self.parent.left.parent = self.parent
			return self
		else:
			successor = self.successor()
			successor.key, self.key = self.key, successor.key
			return successor.delete()
		return node

	def _str(self):
		"""Internal method for ASCII art."""
		label = str(self.key) + '(' + str(self.subtree_height) + ')'
		if self.left is None:
			left_lines, left_pos, left_width = [], 0, 0
		else:
			left_lines, left_pos, left_width = self.left._str()
		if self.right is None:
			right_lines, right_pos, right_width = [], 0, 0
		else:
			right_lines, right_pos, right_width = self.right._str()
		middle = max(right_pos + left_width - left_pos + 1, len(label), 2)
		pos = left_pos + middle // 2
		width = left_pos + middle + right_width - right_pos
		while len(left_lines) < len(right_lines):
			left_lines.append(' ' * left_width)
		while len(right_lines) < len(left_lines):
			right_lines.append(' ' * right_width)
		if (middle - len(label)) % 2 == 1 and self.parent is not None and \
			self is self.parent.left and len(label) < middle:
			label += '.'
		label = label.center(middle, '.')
		if label[0] == '.': label = ' ' + label[1:]
		if label[-1] == '.': label = label[:-1] + ' '
		lines = [' ' * left_pos + label + ' ' * (right_width - right_pos),
                 ' ' * left_pos + '/' + ' ' * (middle-2) +
                 '\\' + ' ' * (right_width - right_pos)] + \
          [left_line + ' ' * (width - left_width - right_width) + right_line
           for left_line, right_line in zip(left_lines, right_lines)]
		return lines, pos, width
	def __str__(self):
		return '\n'.join(self._str()[0])

class AugAVL(object):
	def __init__(self):
		self.root = None

	def insert(self, key):
		if(self.root == None):
			self.root = AVLNode(key)
			self.rebalance(self.root)
		else:
			node = self.root.insert(key)
			self.rebalance(node)

	def find(self, key):
		if(self.root == None):
			return None
		return self.root.find(key)

	def delete(self, key):
		if(key == self.root.key):
			pseudoroot = AVLNode(0)
			pseudoroot.left = self.root
			self.root.parent = pseudoroot
			deleted = self.root.delete()
			self.root = pseudoroot.left
			if self.root is not None:
				self.root.parent = None
		else:
			deleted = self.find(key).delete()
		self.rebalance(deleted.parent)

	def height(self, node):
		if(node is None):
			return -1
		else:
			return node.height

	def update_height(self, node):
		node.height = max(self.height(node.left), self.height(node.right)) + 1

	def subtree_height(self, node):
		if(node is None):
			return 0
		else:
			return node.subtree_height

	def update_subtree_height(self, node):
		node.subtree_height = self.subtree_height(node.left) + self.subtree_height(node.right) + 1

	def left_rotate(self, x):
		y = x.right
		y.parent = x.parent
		if(y.parent == None):
			self.root = y
		elif(y.parent.right == x):
			y.parent.right = y
		else:
			y.parent.left = y
		x.right = y.left
		if(y.left is not None):
			y.left.parent = x
		y.left = x
		x.parent = y
		self.update_height(x)
		self.update_height(y)
		self.update_subtree_height(x)
		self.update_subtree_height(y)		

	def right_rotate(self, x):
		y = x.left
		y.parent = x.parent
		if(y.parent == None):
			self.root = y
		elif(y.parent.left == x):
			y.parent.left = y
		else:
			y.parent.right = y
		x.left = y.right
		if(y.right is not None):
			y.right.parent = x
		y.right = x
		x.parent = y
		self.update_height(x)
		self.update_height(y)
		self.update_subtree_height(x)
		self.update_subtree_height(y)

	def rebalance(self, node):
		while(node is not None):
			self.update_height(node)
			self.update_subtree_height(node)
			if(self.height(node.left) > self.height(node.right) + 1):
				if(self.height(node.left.left) > self.height(node.left.right)):
					self.right_rotate(node)
				else:
					self.left_rotate(node.left)
					self.right_rotate(node)
			elif(self.height(node.right) > self.height(node.left) + 1):
				if(self.height(node.right.right) > self.height(node.right.left)):
					self.left_rotate(node)
				else:
					self.right_rotate(node.right)
					self.left_rotate(node)
			node = node.parent

	def rank(self, x):
		rank = 0
		node = self.root
		while(node is not None):
			if(x < node.key):
				node = node.left
			elif(x == node.key):
				rank = rank + 1
				if(node.left is not None):
					rank = rank + node.left.subtree_height
				break
			else:
				rank = rank + 1
				if(node.left is not None):
					rank = rank + node.left.subtree_height
				node = node.right
		return rank


	def count(self, first_key, last_key):
		if(self.find(first_key) is None):
			return self.rank(last_key) - self.rank(first_key)
		else:
			return self.rank(last_key) - self.rank(first_key) + 1

	def list(self, l, h):
		lca = self.lca(l, h)
		result = []
		self.node_list(lca, l, h, result)
		return result

	def node_list(self, node, l, h, result):
		if(node is None):
			return
		if(l <= node.key and node.key <= h):
			result.append(node.key)
		if(node.key >= l):
			self.node_list(node.left, l, h, result)
		if(node.key <= h):
			self.node_list(node.right, l, h, result)

	def lca(self, l, h):
		node = self.root
		while (not (node is None or (l <= node.key and h >= node.key))):
			if(l < node.key):
				node = node.left
			else:
				node = node.right
		return node

	def __str__(self):
		if self.root is None: return '<empty tree>'
		return str(self.root)

def main():
	tree = AugAVL()
	tree.insert(41)
	print("Insertion!")
	print(tree)
	tree.insert(20)
	print("Insertion!")
	print(tree)
	tree.insert(65)
	print("Insertion!")
	print(tree)
	tree.insert(11)
	print("Insertion!")
	print(tree)
	tree.insert(29)
	print("Insertion!")
	print(tree)
	tree.insert(26)
	print("Insertion!")
	print(tree)
	tree.insert(50)
	print("Insertion!")
	print(tree)
	tree.delete(29)
	print("Deletion!")
	tree.insert(16)
	print(tree)
	print(str(tree.rank(1000)))
	print(str(tree.count(16, 40)))
	print(str(tree.lca(16, 40).key))
	print(str(tree.list(11, 40)))

if __name__ == '__main__': main()