class TreeNode:
  def __init__(self, value):
    self.value = value # data
    self.children = [] # references to other nodes

  def add_child(self, child_node):
    # creates parent-child relationship
    #print("Adding " + child_node.value)
    self.children.append(child_node) 
    
  def remove_child(self, child_node):
    # removes parent-child relationship
    #print("Removing " + child_node.value + " from " + self.value)
    self.children = [child for child in self.children 
                     if child is not child_node]

  def traverse(self):
    # moves through each node referenced from self downwards
    nodes_to_visit = [self]
    while len(nodes_to_visit) > 0:
      current_node = nodes_to_visit.pop()
      print(current_node.value)
      nodes_to_visit += current_node.children

  def is_in(self, value):
    #defines a method to determine if a node child is already assigned to a specific value
    for node in self.children:
      if node.value == value:
        return True  
    return False

  def get_child_node(self, value):
    #function to retrive a child node with a specific value from a parent node
    for node in self.children:
      if node.value == value:
        return node
    return None