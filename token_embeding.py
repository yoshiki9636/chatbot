import sys
import torch
from transformers import BertJapaneseTokenizer, BertForMaskedLM
from transformers import BertJapaneseTokenizer, BertModel
from janome.tokenizer import Tokenizer
import numpy as np
import re

class tokenEmbeding():

    # embedingで使いたくないワードを登録
    useless_words = ['の','問題','様','さん','なに','何','匹','頭']
    # Bertのtokenizerを起動
    tokenizer = BertJapaneseTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking')
    model_bert = BertModel.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking', output_hidden_states=True)
    model_bert.eval()
    # janomeのtokenizerを起動
    t = Tokenizer()

    def __init__(self):
        return

    # embedingに邪魔なのでhttp以下を削除
    def remove_http(self,textlist):
        tlist = []
        for i in textlist:
            tlist.append(re.sub('http\S+', ' ',i))
        return tlist
    
    # embedingに邪魔なので名詞句のみを抜き出し、ついでに使わない語句も消去
    def get_nouns(self,text):
        terms = [token.surface for token in self.t.tokenize(text) if token.part_of_speech.startswith('名詞')]
        terms2 = [ token for token in terms if not (token in self.useless_words) ]
        return terms2
    
    # 各文章のembedingの計算
    def calc_embedding(self,text):
        btokens = self.get_nouns(text)
        ids = self.tokenizer.convert_tokens_to_ids(["[CLS]"] + btokens[:126] + ["[SEP]"])
        tokens_tensor = torch.tensor(ids).reshape(1, -1)
        with torch.no_grad():
            output = self.model_bert(tokens_tensor)
        return output[1].numpy()

