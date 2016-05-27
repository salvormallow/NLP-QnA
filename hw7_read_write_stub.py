import zipfile, os
import re, nltk, operator
from collections import OrderedDict
import ConstParse as cp
from nltk.corpus import wordnet as wn
from nltk.tree import Tree


###############################################################################
## Utility Functions ##########################################################
###############################################################################

# returns a dictionary where the question numbers are the key
# and its items are another dict of difficulty, question, type, and answer
# e.g. story_dict = {'fables-01-1': {'Difficulty': x, 'Question': y, 'Type':}, 'fables-01-2': {...}, ...}
def getQA(filename):
    content = open('Data/' + filename, 'rU', encoding='latin1').read()
    question_dict = {}
    for m in re.finditer(
            r"QuestionID:\s*(?P<id>.*)\nQuestion:\s*(?P<ques>.*)\n(Answer:\s*(?P<answ>.*)\n){0,1}Difficulty:\s*(?P<diff>.*)\nType:\s*(?P<type>.*)\n+",
            content):
        qid = m.group("id")
        question_dict[qid] = {}
        question_dict[qid]['Question'] = m.group("ques")
        question_dict[qid]['Answer'] = m.group("answ")
        question_dict[qid]['Difficulty'] = m.group("diff")
        question_dict[qid]['Type'] = m.group("type")
    return question_dict


def get_data_dict(fname):
    data_dict = {}
    data_types = ["story", "sch", "questions"]
    parser_types = ["par", "dep"]
    for dt in data_types:
        data_dict[dt] = read_file(fname + "." + dt)
        for tp in parser_types:
            data_dict['{}.{}'.format(dt, tp)] = read_file(fname + "." + dt + "." + tp)
    return data_dict


# Read the file from disk
# filename can be fables-01.story, fables-01.sch, fables-01-.story.dep, fables-01.story.par
def read_file(filename):
    fh = open('Data/' + filename, 'r')
    text = fh.read()
    fh.close()
    return text


###############################################################################
## Question Answering Functions Baseline ######################################
###############################################################################
stopwords = nltk.corpus.stopwords.words("english")
stopwords.append("?")
stopwords.append("'s")
stopwords.append("'t")
stopwords.append(".")


def get_sentences(text):
    sentences = nltk.sent_tokenize(text)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]

    return sentences


def sanitize_text(text, stopwords):
    return set([t[0].lower() for t in text if t[0].lower() not in stopwords])


def lemma_sanitize(text, stopwords):
    return set([(t[0].lower(), t[1]) for t in text if t[0].lower() not in stopwords])


def find_best_sent(question, text, stopwords):
    answers = []
    count = 0
    for sent in text:
        # A list of all the word tokens in the sentence
        words_in_sent = sanitize_text(sent, stopwords)
        string_sent = " ".join(t for t in words_in_sent)

        overlapCount = 0
        for token in question:

            result = re.search(token, string_sent)
            if result:
                overlapCount += 1

        # Count the # of overlapping words between the Q and the A
        # & is the set intersection operator
        overlap = len(question & words_in_sent)
        overlap += overlapCount

        answers.append((overlap, sent, count))
        count += 1

    # Sort the results by the first element of the tuple (i.e., the count)
    # Sort answers from smallest to largest by default, so reverse it
    answers = sorted(answers, key=operator.itemgetter(0), reverse=True)

    # Return the best answer
    best_answer = (answers[0])
    return best_answer


def lemmatize_words(text):
    lmtzr = nltk.stem.wordnet.WordNetLemmatizer()
    stemmed_words = []
    for token in text:
        tag = token[1]
        word = token[0]
        if word is not None:
            if tag.startswith("V"):
                stemmed_words.append(lmtzr.lemmatize(word, 'v'))
            else:
                stemmed_words.append(word)
    return stemmed_words


# stuff for const trees



#######################################################################

if __name__ == '__main__':

    # Loop over the files in fables and blogs in order.
    output_file = open("train_my_answers.txt", "w", encoding="utf-8")
    cname_size_dict = OrderedDict();
    # we should set these to 4 and 4 when we are ready but just work on fables 1 for now
    cname_size_dict.update({"fables": 4})
    cname_size_dict.update({"blogs": 4})
    for cname, size in cname_size_dict.items():
        for i in range(0, size):
            # File format as fables-01, fables-11
            fname = "{0}-{1:02d}".format(cname, i + 1)
            print("File Name: " + fname)
            # output_file.write("File Name: " + fname + '\n')
            data_dict = get_data_dict(fname)

            questions = getQA("{}.questions".format(fname))
            for j in range(0, len(questions)):
                qname = "{0}-{1}".format(fname, j + 1)
                if qname in questions:
                    print("QuestionID: " + qname)
                    question = questions[qname]['Question']
                    print(question)
                    qcat = get_sentences(question)[0][0][0]
                    # print(qcat)
                    qtypes = questions[qname]['Type']

                    # Read the content of fname.questions.par, fname.questions.dep for hint.
                    question_par = data_dict["questions.par"]
                    question_dep = data_dict["questions.dep"]

                    answer = None
                    # qtypes can be "Story", "Sch", "Sch | Story"
                    for qt in qtypes.split("|"):
                        qt = qt.strip().lower()

                        # These are the text data where you can look for answers.
                        raw_text = data_dict[qt]
                        par_text = data_dict[qt + ".par"]
                        dep_text = data_dict[qt + ".dep"]

                        # TODO: You need to find the answer for this question
                        if qcat == "Yo":
                            print("fatty go boom")
                            sent_num = "I dunno"
                        else:
                            stem = lemma_sanitize(get_sentences(question)[0], stopwords)
                            normQ = set(lemmatize_words(stem))
                            answer = find_best_sent(normQ, get_sentences(raw_text), stopwords)
                            result = " ".join(t[0] for t in answer[1])
                            sent_num = answer[2]

                            if qcat == "Where":
                                qnum = int(qname[qname.rfind("-") + 1:])
                                # print(fname, qt, qnum, sent_num)
                                possible_result = cp.find_where(fname, qt, qnum - 1, sent_num)
                                if possible_result is not None:
                                    result = possible_result

                    print("Answer: " + str(result))
                    print("answer is in sentence: ", sent_num)
                    print("")

                    # Save your results in output file.
                    output_file.write("QuestionID: {}\n".format(qname))
                    output_file.write("Answer: {}\n\n".format(result))
                    #                    output_file.write("Answer is in sentence: {}\n\n".format(sent_num))

                    # output_file.close()
