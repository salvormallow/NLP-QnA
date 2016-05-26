import nltk
import re
import sys

from pprint import pprint
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer


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



# Read a file.questions and return a list with a list of 4 entry
# entry 1 = Question ID
# entry 2 = Actual question
# entry 3 = Question difficulty
# entry 4 = Question type
def question_parser( filename ):
    result = []
    questions = file_reader( filename, 'questions')
    match_question = re.findall(r'Question: (.+)',questions)
    match_id = re.findall(r'QuestionID: (.+)', questions)
    match_difficulty = re.findall(r'Difficulty: (.+)', questions)
    match_type = re.findall(r'Type: (.+)', questions)
    for i in range(0,len(match_id)):
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
    dict = {'np': 'NP: {<DT>?<JJ>*<NN>}',
            'vp': 'VP: {<V> <NP|PP>*}',
            'pp': 'PP: {<P> <DT>?<JJ>*<NN>}',
            }
    grammer = dict[type.lower()]
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
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = 'blogs-01'
    story_text = file_reader(input_file, 'story')
    print(story_text)
    sent_tokens = sentence_tokenizer(story_text)
    print(phrase_chunker(sent_tokens, "np"))



    # else:
    #     print("Please enter input file as an arguments to start like blog-01 ****NO EXTENSION****")
    #     exit()
