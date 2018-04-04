from flask import abort, Flask, request
import json
import spacy
from spacy.tokens import Doc

app = Flask(__name__)

nlp = spacy.load('en')

categories = ['Dorm rules', 'Food', 'Transportation', 'Financial Aid', 'Logistics']

# Dorm rules
set1 = ['Are pets allowed in the dorms?', 'Are power strips allowed?', 'What are the policies on space heaters in dorms?']

# Food
set2 = ['How many cafeterias are there on campus?', 'How expensive are the meal plans?', 'Are there kosher dining options?']

# Transportation
set3 = ['Can I bring my car to campus?', 'How much is a bus pass?', 'Do the buses run on the weekends?']

# Financial Aid
set4 = ['What is FAFSA?', 'How do I apply for a scholarship?', 'How much does tuition cost?']

# Logistics
set5 = ['When is move-in day?', 'Is there an orientation week for freshmen?', 'What day do classes start?']

combined = (set1, set2, set3, set4, set5)

def doc(string):
	output = nlp(string)
	return output

def checkSimilarity(string1, string2):
	doc1 = doc(string1)
	doc2 = doc(string2)
	return doc1.similarity(doc2)

def categorizeSentence(string):
	i = 0
	for each_set in combined:
		for sentence in each_set:
			if checkSimilarity(string, sentence) > 0.70:
				# print(checkSimilarity(string, sentence))
				return ["Category "+str(i+1)+": "+categories[i], "Closest question: "+sentence]
		i += 1
	if i == 5:
		return 'Sentence was not above 70 percent similar with any category'
	return null

@app.route("/hello/")
def hello():
    name = request.args.get("name")
    if not name:
        abort(400, "/hello requires string argument 'name'")

    return json.dumps(["This is a list of greetings", "Hello " + name, "How goes it?"])

@app.route("/")
def greeting():
	message = "Hello, welcome to my little API. Use via query string parameters."
	return message

# An API that lists available categories: their index/ID, a sample question
@app.route("/a1")
def a1():
	mydict = {}
	i = 0
	for each_set in combined:
		for sentence in each_set:
			category_and_index = "Category " + str(i+1) + ": " + categories[i]
			sample_question = each_set[0]
			mydict.update({category_and_index:sample_question})
		i += 1
	return json.dumps(mydict)

# An API that takes in a query text and returns the index/ID of the category it matched to and the closest question that made it match.
@app.route("/a2")
def a2():
	query = request.args.get("query")
	if not query:
		abort(400, "/hello requires string argument 'query'")

	return json.dumps(categorizeSentence(query))

app.run()



