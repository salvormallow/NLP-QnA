import question_answering as qa
import nltk
from pprint import pprint


def dependency_parser(filename, type='story'):
    graphs = []
    items = []
    content = qa.file_reader(filename, type + '.dep')
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


dependency_parser('fables-01', 'questions')
# def find_what(story_name, file_type, question_no, sentence_no):
