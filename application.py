from flask import Flask, request, jsonify, render_template # type: ignore
import spacy # type: ignore
import json
from fuzzywuzzy import fuzz # type: ignore

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

# Load FAQs data from JSON file
with open('Ecommerce_FAQ_Chatbot_dataset.json') as f:
    faq_data = json.load(f)["questions"]

def get_response(user_input):
    doc = nlp(user_input)
    for token in doc:
        if token.text.lower() in ["hello", "hi", "hey"]:
            return "Hello! How can I help you today?"
        if token.text.lower() in ["goodbye", "bye"]:
            return "Goodbye! Have a great day!"
    
    max_similarity = 0
    best_match = None
    for entry in faq_data:
        question = entry["question"]
        similarity = fuzz.token_sort_ratio(user_input.lower(), question.lower())
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = entry
    
    if max_similarity > 50:  # Adjust the threshold as needed
        response = best_match["answer"]
    else:
        response = "I'm sorry, I don't understand that question. Can you please rephrase?"
    
    return response + " Need any help?"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get("message")
    response = get_response(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
