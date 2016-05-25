'''
Created on May 14, 2014
@author: reid

Modified on May 21, 2015
'''

import sys, nltk
from nltk.tree import Tree
from nltk.parse import DependencyGraph

# Read the constituency parse from the line and construct the Tree
def read_con_parses(parfile):
    fh = open(parfile, 'r')
    lines = fh.readlines()
    fh.close()
    return [Tree.fromstring(line) for line in lines]

def matches(pattern, root):
    if root is None and pattern is None: return root
    elif pattern is None:                return root
    elif root is None:                   return None
    
    plabel = pattern if isinstance(pattern, str) else pattern.label()
    rlabel = root if isinstance(root, str) else root.label()
    
    if plabel == "*":
        return root
    elif plabel == rlabel:
        for pchild, rchild in zip(pattern, root):
            match = matches(pchild, rchild) 
            if match is None:
                return None
        return root
    
    return None

def process_con(trees):
    tree = trees[1]
    
    pattern = nltk.ParentedTree.fromstring("(VP (*) (PP))")
    
    # get the first child of the tree because there
    # is a dummy ROOT node in there
    for subtree in tree[0].subtrees():
        node = matches(pattern, subtree)
        if node is not None:
            print(node)

# Read the lines of an individual dependency parse
def read_dep(fh):
    dep_lines = []
    for line in fh:
        line = line.strip()
        if len(line) == 0:
            return "\n".join(dep_lines)
        dep_lines.append(line)
        
    return "\n".join(dep_lines) if len(dep_lines) > 0 else None          

# Read the dependency parses from a file
def read_dep_parses(depfile):
    fh = open(depfile, 'r')

    # list to store the results
    graphs = []
    
    # Read the lines containing the first parse.
    dep = read_dep(fh)
    
    # While there are more lines:
    # 1) create the DependencyGraph
    # 2) add it to our list
    # 3) try again until we're done
    while dep is not None:
        graph = DependencyGraph(dep)
        graphs.append(graph)
        
        dep = read_dep(fh)
    fh.close()
    
    return graphs 
    
def process_dep(graphs):
    graph = graphs[1]
    
    # TODO
    

if __name__ == '__main__':
    # A file containing a list of constituency parses (i.e. ending in .par)
    # Each parse is on its own line and there should be no blank lines in
    # between.
    parfile = sys.argv[1]
    
    # A file containing a list of dependency parses (i.e. ending in .dep)
    # Each line represents the dependency triple between the dependent, its
    # governor and the grammatical relation that holds between them.
    depfile = sys.argv[2]
    
    # Read the constituency parses into a list 
    con_parses = read_con_parses(parfile)
    
    # Read the dependency parses into a list
    dep_parses = read_dep_parses(depfile)

    process_con(con_parses)
    process_dep(dep_parses)
