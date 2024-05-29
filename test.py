import os
from openai import OpenAI

# os.environ["OPENAI_API_KEY"] = "sk-proj-uKz845rWEhZjPjFs55WUT3BlbkFJsX1pkp7s9LL9Uz00qj44"
os.environ["OPENAI_API_KEY"] = "sk-VbBK9ARkkhKG25Io2783Bd26Ed404788Ad6cC25559E7C005"
os.environ["OPENAI_BASE_URL"] = "https://api.xiaoai.plus/v1"

client = OpenAI()
# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
# if you saved the key under a different environment variable name, you can do something like:
# client = OpenAI(
#   api_key=os.environ.get("CUSTOM_ENV_NAME"),
# )

completion = client.chat.completions.create(
  model="gpt-4",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)

