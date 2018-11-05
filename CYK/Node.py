#class Node:
#	def __init__(self, root, left, right, end):
#		self.root = root
#		self.left = left
#		self.right = right
#		self.terminal = end
#		self.status = True
#		if end == None:
#			self.status = False
#
#	def root(self):
#		return self.root
#
#	def left(self):
#		return self.left
#
#	def right(self):
#		return self.right
#
#	def status(self):
#		return self.status
#
#	def terminal(self):
#		return self.terminal
class Node:
    def __init__(self,name,lrow,lcol,lorder,rrow,rcol,rorder,terminal):
        self.name = name
        self.lrow = lrow
        self.lcol = lcol
        self.lorder = lorder
        self.rrow = rrow
        self.rcol = rcol
        self.rorder = rorder
        self.terminal = terminal