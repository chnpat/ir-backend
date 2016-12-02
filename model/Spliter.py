import nltk, re, pprint, string
from model.model import *
from nltk import word_tokenize
from nltk.corpus import stopwords

class Spliter:

    '''
    Class Constructor
    '''
    def __init__(self):
        self.course_index = {}
        self.all_term = dict()

    '''
    Word Stemming Function
    '''
    def stemmer(self, word):
        regexp = r'^(.*?)(ing|ly|ed|ious|ies|ive|es|s|ment)?$'
        stem, suffix = re.findall(regexp, word)[0]
        return stem

    '''
    A Function to get only course title and description which are tokenized
    '''
    def get_title_desc_token(self, c_id):
        c = Course().get(Course.course_id == c_id)
        c.course_description = c.course_description.replace('\n',' ').replace('.',' ')
        data = c.course_title.lower() + " " + c.course_description.lower()
        return [self.stemmer(t) for t in word_tokenize(re.sub(r'[^a-zA-Z0-9 \n\.]',' ',data)) if t.isalpha()]

    '''
    A Function to generate a dictionary of all index terms
    If the index term dictionary is indexed once, it will skip the generation.
    '''
    def get_all_term(self):
        if len(self.all_term.keys()) == 0:
            result = []
            for c in Course().select():
                result += self.get_title_desc_token(c.course_id)
            self.all_term = dict.fromkeys([str(s) for s in result if s != ''],0)
        return self.all_term

    '''
    A Function to generate dictonary of index terms for each course
    '''
    def generate_index_per_doc(self, course):
        result = self.get_all_term()
        x = nltk.FreqDist(self.get_title_desc_token(course.course_id))
        result.update(x)
        self.course_index[str(course.course_id)] = result

    '''
    A Function to initialize inverted index file with index terms
    '''
    def init_file(self, infile):
        a_t = self.get_all_term().keys()
        infile.write('Document')
        for t in a_t:
            infile.write(','+str(t))
        infile.write('\n')
        return a_t

    '''
    A Function to print data index into file
    '''
    def print_to_file(self, k_list, course_id, infile):
        infile.write(course_id)
        for k in k_list:
            if k in self.course_index[course_id].keys():
                infile.write(str(self.course_index[course_id][k])+',')
        infile.write('\n')
        
    '''
    A Function as main in spliter class for creating inverted index file
    '''
    def create_index_file(self):
        infile = open('iif.csv','w')
        k_list = self.init_file(infile)
        for course in Course().select():
            self.generate_index_per_doc(course)
            self.print_to_file(k_list, str(course.course_id), infile)
        infile.close()
        print("Inverted Index File Creation done!!")


    def get_JSON(self, tuples_list):
        json = "{courses:["
        for c_id, sim in tuples_list:
            for course in Course().select():
                if c_id[:-1] == str(course.course_id):                    
                    json += "{"
                    json += "'course_id':'" + str(course.course_id) + "',"
                    json += "'course_title':'" + course.course_title + "',"
                    json += "'course_description':'" + course.course_description + "',"
                    json += "'language':'" + course.language + "',"
                    json += "'level':'" + course.level + "',"
                    json += "'student_enrolled':" + str(course.student_enrolled) + ","
                    json += "'ratings':" + str(course.ratings) + ","
                    json += "'overall_rating':" + str(course.overall_rating) + ","
                    json += "'course_url':'" + course.course_url + "',"
                    json += "'cover_image':'" + course.cover_image + "',"
                    json += "'source':'" + course.source + "'"
                    json += "},"
        json = json[:-1] + "]}"
        return json
