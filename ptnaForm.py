import json
from ptna import *
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin


def ptnaPrompt(obj):
    """ ChatLogにピティナのレスポンスを表示する関数
        戻り値 'Ptnaオブジェクト名(応答オブジェクト名) : '
    """
    return ptna.name + "："


ptna = Ptna('ptna')                     # Ptnaオブジェクトを生成

app = Flask(__name__)                   # Flaskを利用できるようにappを定義
app.config['JSON_AS_ASCII'] = False     # 日本語の文字化けを防止
CORS(app, support_credentials=True)


@cross_origin(supports_credentials=True)
@app.route('/', methods=['POST'])       # ルートでPOSTデータの受け取りを許可
def ptnaResponse():
    """ フロントからJSONデータを受け取ってdataに格納し、
        dataが空かどうかで処理を分岐
    """
    data = request.get_json()
    if not data:
        response = ptnaPrompt(ptna) + "どうしたの？"
        return jsonify(response)
    else:
        response = ptnaPrompt(ptna) + ptna.dialogue(data)
        return jsonify(response)


# このPythonファイルが「python ファイル名.py というふうに実行されているかどうか」を判定するif文
if __name__ == '__main__':
    app.debug = True
    app.run()
