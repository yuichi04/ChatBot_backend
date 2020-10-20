import random
import re


class Responder:
    """ 応答クラスのスーパークラス
    """

    def __init__(self, name, dictionary):
        """ Responderオブジェクトの名前をnameに格納

            @param  name Responderオブジェクトの名前
        """
        self.name = name
        self.dictionary = dictionary

    def response(self, input, mood):
        """ オーバーライドを前提としたresponse()メソッド

            @param  input 入力された文字列
            戻り値   空の文字列
        """
        return ''

    def get_name(self):
        """ 応答オブジェクトの名前を返す
        """
        return self.name


class WhatResponder(Responder):
    """ オウム返しを行うためのサブクラス
    """

    def response(self, input, mood):
        """ 応答文字列を作って返す

            @param  input   入力された文字列
        """
        return '{}ってなに？'.format(input)


class RandomResponder(Responder):
    """ ランダムな応答を行うためのサブクラス
    """

    def response(self, input, mood):
        """ 応答文字列を作って返す

            @param  input 入力された文字列
            戻り値   リストからランダムに抽出した文字列
        """
        return (random.choice(self.dictionary.random))


class PatternResponder(Responder):
    """ パターンに反応するためのサブクラス
    """

    def response(self, input, mood):
        """ パターンにマッチした場合に応答文字列を作って返す

            @param input 入力された文字列
            @param mood 機嫌値
        """

        self.resp = None

        for ptn_item in self.dictionary.pattern:
            # match()でインプット文字列にパターンマッチを行う
            m = ptn_item.match(input)
            # マッチした場合は機嫌値moodを引数にしてchoice()を実行し、
            # 戻り値の応答文字列、またはNoneを取得
            if (m):
                self.resp = ptn_item.choice(mood)
            # choice()の戻り値がNoneであれば次のループに移行する
            if self.resp != None:
                # 応答例の中に%match%があれば、インプットされた文字列内の
                # パターンマッチした文字列に置き換え、
                # それ以外は応答文字列をそのまま返す
                return re.sub('%match%', m.group(), self.resp)
            # パターンマッチしない場合はランダム辞書から返す
        return random.choice(self.dictionary.random)
