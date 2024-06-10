from flask import Flask, render_template, jsonify
import aitarot

global out_str

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_output')
def get_output():
    # 在这里编写生成输出的代码
    out_str = aitarot.generate_card()
    # 将输出以 JSON 格式返回给网页
    return jsonify(output=out_str)


if __name__ == '__main__':
  app.run(host='0.0.0.0',port=5000)
