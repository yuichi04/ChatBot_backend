import random
import re


class Dictionary:
    def __init__(self):
        self.random = []  # (1)
        # ランダム辞書ファイルオープン
        rfile = open('dics/random.txt', 'r', encoding='utf_8')
        # 各行を要素としてリストに格納
        r_lines = rfile.readlines()
        rfile.close()

        # 末尾の改行と空白文字を取り除いて
        # インスタンス変数（リスト）に格納
        self.random = []
        for line in r_lines:
            str = line.rstrip('\n')
            if (str != ''):
                self.random.append(str)

        # パターン辞書オープン
        pfile = open('dics/pattern.txt', 'r', encoding='utf_8')
        # 各行を要素としてリストに格納
        p_lines = pfile.readlines()
        pfile.close()
        # 末尾の改行と空白文字を取り除いて
        # インスタンス変数（リスト）に格納
        self.new_lines = []
        for line in p_lines:
            str = line.rstrip('\n')
            if (str != ''):
                self.new_lines.append(str)

        # リスト型のインスタンス変数を用意
        self.pattern = []

        # 辞書データの各行をタブで切り分ける
        # ptn 正規表現のパターン
        # prs 応答例
        # ParseItemオブジェクトを生成(引数はptn、prs）して
        # インスタンス変数pattern（リスト）に追加
        for line in self.new_lines:
            ptn, prs = line.split('\t')
            self.pattern.append(ParseItem(ptn, prs))


class ParseItem:
    SEPARATOR = '^((-?\d+)##)?(.*)$'

    def __init__(self, pattern, phrases):
        """ @param pattern  パターン
            @param phrases  応答例
        """
        # 辞書のパターンの部分にSEPARATORをパターンマッチさせる
        m = re.findall(ParseItem.SEPARATOR, pattern)
        # インスタンス変数modifyに0を代入
        self.modify = 0
        # マッチ結果の整数の部分が空でなければ値を再代入
        if m[0][1]:
            self.modify = (m[0][1])
        # インスタンス変数patternにマッチ結果のパターン部分を代入
        self.pattern = m[0][2]

        self.phrases = []   # 応答例を保持するインスタンス変数
        self.dic = {}       # インスタンス変数
        # 引数で渡された応答例を'|'で分割し、
        # 個々の要素に対してSEPARATORをパターンマッチさせる
        # self.phrases[ 'need'  : 応答例の整数部分
        #               'phrase': 応答例の文字列部分 ]
        for phrase in phrases.split('|'):
            # 応答例に対してパターンマッチを行う
            m = re.findall(ParseItem.SEPARATOR, phrase)
            # 'need'キーの値を整数部分m[0][1]にする
            # 'phrase'キーの値を応答文字列m[0][1]にする
            self.dic['need'] = 0
            if m[0][1]:
                self.dic['need'] = m[0][1]
            self.dic['phrase'] = m[0][2]
            # 作成した辞書をphrasesリストに追加
            self.phrases.append(self.dic.copy())

    def match(self, str):
        """self.pattern(各行ごとの正規表現)を
           インプット文字列にパターンマッチ
        """
        return re.search(self.pattern, str)

    def choice(self, mood):
        """インスタンス変数phrases(リスト）の
           要素('need''phrase'の辞書)
            'need':数値を

            @ptam mood
        """
        choices = []
        for p in self.phrases:
            # print(self.phrases)
            #print('p======', p['phrase'])
            # 'need'キーの数値とパラメーターmoodをsuitable()に渡し、
            # 結果がTrueであれば
            # choicesリストに'phrase'キーの文字列を追加
            # a=self.suitable(p['need'], mood)
            # print('応答例の整数部分',a)
            if (self.suitable(p['need'], mood)):
                choices.append(p['phrase'])
            # choicesリストが空であればNoneを返す
            if (len(choices) == 0):
                return None
            # choicesリストが空でなければランダムに
            # 応答文字列を選択して返す
        # print('最終choice==',choices)
        return random.choice(choices)

    def suitable(self, need, mood):
        """インスタンス変数phrases(リスト）の
           要素('need''phrase'の辞書)
            'need':数値を

            @ptam need 応答例の数値
            @ptam mood 現在値
        """
        # print('need=========',need)
        #print('need type==',type(need))
        # 必要機嫌値が0であればTrueを返す
        if (int(need) == 0):
            return True
        # 必要機嫌値がプラスの場合は機嫌値が必要機嫌値を超えているか判定
        elif (int(need) > 0):
            return (mood > int(need))
        # 応答例の数値がマイナスの場合は機嫌値が下回っているか判定
        else:
            return (mood < int(need))

#obj = Dictionary()
