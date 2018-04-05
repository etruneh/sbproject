from flask import abort, Flask, request
import json
import spacy
from spacy.tokens import Doc

app = Flask(__name__)

nlp = spacy.load('en')

categories = ['Dorm rules', 'Food', 'Transportation', 'Financial Aid', 'Logistics']

dorm_rules = ['Are pets allowed in the dorms?', 'Are power strips allowed?', 'What are the policies on space heaters in dorms?']

food = ['How many cafeterias are there on campus?', 'How expensive are the meal plans?', 'Are there kosher dining options?']

transportation = ['Can I bring my car to campus?', 'How much is a bus pass?', 'Do the buses run on the weekends?']

financial_aid = ['What is FAFSA?', 'How do I apply for a scholarship?', 'How much does tuition cost?']

logistics = ['When is move-in day?', 'Is there an orientation week for freshmen?', 'What day do classes start?']

all_categories = (dorm_rules, food, transportation, financial_aid, logistics)

def parse_text(string):
    output = nlp(string)
    return output

def check_similarity(string1, string2):
    doc1 = parse_text(string1)
    doc2 = parse_text(string2)
    return doc1.similarity(doc2)

def categorize_sentence(querytext):
    i = 0
    highest_similarity_float = 0 # the highest similarity score thus far
    highest_similarity_question = "" # the highest similarity question thus far
    highest_similarity_category_index = 0 # the index of the category of the highest similarity question thus far
    categoryindex_similarity = {}
    for each_set in all_categories:
        for question in each_set:
            similarity = check_similarity(querytext, question)
            if similarity > 0.70:
                categoryindex_similarity.update({i:similarity})
                if max(categoryindex_similarity.values()) == similarity:
                    highest_similarity_float = similarity
                    highest_similarity_question = question
                    highest_similarity_category_index = i
        i += 1
    if highest_similarity_float == 0:
        return 'Sentence was not above 70 percent similar with any category'

    # test = ["Category "+str(highest_similarity_category_index + 1)+": "+categories[highest_similarity_category_index], "Closest question: "+highest_similarity_question,"(for testing) similarity = "+str(highest_similarity_float),json.dumps(categoryindex_similarity)]
    # return test

    return ["Category "+str(highest_similarity_category_index + 1)+": "+categories[highest_similarity_category_index], "Closest question: "+highest_similarity_question]


@app.route("/")
def greeting():
    message = "Hello, welcome to my little API. Use via query string parameters."
    return message

# An API that lists available categories: their index/ID, a sample question
@app.route("/list_available_categories")
def list_available_categories():
    mydict = {}
    i = 0
    for each_set in all_categories:
        for sentence in each_set:
            category_and_index = "Category " + str(i+1) + ": " + categories[i]
            sample_question = each_set[0]
            mydict.update({category_and_index:sample_question})
        i += 1
    return json.dumps(mydict)

# An API that takes in a query text and returns the index/ID of the category it matched to and the closest question that made it match.
@app.route("/find_match")
def find_match():
    querytext = request.args.get("querytext")
    if not querytext:
        abort(400, "/find_match requires string argument 'querytext'")

    return json.dumps(categorize_sentence(querytext))

app.run()



