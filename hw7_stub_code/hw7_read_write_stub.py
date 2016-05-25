import zipfile, os
import re, nltk
from collections import OrderedDict

###############################################################################
## Utility Functions ##########################################################
###############################################################################

# returns a dictionary where the question numbers are the key
# and its items are another dict of difficulty, question, type, and answer
# e.g. story_dict = {'fables-01-1': {'Difficulty': x, 'Question': y, 'Type':}, 'fables-01-2': {...}, ...}
def getQA(filename):
    content = open(filename, 'rU', encoding='latin1').read()
    question_dict = {}
    for m in re.finditer(r"QuestionID:\s*(?P<id>.*)\nQuestion:\s*(?P<ques>.*)\n(Answer:\s*(?P<answ>.*)\n){0,1}Difficulty:\s*(?P<diff>.*)\nType:\s*(?P<type>.*)\n+", content):
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
    fh = open(filename, 'r')
    text = fh.read()
    fh.close()   
    return text

###############################################################################
## Question Answering Functions Baseline ######################################
###############################################################################


    
#######################################################################

if __name__ == '__main__':

    # Loop over the files in fables and blogs in order.
    output_file = open("train_my_answers.txt", "w", encoding="utf-8")
    cname_size_dict = OrderedDict();
    cname_size_dict.update({"fables":2})
    cname_size_dict.update({"blogs":1})
    for cname, size in cname_size_dict.items():
        for i in range (0, size):
            # File format as fables-01, fables-11
            fname = "{0}-{1:02d}".format(cname, i+1)
            #print("File Name: " + fname)
            data_dict = get_data_dict(fname)

            questions = getQA("{}.questions".format(fname))
            for j in range(0, len(questions)):
                qname = "{0}-{1}".format(fname, j+1)
                if qname in questions:
                    print("QuestionID: " + qname)
                    question = questions[qname]['Question']
                    print(question)
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
                        # TODO: You need to find the answer for this question.
                        answer = None
                                            
                    print("Answer: " + str(answer))
                    print("")

                    # Save your results in output file.
                    output_file.write("QuestionID: {}\n".format(qname))
                    output_file.write("Answer: {}\n\n".format(answer))
    output_file.close()

                    



