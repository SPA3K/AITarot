import os
import random
from openai import OpenAI

# os.environ["OPENAI_API_KEY"] = "sk-proj-uKz845rWEhZjPjFs55WUT3BlbkFJsX1pkp7s9LL9Uz00qj44"   # kehan key
os.environ["OPENAI_API_KEY"] = "sk-VbBK9ARkkhKG25Io2783Bd26Ed404788Ad6cC25559E7C005"          # no proxy key
os.environ["OPENAI_BASE_URL"] = "https://api.xiaoai.plus/v1"

client = OpenAI()

print("Start Running")

card_set = ["Fool", "Magician", "High Priestess", "Empress", "Emperor", "Hierophant", "Lovers", "Chariot", "Chariot", "Chariot", "Hermit", "Wheel of Fortune", "Justice", "Hanged Man", "Death", "Temperance", "Devil", "Tower", "Star", "Moon", "Sun", "Judgment", "World", 
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

card_number = 8
numbers = list(range(len(card_set) - 1)) 
random_card_num = random.sample(numbers, card_number)  
input_str = ""
for i in range(card_number):
    input_str += "Card_" + str(i) + ":" + card_set[random_card_num[i]] + ", status: " + card_status[random.randint(0, 1)] + "; "

completion = client.chat.completions.create(
  model="gpt-4",
  messages=[
    {"role": "system", "content": "You're a tarot card prognosticator, and you need to give a 500-word or so prediction of the future through my next hand input, and the consulter usually comes with frustration, and your answers need to sell anxiety. Translate to Chinese."},
    {"role": "user", "content": input_str}
  ]
)

print(completion.choices[0].message)
input("Press any key to exit.")
