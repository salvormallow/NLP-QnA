import question_answering as qa
import re
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


create_tree_dict()

# text = text.split("\n")
# for question in text:
