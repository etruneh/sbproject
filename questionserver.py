from flask import abort, Flask, request
import json
import spacy
from spacy.tokens import Doc
from collections import defaultdict

app = Flask(__name__)

nlp = spacy.load('en')

dorm_rules = ['are pets allowed in the dorms?', 'are power strips allowed?', 'what are the policies on space heaters in dorms?']

food = ['how many cafeterias are there on campus?', 'how expensive are the meal plans?', 'are there kosher dining options?']

transportation = ['can I bring my car to campus?', 'how much is a bus pass?', 'do the buses run on the weekends?']

financial_aid = ['what is fafsa?', 'How do I apply for a scholarship?', 'how much does tuition cost?']

logistics = ['when is move-in day?', 'is there an orientation week for freshmen?', 'what day do classes start?']

all_categories = defaultdict(list)
all_categories['dorm rules'] = dorm_rules
all_categories['food'] = food
all_categories['transportation'] = transportation
all_categories['financial aid'] = financial_aid
all_categories['logistics'] = logistics

def parse_text(string):
    output = nlp(string)
    return output

def check_similarity(string1, string2):
    doc1 = parse_text(string1)
    doc2 = parse_text(string2)
    return doc1.similarity(doc2)

def categorize_sentence(query_text):
    matches = defaultdict(tuple) # key = the string category name, value = the tuple (best sentence, its similarity score)
    for category_name,category_list in all_categories.items():
        for sentence in category_list:
            score = check_similarity(query_text, sentence)
            if score == 1.0:
                return("Perfect match within category: {}. Question match: {} (similarity score = {})".format(category_name,sentence,score))
            if score > 0.70:
                if category_name in matches.keys():
                    if score > matches[category_name][1]:
                        matches[category_name] = (sentence, score)
                else:
                    matches[category_name] = (sentence,score)
    best_match = max(matches, key = lambda key: matches[key][1])
    output = ("| Best category match: {} | Most similar sentence: {} (similarity = {})".format(best_match,matches[best_match][0],matches[best_match][1]))
    return output


@app.route("/")
def greeting():
    # message = "Hello, welcome to my little API. Use via query string parameters."
    message = "Hello and welcome! APIs for you to use: /list_available_categories, /find_match, /add_query_text, /add_category"

    return message

# An API that lists available categories: their name, a sample question
@app.route("/list_available_categories")
def list_available_categories():
    output = [name +": "+questions[0] if len(questions) != 0 else name for name,questions in all_categories.items()]

    return json.dumps("Available categories (and sample questions): "+str(output))

# An API that takes in a query text and returns the category it matched to and the closest question that made it match.
@app.route("/find_match")
def find_match():
    query_text = request.args.get("query_text")
    if not query_text:
        abort(400, "/find_match requires string argument 'query_text'")

    return json.dumps(categorize_sentence(query_text))

# An API that takes a category name and a query text and then adds the query text to the category.
@app.route("/add_query_text")
def add_query_text():
    query_text = request.args.get("query_text")
    query_text = query_text.lower()
    category_to_update = request.args.get("category")
    category_to_update = category_to_update.lower()
    message = ""
    if (not query_text) or (not category_to_update):
        abort(400, "/add_query_text requires two string arguments, 'query_text' and 'category'")

    # keys = [key for key in all_categories.keys()]
    # if category_to_update not in keys:
    #     return json.dumps(keys)
    #     return "Category {} does not exist. Go to /add_category to create it.".format(category_to_update)

    # TODO: this string comparison is not working
    found = False
    for key in all_categories.keys():
        if category_to_update.lower() == key.lower():
            found == True
    if found == False:
        return "Category {} does not exist. Go to /add_category to create it.".format(category_to_update)

    for category,questions in all_categories.items():
        for question in questions:
            if query_text == question.lower():
                if category == category_to_update:
                    return "Question already exists in this category"
                else:
                    return "Question already exists within category {}".format(category)

    all_categories[category].append(query_text)

    return 'Category {} has been updated with question "{}"'.format(category_to_update,query_text)

# An API that adds an entire category.
@app.route("/add_category")
def add_category():
    new_category = (request.args.get("new_category")).lower()
    message = ""
    if not new_category:
        abort(400, "/add_category requires string argument 'new_category'")
    found = False

    if new_category in all_categories.keys():
        return "Category {} already exists".format(new_category)

    all_categories[new_category] = []

    return "Category {} has been added. To add questions for it, go to /add_query_text".format(new_category)


app.run()



