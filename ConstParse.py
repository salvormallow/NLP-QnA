import question_answering as qa
import re, nltk
from pprint import pprint
from nltk.tree import Tree
from nltk.stem.wordnet import WordNetLemmatizer


def create_tree_dict(filename='blogs-01', filetype='story'):
    text = qa.file_reader(filename, filetype + '.par')
    treedict = {}

    if (filetype.lower() == "question"):
        pattern = r'QuestionId: ([\w-]+)\n(.+)\n'
        questions = re.findall(pattern, text)
        for question in questions:
            treedict[question[0]] = nltk.tree.ParentedTree.fromstring(question[1])
    else:
        lines = text.split("\n")
        i = 0
        lines = lines[:-1]
        for line in lines:
            treedict[i] = nltk.tree.ParentedTree.fromstring(line)
            i += 1

    return treedict


def find_subtree(tree, string):
    left_wild = ""
    right_wild = ""
    if string[0] == "*":
        left_wild = "\w*"
        string = string[1:]
    if string[-1] == "*":
        right_wild = "\w*"
        string = string[:-1]
    NPs = list(tree.subtrees(
        filter=lambda x: re.match(r"\b" + left_wild + string.lower() + right_wild + r"\b", x.label().lower())))
    return NPs
    # map(lambda x: list(tree.subtrees(filter=lambda x: x.node == string)), NPs)
    # if(string in tree.leaves()):
    #     leaf_index = tree.leaves().index(string)
    #     tree_location = tree.leaf_treeposition(leaf_index)
    #     return tree_loca tion


def find_verb_phrase(tree, verb):
    subtrees = find_subtree(tree, "VB*")
    lemmatized_verb = qa.lemmatizer(verb, 'v')
    print(subtrees)
    for subtree in subtrees:
        if qa.lemmatizer(subtree[0], 'v') == lemmatized_verb:
            if subtree.parent() is None:
                return subtree
            else:
                return subtree.parent()


def find_where(story_name, file_type, question_no, sentence_no):
    treedict = create_tree_dict(story_name, file_type)
    sentence_no = 1
    root_verb = "was"
    v_phrase = find_verb_phrase(treedict[sentence_no], root_verb)

    subtree = find_subtree(v_phrase, "PP")
    print(" ".join(subtree[0].leaves()))


find_where("fables-02", "sch", 6, 2)
# file = qa.file_reader('blogs-01', 'sch')
# sents = qa.sentence_tokenizer(file)
# pattern = nltk.ParentedTree.fromstring("(PP)")
# subtree = pattern_matcher(pattern, treedict[4])
# coo = []
# print()
# coo = find_verb_phrase(treedict[2], "was")
# coo = find_subtree(coo, "PP")

# subtrees = find_subtree(treedict[3], "VB*")
# test = []
# for subtree in test:
#     for word in subtree:
#         w
# pprint(subtrees[0].)
# subtree = find_leaf(subtree[0], "VBD")[0].leaves()
# for subtree in subtrees:
#     if subtree[0][0] == "observed":
#         print (subtree.parent().parent())
# pprint(qa.lemmatizer(subtrees[0][0][0], 'v'))/
