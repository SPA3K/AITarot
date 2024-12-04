from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os
import re
import random

os.environ["OPENAI_API_KEY"] = "***"
os.environ["BACKEND_URL"] = "***"

load_dotenv()
app = Flask(__name__)
client = OpenAI()
CORS(app)
history = []
draft_story_save = ""
puzzles = ""
final_story = ""

card_set = ["THE_FOOL", "THE_MAGICIAN", "THE_HIGH_PRIESTESS", "THE_EMPRESS", "THE_EMPEROR", "THE_HIEROPHANT", "THE_LOVERS", "THE_CHARIOT", "STRENGTH", "THE_HERMIT", "WHEEL_OF_FORTUNE", "JUSTICE", "THE_HANGED_MAN", "DEATH", "TEMPERANCE", "THE_DEVIL", "THE_TOWER", "THE_STAR", "THE_MOON", "THE_SUN", "JUDGEMENT", "THE_WORLD", 
            "ACE_OF_WANDS", "TWO_OF_WANDS", "THREE_OF_WANDS", "FOUR_OF_WANDS", "FIVE_OF_WANDS", "SIX_OF_WANDS", "SEVEN_OF_WANDS", "EIGHT_OF_WANDS", "NINE_OF_WANDS", "TEN_OF_WANDS", 
            "PAGE_OF_WANDS", "KNIGHT_OF_WANDS", "QUEEN_OF_WANDS", "KING_OF_WANDS", 
            "ACE_OF_CUPS", "TWO_OF_CUPS", "THREE_OF_CUPS", "FOUR_OF_CUPS", "FIVE_OF_CUPS", "SIX_OF_CUPS", "SEVEN_OF_CUPS", "EIGHT_OF_CUPS", "NINE_OF_CUPS", "TEN_OF_CUPS", 
            "PAGE_OF_CUPS", "KNIGHT_OF_CUPS", "QUEEN_OF_CUPS", "KING_OF_CUPS", 
            "ACE_OF_SWORDS", "TWO_OF_SWORDS", "THREE_OF_SWORDS", "FOUR_OF_SWORDS", "FIVE_OF_SWORDS", "SIX_OF_SWORDS", "SEVEN_OF_SWORDS", "EIGHT_OF_SWORDS", "NINE_OF_SWORDS", "TEN_OF_SWORDS", 
            "PAGE_OF_SWORDS", "KNIGHT_OF_SWORDS", "QUEEN_OF_SWORDS", "KING_OF_SWORDS", 
            "ACE_OF_PENTACLES", "TWO_OF_PENTACLES", "THREE_OF_PENTACLES", "FOUR_OF_PENTACLES", "FIVE_OF_PENTACLES", "SIX_OF_PENTACLES", "SEVEN_OF_PENTACLES", "EIGHT_OF_PENTACLES", "NINE_OF_PENTACLES", "TEN_OF_PENTACLES", 
            "PAGE_OF_PENTACLES", "KNIGHT_OF_PENTACLES", "QUEEN_OF_PENTACLES", "KING_OF_PENTACLES", 
            ]
card_status = ["upright", "reversed"]

def generate_draft_story_message(aspect_data, input_str):
    history = []
    messages = [
        {"role": "system", "content": "You're a tarot card prognosticator, and you need to give a 300-word or so prediction of the future through my next hand input, and the consulter usually comes with frustration, and your answers need to sell anxiety."},
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
    cards=[]
    posis=[]
    for i in range(card_number):
        card = card_set[random_card_num[i]]
        posi = card_status[random.randint(0, 1)]
        cards.append(card)
        posis.append(posi)
        input_str += "Card_" + str(i) + ":" + card + ", status: " + posi + "; "
    print(cards)
    print(posis)

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

        output = {
            'cards': cards,
            'posis': posis,
            'answer': answer
        }
        return jsonify(output)
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


def generate_puzzle(story, history):
    messages = history.copy()
    messages.append({"role": "assistant", "content": f"tarot predict is above"})
    messages.append(
        {"role": "user", "content": f"Find five information user might ask according to the tarot predict. Return them in the following format without numerical numbering [\"sentence\",\"sentence\",\"sentence\",\"sentence\",\"sentence\"]"}
    )
    print(messages)
    history = messages.copy()
    return messages, history


@app.route('/get_puzzle_options', methods=['GET'])
def get_puzzle_options():
    global draft_story_save, history
    try:
        messages, history = generate_puzzle(draft_story_save, history)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        answer = response.choices[0].message.content
        print(response.choices[0].message.content)
        return jsonify({'options': answer})
    except Exception as e:
        print(f"General error: {e}")
        return jsonify({'error': f"General error: {e}"}), 500
    

def generate_final_story_prompt(reask, mbti, zodiac, draft_story_save, history):
    messages = history.copy()
    messages.append({"role": "assistant", "content": f"tarot predict is above"})
    messages.append(
        {"role": "user", "content": f"According to the mbti of tester is {mbti} and the zodiac {zodiac}, resolving this questiongs: {reask} in 200-words."}
    )
    print(messages)
    return messages


@app.route('/generate_final_story', methods=['POST'])
def generate_final_story():
    global draft_story_save, history
    finalData = request.get_json()
    reask = finalData['puzzles']
    selfConfig = finalData['selfAnswers']
    mbti = selfConfig.get('section1')
    zodiac = selfConfig.get('section2')
    print(finalData)
    # mbti = data.get('section1')
    # constellation = data.get('section2')
    try:
        messages = generate_final_story_prompt(reask, mbti, zodiac, draft_story_save, history)
        print(messages)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
        answer = response.choices[0].message.content
        print(response.choices[0].message.content)
        return jsonify({'story': answer})
    except Exception as e:
        print(f"General error: {e}")
        return jsonify({'error': f"General error: {e}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
