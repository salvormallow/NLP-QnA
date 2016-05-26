def dependency_parser(filename, type='story'):
    graphs = []
    items = []
    content = file_reader(filename, type + '.dep')
    lines = content.split('\n\n')
    dependency = [line.split('\n') for line in lines]
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


def find_what(story_name, file_type, question_no, sentence_no):
