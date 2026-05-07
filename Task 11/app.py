from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

responses = {
    "hours": {
        "keywords": ["hours", "open", "timing", "when", "time"],
        "answer": "We're open Monday-Friday 8am-6pm, Saturday 10am-4pm, Closed on Sundays"
    },
    "location": {
        "keywords": ["location", "address", "where", "find"],
        "answer": "We're located at 123 Main Street, Building A, 2nd Floor"
    },
    "book_search": {
        "keywords": ["search", "find book", "look for", "book"],
        "answer": "Search books using our online catalog at our desk, or tell me the title/author"
    },
    "membership": {
        "keywords": ["membership", "register", "join", "card"],
        "answer": "Get a free membership at the front desk with your ID. It's valid for 1 year"
    },
    "due_date": {
        "keywords": ["due", "when due", "return"],
        "answer": "Most books are due in 2 weeks. Provide your membership ID at the desk to check"
    },
    "fine": {
        "keywords": ["fine", "late", "penalty", "charge"],
        "answer": "Late fine is Rs.5 per day per book. Extend books online before due date"
    },
    "quiet_zone": {
        "keywords": ["quiet", "silent", "study", "noise"],
        "answer": "Yes, we have a quiet zone on 2nd floor. No phones or loud talking allowed"
    },
    "wifi": {
        "keywords": ["wifi", "internet", "password"],
        "answer": "Free WiFi available. Password: Library123"
    },
    "contact": {
        "keywords": ["contact", "phone", "call", "email"],
        "answer": "Call us at 123-456-7890 or email library@university.edu"
    },
    "printing": {
        "keywords": ["print", "copy", "scan", "printer"],
        "answer": "We have printing and scanning facilities on the 1st floor. B&W is Rs.5/page, Color is Rs.20/page."
    },
    "food": {
        "keywords": ["food", "eat", "drink", "coffee", "water", "cafe"],
        "answer": "Only bottled water is allowed in the study areas. We have a cafeteria on the ground floor for eating/drinking."
    },
    "lost_found": {
        "keywords": ["lost", "found", "missing", "forgot"],
        "answer": "Our lost and found is at the main security desk near the entrance. Please ask the guard."
    },
    "events": {
        "keywords": ["event", "workshop", "seminar"],
        "answer": "We host weekly workshops. Check our notice board or ask the front desk for this week's schedule."
    },
    "restroom": {
        "keywords": ["restroom", "toilet", "washroom", "bathroom"],
        "answer": "Restrooms are located on the left wing of every floor, directly opposite the elevators."
    },
    "help": {
        "keywords": ["help", "assist", "guidance", "how", "options"],
        "answer": "I can help with: hours, location, book search, membership, due dates, fines, quiet zones, WiFi, contact, printing, food rules, lost & found, and restrooms."
    }
}

def get_response(user_input):
    user_input = user_input.lower()
    
    for key, data in responses.items():
        for keyword in data["keywords"]:
            if keyword in user_input:
                return data["answer"]
    
    return "I'm not sure about that. Try asking about: hours, location, book search, membership, due dates, or contact us."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'response': 'Please say something'})
    
    bot_response = get_response(user_message)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
