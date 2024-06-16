from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os
import re
import random

# os.environ["OPENAI_API_KEY"] = "sk-proj-uKz845rWEhZjPjFs55WUT3BlbkFJsX1pkp7s9LL9Uz00qj44"   # kehan key
os.environ["OPENAI_API_KEY"] = "sk-VbBK9ARkkhKG25Io2783Bd26Ed404788Ad6cC25559E7C005"          # no proxy key
os.environ["OPENAI_BASE_URL"] = "https://api.xiaoai.plus/v1"
os.environ["BACKEND_URL"] = "https://aitarot.azurewebsites.net/"

load_dotenv()
app = Flask(__name__)
client = OpenAI()
CORS(app)
history = []
draft_story_save = ""
puzzles = ""
final_story = ""

card_set = ["Fool", "Magician", "High Priestess", "Empress", "Emperor", "Hierophant", "Lovers", "Chariot", "Hermit", "Wheel of Fortune", "Justice", "Hanged Man", "Death", "Temperance", "Devil", "Tower", "Star", "Moon", "Sun", "Judgment", "World", 
            "Ace of Wands", "Two of Wands", "Three of Wands", "Four of Wands", "Five of Wands", "Six of Wands", "Seven of Wands", "Eight of Wands", "Nine of Wands", "Ten of Wands", 
            "Page of Wands", "Queen of Wands", "King of Wands", 
            "Ace of Cups", "Two of Cups", "Three of Cups", "Four of Cups", "Five of Cups", "Six of Cups", "Seven of Cups", "Eight of Cups", "Nine of Cups", "Ten of Cups", 
            "Page of Cups", "Queen of Cups", "King of Cups", 
            "Ace of Swords", "Two of Swords", "Three of Swords", "Four of Swords", "Five of Swords", "Six of Swords", "Seven of Swords", "Eight of Swords", "Nine of Swords", "Ten of Swords", 
            "Page of Swords", "Queen of Swords", "King of Swords", 
            "Ace of Pentacles", "Two of Pentacles", "Three of Pentacles", "Four of Pentacles", "Five of Pentacles", "Six of Pentacles", "Seven of Pentacles", "Eight of Pentacles", "Nine of Pentacles", "Ten of Pentacles", 
            "Page of Pentacles", "Queen of Pentacles", "King of Pentacles"
            ]
card_status = ["positive", "negative"]

def generate_draft_story_message(aspect_data, input_str):
    history = []
    messages = [
        {"role": "system", "content": "You're a tarot card prognosticator, and you need to give a 500-word or so prediction of the future through my next hand input, and the consulter usually comes with frustration, and your answers need to sell anxiety. Translate all to Chinese."},
        {"role": "user", "content": f"In the aspect of {aspect_data}, cards are {input_str}"}
    ]
    history.append(messages[0])
    return messages, history


def generate_story_options(request):
    messages = [
        {"role": "user", "content": request}
    ]
    return messages

@app.route('/')
def index():
    backend_url = os.getenv('BACKEND_URL')
    return render_template('index.html', backend_url=backend_url)
 
@app.route('/generate_draft_story', methods=['POST'])
def draft_story():
    global draft_story_save, history
    data = request.get_json()
    print(data)
    aspect_data = data.get('section1')
    if not data:
        return jsonify({'error': 'No query provided'}), 400
    
    # select random tarot card
    card_number = 8
    numbers = list(range(len(card_set) - 1)) 
    random_card_num = random.sample(numbers, card_number)  
    input_str = ""
    for i in range(card_number):
        input_str += "Card_" + str(i) + ":" + card_set[random_card_num[i]] + ", status: " + card_status[random.randint(0, 1)] + "; "

    # predict the story
    try:
        messages, history = generate_draft_story_message(aspect_data, input_str)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        answer = response.choices[0].message.content
        print(response.choices[0].message)
        draft_story_save = answer

        output = f"Your cards is {input_str}\n{answer}"
        return jsonify({'answer': output})
    except Exception as e:
        print(f"General error: {e}")
        return jsonify({'error': f"General error: {e}"}), 500

    
@app.route('/get_options', methods=['GET'])
def get_options():
    query_type = request.args.get('type')
    if not query_type:
        return jsonify({'error': 'No query type provided'}), 400
    prompts = {
        "aspect": "Provide 6 different tarot predict aspects in an array format, for example, [\"Romanticships\", \"Studying\", \"Business\", \"Fortune\", \"Health\", \"Family\"]",
    }
    prompt = prompts.get(query_type)
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=generate_story_options(prompt)
        )
        answer = response.choices[0].message.content
        print(response.choices[0].message.content)
        json_pattern = re.findall(r'\[([^\[\]]+)\]', answer)
        print(json_pattern[0])
        options_list = [opt.strip('" ') for opt in json_pattern[0].split(',')] 
        print(options_list)
        return jsonify({'options': options_list})
    except Exception as e:
        print(f"General error: {e}")
        return jsonify({'error': f"General error: {e}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
