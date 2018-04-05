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

def categorize_sentence(string):
    i = 0
    for each_set in all_categories:
        for sentence in each_set:
            if checkSimilarity(string, sentence) > 0.70:
                # print(checkSimilarity(string, sentence))
                return ["Category "+str(i+1)+": "+categories[i], "Closest question: "+sentence]
        i += 1
    if i == 5:
        return 'Sentence was not above 70 percent similar with any category'
    return null


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
        abort(400, "/hello requires string argument 'querytext'")

    return json.dumps(categorizeSentence(querytext))

app.run()



