class Branch(object):
	def __init__(self,name='Root',parent=None):
		self.name = name
		self.parent = parent
		self.children = []
		self._stringFormat = []

	def _convertToString(self):
		name = ''
		for item in self.children:
			name += item._convertToString()
		else:
			return self.name + '\n' + name

	def __hash__(self):
		return hash(self.stringFormat)

	@property
	def stringFormat(self):
		if not len(self._stringFormat):
			self._stringFormat = self._convertToString()
		return self._stringFormat

	def printChildren(self):
		for item in self.children:
			print item.name

	def printChildrenWithGrandchild(self):
		for item in self.children:
			print item.name
			item.printChildrenWithGrandchild()

	def getChildBy(self,child):
		for item in self.children:
			if item.name.strip() == child.strip():
				return item
		else:
			print "Given child not found"

class Tree():
	def __init__(self,conf):
		self.root = Branch()
		self._parse(conf)

	def _parse(self,conf):
		for item in conf:
			depth = len(item) - len(item.lstrip(' '))
			if depth == 0:
				first_branch = Branch(item,self.root)
				self.root.children.append(first_branch)
				hierachy={depth:first_branch}
			else:
				new_branch = Branch(item, parent=hierachy[depth - 1])
				hierachy[depth - 1].children.append(new_branch)
				hierachy[depth] = new_branch

	@staticmethod
	def compare(obj1, obj2):
		if isinstance(obj1,Tree) and isinstance(obj2,Tree):
			leftOnly = [item for item in obj1.root.children if item.name not in [i.name for i in obj2.root.children]]
			rightOnly = [item for item in obj2.root.children if item.name not in [i.name for i in obj1.root.children]]
			modifyLeft = []
			modifyRight = []
			modifyPairs = []
			for child in [item for item in obj1.root.children if item.name in [i.name for i in obj2.root.children]]:
				if hash(child) != hash(obj2.root.getChildBy(child.name)):
					modifyLeft.append(child)
					modifyRight.append(obj2.root.getChildBy(child.name))
					modifyPairs.append((child, obj2.root.getChildBy(child.name)))
			return leftOnly, rightOnly, modifyLeft, modifyRight, modifyPairs
		else:
			print "Error: args must be instance of Tree"

	def search(self,keyword):
		match = []
		import re
		for item in self.root.children:
			if re.search(keyword, item.stringFormat, re.MULTILINE):
				match.append(item)
		return match
