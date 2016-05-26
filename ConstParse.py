import question_answering as qa
import re, nltk
from pprint import pprint
from nltk.tree import Tree


def create_tree_dict(filename='blogs-01', filetype='story'):
    text = qa.file_reader(filename + "." + filetype, 'par')
    treedict = {}

    if (filetype.lower() == "question"):
        pattern = r'QuestionId: ([\w-]+)\n(.+)\n'
        questions = re.findall(pattern, text)
        for question in questions:
            treedict[question[0]] = Tree.fromstring(question[1])
    else:
        lines = text.split("\n")
        i = 0
        lines = lines[:-1]
        for line in lines:
            treedict[i] = Tree.fromstring(line)
            i += 1

    return treedict


def matches(pattern, root):
    if root is None and pattern is None:
        return root

    elif pattern is None:
        return root

    elif root is None:
        return None

    # A node in a tree can either be a string (if it is a leaf) or node
    plabel = pattern if isinstance(pattern, str) else pattern.label()
    rlabel = root if isinstance(root, str) else root.label()

    # If our pattern label is the * then match no matter what
    if plabel == "*":
        return root
    # Otherwise they labels need to match
    elif plabel == rlabel:
        # If there is a match we need to check that all the children match
        # Minor bug (what happens if the pattern has more children than the tree)
        for pchild, rchild in zip(pattern, root):
            match = matches(pchild, rchild)
            if match is None:
                return None
        return root

    return None


def pattern_matcher(pattern, tree):
    for subtree in tree.subtrees():
        node = matches(pattern, subtree)
        if node is not None:
            return node
    return None


treedict = create_tree_dict("blogs-01", "sch")
# file = qa.file_reader('blogs-01', 'sch')
# sents = qa.sentence_tokenizer(file)
pprint(treedict[4])
pattern = nltk.ParentedTree.fromstring("(PP)")
subtree = pattern_matcher(pattern, treedict[4])
pprint(subtree)
