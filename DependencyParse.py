import question_answering as qa
import nltk
from pprint import pprint

def dependency_parser(filename, type='story'):
    graphs = []
    items = []
    content = qa.file_reader(filename, type + '.dep')
    lines = content.split('\n\n')
    dependency = [line.split('\n') for line in lines]
    pprint(dependency[0][0])
    dependency = sorted(dependency, key=lambda tup: (len(tup[0])))
    dependency = dependency[1:]
    pprint(dependency)
    if (type == 'questions'):
        for i in range(0, len(dependency)):
            dependency[i] = dependency[i][1:]
    for i in dependency:
        dep = []
        dep = nltk.parse.DependencyGraph(i)
        graphs.append(dep)
    for i in graphs:
        item = []
        item = i.nodes.values()
        items.append(item)

    for i in items[6]:
        print(i)
        print('\n')


dependency_parser('fables-01', 'questions')
# def find_what(story_name, file_type, question_no, sentence_no):
