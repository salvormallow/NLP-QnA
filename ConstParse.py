
import re, nltk
from pprint import pprint
from nltk.stem.wordnet import WordNetLemmatizer


def file_reader(filename, extension):
    with open('Data/' + filename + '.' + extension, 'r') as file:
        text = file.read()
    file.close()
    return text


def sentence_tokenizer(text):
    token_list = nltk.sent_tokenize(text, "english")
    return token_list


def word_tokenizer(text):
    return nltk.word_tokenize(text)


# accepts a word and either 'n' or 'v' depending on whether the word is a noun or a verb
def lemmatizer(word, n_v):
    lmtzr = WordNetLemmatizer()
    return lmtzr.lemmatize(word, n_v)


def question_parser(filename):
    result = []
    questions = file_reader(filename, 'questions')
    match_question = re.findall(r'Question: (.+)', questions)
    match_id = re.findall(r'QuestionID: (.+)', questions)
    match_difficulty = re.findall(r'Difficulty: (.+)', questions)
    match_type = re.findall(r'Type: (.+)', questions)
    for i in range(0, len(match_id)):
        each = []
        each.append(match_id[i])
        each.append(match_question[i])
        each.append(match_difficulty[i])
        each.append(match_type[i])
        result.append(each)

    return result

def create_tree_dict(filename='blogs-01', filetype='story'):
    text = file_reader(filename, filetype + '.par')
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


def dependency_parser(filename, type='story'):
    graphs = []
    items = []
    content = file_reader(filename, type + '.dep')
    lines = content.split('\n\n')
    dependency = [line.split('\n') for line in lines]
    if (type == 'questions'):
        dependency = sorted(dependency, key=lambda tup: (len(tup[0])))
        for i in range(0, len(dependency)):
            dependency[i] = dependency[i][1:]
        dependency = dependency[1:len(dependency)]
    else:
        dependency = dependency[0:len(dependency) - 1]

    # for i in dependency:
    #     print(i)
    #     print('\n')

    for i in dependency:
        dep = []
        dep = nltk.parse.DependencyGraph(i)
        graphs.append(dep)
    for i in graphs:
        item = []
        item = i.nodes.values()
        items.append(item)
    return items


def get_root(story_name, question_no):
    result = []
    question_dep = dependency_parser(story_name, 'questions')
    question = question_dep[question_no]
    # root = question['deps']
    for i in question:
        deps = i['deps']
        if len(deps['ROOT']) > 0:
            root = (deps['ROOT'][0])
    for i in question:
        if i['address'] == root:
            result.append(i['lemma'])
            result.append(i['tag'])
            result.append(list(i['deps']))
            result[2].remove('ROOT')
    return (result)


def find_subtree(tree, string):
    left_wild = ""
    right_wild = ""
    if string[0] == "*":
        left_wild = "\w*"
        string = string[1:]
    if string[-1] == "*":
        right_wild = "\w*"
        string = string[:-1]
    pattern = r"\b" + left_wild + string.lower() + right_wild + r"\b"
    NPs = list(tree.subtrees(
        filter=lambda x: re.match(pattern, x.label().lower())))
    return NPs
    # map(lambda x: list(tree.subtrees(filter=lambda x: x.node == string)), NPs)
    # if(string in tree.leaves()):
    #     leaf_index = tree.leaves().index(string)
    #     tree_location = tree.leaf_treeposition(leaf_index)
    #     return tree_loca tion


def find_supertree(tree, string):
    left_wild = ""
    right_wild = ""
    if string[0] == "*":
        left_wild = "\w*"
        string = string[1:]
    if string[-1] == "*":
        right_wild = "\w*"
        string = string[:-1]
    pattern = r"\b" + left_wild + string.lower() + right_wild + r"\b"
    tree = tree.parent().parent()
    while (tree.parent() is not None):
        tree = tree.parent()
        if re.match(pattern, tree.label().lower()):
            pprint(tree.leaves())
            return tree


def find_verb_phrase(tree, verb, lemmatize=True):
    subtrees = find_subtree(tree, "VB*")
    if lemmatize:
        lemmatized_verb = lemmatizer(verb, 'v')
    else:
        lemmatized_verb = verb
    for subtree in subtrees:
        if lemmatizer(subtree[0], 'v') == lemmatized_verb:
            if subtree.parent() is None:
                return subtree
            else:
                return subtree.parent()


def find_direct_child(tree, string):
    left_wild = ""
    right_wild = ""
    if string[0] == "*":
        left_wild = "\w*"
        string = string[1:]
    if string[-1] == "*":
        right_wild = "\w*"
        string = string[:-1]
    pattern = r"\b" + left_wild + string.lower() + right_wild + r"\b"
    if tree is not None:
        for subtree in tree:
            if re.match(pattern, subtree.label().lower()):
                return subtree


def find_where(story_name, file_type, question_no, sentence_no):
    treedict = create_tree_dict(story_name, file_type)
    root_verb = get_root(story_name, question_no)[0]
    # print(root_verb)
    # treedict[sentence_no].draw()
    # print(root_verb)
    v_phrase = find_verb_phrase(treedict[sentence_no], root_verb)
    # v_phrase.draw()
    if v_phrase is None:
        v_phrase = find_verb_phrase(treedict[sentence_no], root_verb, False)
    if v_phrase is None:
        v_phrase = treedict[sentence_no]
    direct_child = find_direct_child(v_phrase, "PP")
    # direct_child.pprint()
    if direct_child is not None:
        return (" ".join(direct_child.leaves()))
    else:
        indirect_child = find_subtree(v_phrase, "PP")
        # indirect_child[0].draw()
        if len(indirect_child) > 0 and len(indirect_child[0]) == 1:
            return (" ".join(indirect_child[0].leaves()))
        else:
            return None
            # print(" ".join(subtree[0].leaves()))


#
def find_who(story_name, file_type, question_no, sentence_no):
    treedict = create_tree_dict(story_name, file_type)
    root_verb = get_root(story_name, question_no)
    v_phrase = find_verb_phrase(treedict[sentence_no], root_verb)
    v_phrase = find_supertree(v_phrase, "S")
    for subtree in v_phrase:
        if subtree.label() == "NP":
            pprint(" ".join(subtree.leaves()))


def get_parent_noun_phrase(tree, string):
    subtree = find_subtree(tree, "NN")
    for tree in subtree:
        if re.match(string, tree[0]):
            subtree = tree
            break

    subtree = find_supertree(subtree, "NP")


pprint(find_where('fables-01', 'sch', 9, 3))
# 'fables-01', 'story', 1, 1
# 'fables-01', 'sch', 5, 5
# 'fables-01', 'sch', 9, 3
# 'fables-02', 'sch', 3, 2
# 'fables-03', 'story', 6, 4
# 'fables-03', 'story', 10, 5
# 'fables-04', 'sch', 3, 2
# 'blogs-01', 'story', 3, 4
