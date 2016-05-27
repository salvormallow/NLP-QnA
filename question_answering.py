import nltk
import re
import sys

from pprint import pprint
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer

filenames = ["fables-01", "fables-02", "fables-03", "fables-04", "blogs-01", "blogs-02", "blogs-03", "blogs-04"]

# Read the file and return a text
def file_reader( filename, extension ):
    with open('Data/'+filename+'.'+extension,'r') as file:
        text = file.read()
    file.close()
    return text

# Read string and return a list contains sentence tokenize of the string
def sentence_tokenizer( text ):
    token_list = nltk.sent_tokenize( text, "english")
    return token_list


def word_tokenizer(text):
    return nltk.word_tokenize(text)


# accepts a word and either 'n' or 'v' depending on whether the word is a noun or a verb
def lemmatizer(word, n_v):
    lmtzr = WordNetLemmatizer()
    return lmtzr.lemmatize(word, n_v)


def normalize(review):
    lowerText = review.lower()
    lowerText = nltk.word_tokenize(lowerText)

    stopWords = stopwords.words('english')
    stopWords.append("'s")
    stopWords.append("'t")

    normalizedText = (" ").join(word for word in lowerText if word not in stopWords)

    pattern = r"(?<!\w)(\W+)(?!\w)"
    normalizedText = re.sub(pattern, " ", normalizedText)
    normalizedText = re.sub(r"( ){2,}", " ", normalizedText)[:-1]
    normalizedText = normalizedText.split(sep=' ')

    return normalizedText


# Read a file.questions and return a list with a list of 4 entry
# entry 1 = Question ID
# entry 2 = Actual question
# entry 3 = Question difficulty
# entry 4 = Question type
def question_parser( filename ):
    result = []
    questions = file_reader( filename, 'questions')
    match_question = re.findall(r'Question: (.+)', questions)
    match_id = re.findall(r'QuestionID: (.+)', questions)
    match_difficulty = re.findall(r'Difficulty: (.+)', questions)
    match_type = re.findall(r'Type: (.+)', questions)
    for i in range(0, len(match_id)):
        each = []
        each.append( match_id[i] )
        each.append( match_question[i] )
        each.append( match_difficulty[i] )
        each.append( match_type[i] )
        result.append(each)

    return result

# Reads tokenize sentence and return a list for each of the sentences contains its noun phrase chunks
def phrase_chunker(text, type='np'):
    tokenize_story = []
    sentence_pos = []
    result = []

    grammer = """
            N: {<PRP>|<NN.*>}
            V: {<V.*>}
            ADJ: {<JJ.*>}
            NP: {<DT>? <ADJ>* <N>+}
            PP: {<IN> <NP>}
            VP: {<TO>? <V> (<NP>|<PP>)*}
            """
    chunker = nltk.RegexpParser(grammer)
    for sentence in text:
        tokenize_story.append( nltk.word_tokenize(sentence) )
    for sentence in tokenize_story:
        sentence_pos.append( nltk.pos_tag(sentence))
    for pos in sentence_pos:
        result.append( chunker.parse(pos) )
    result[0].draw()
    return result

# Argument format is filename example: blogs-01   ***NO EXTENSION***
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
                                file = fname + "." + qt + ".par"
                                Trees = read_con_parses(file)
                                tree = Trees[sent_num]
                                pattern = nltk.ParentedTree.fromstring("(VP (*) (PP))")
                                subtree = pattern_matcher(pattern, tree)
                                if subtree:
                                    pattern = nltk.ParentedTree.fromstring("(PP)")
                                    subtree2 = pattern_matcher(pattern, subtree)
                                    if subtree2:
                                        result = " ".join(subtree2.leaves())

                    print("Answer: " + str(result))
                    print("answer is in sentence: ", sent_num)
                    print("")

                    # Save your results in output file.
                    output_file.write("QuestionID: {}\n".format(qname))

                    output_file.write("Answer: {}\n\n".format(result))
                    #                    output_file.write("Answer is in sentence: {}\n\n".format(sent_num))

                    # output_file.close()



    # else:
    #     print("Please enter input file as an arguments to start like blog-01 ****NO EXTENSION****")
    #     exit()
