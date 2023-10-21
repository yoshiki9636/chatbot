from flask import Flask, render_template, request
import os
import sys
import numpy as np
import openai
import token_embeding

openai.api_key = os.getenv("OPENAI_API_KEY")
te = token_embeding.tokenEmbeding()
index = np.load('./npy/index.npy',allow_pickle=True).tolist()
textlist = np.load('./npy/textlist.npy',allow_pickle=True).tolist()
prev_question = ""
prev_fact = ""
select_sentences = 4
print(len(textlist))

app = Flask(__name__)

# レスポンスを整形する関数
def format_response(response):
    # レスポンス内の各部分を適切な形式に変換
    response = response.replace("・", "\n・")
    # 改行をHTML形式に変換
    response = response.replace("\n", "<br>")
    return response

# ルートURLへのリクエストを処理する関数
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # フォームから質問を取得
        question = request.form['question']
        # 質問に対するレスポンスを生成
        response = generate_response(question)
        # レスポンスを含むページを表示
        return render_template('index.html', response=response)
    # フォームを表示
    return render_template('index.html')

# 質問に対するレスポンスを生成する関数
def generate_response(question):
    # 質問が含まれている文章を選択
    fact = get_fact_from_question(question)
    print("chk1")
    # 質問と文章から答を生成
    answer = fact_qa(fact, question)
    # レスポンスを整形
    formatted_response = format_response(answer)
    return formatted_response

# 質問が含まれている文章を選択
def get_fact_from_question(question):
    global prev_question
    global prev_fact

    toklist = te.get_nouns(question)
    question_embed = te.calc_embedding(question)
    D, I = index.search(question_embed, len(textlist))
    # 各名詞が含まれる文書の数を算,出
    cn, markcntr, mark, words = get_candidate_num(toklist,textlist)

    if markcntr > 1:
        # 名詞2つのコンビネーションを探索
        flg, cn2, word1, word2 = get_2conbination(toklist,textlist,markcntr,mark)
        print(word1)
        print(word2)
        # 文書数が最小の名詞を選択
        if flg == 1:
            cntr, idx = get_word_num(word1,word2,cn2,textlist)
            # 最小の文書数が3以下であればその文書を選択
            if cntr <= select_sentences:
                fact = get_text_by_words(textlist,word1[idx],word2[idx])
            # 最小の文書数が3より大きい場合はコサイン類似度で選択
            else:
                fact = get_text_by_cos(textlist,word1[idx],word2[idx],I)
        else:
            # 文書数が最小の名詞を選択
            cntr, idx = get_word_num(words,[],cn,textlist)
            # 空の質問には前回の質問を返す
            print("cntr3 ",cntr)
            if cntr <= select_sentences:
                fact = get_text_by_words(textlist,words[idx],"")
            # 最小の文書数が3より大きい場合はコサイン類似度で選択
            else:
                fact = get_text_by_cos(textlist,words[idx],"",I)
    else:
        # 文書数が最小の名詞を選択
        cntr, idx = get_word_num(words,[],cn,textlist)
        # 空の質問には前回の質問を返す
        print("cntr2 ",cntr)
        if cntr == len(textlist):
            question = prev_question
            fact = prev_fact
        # 最小の文書数が3以下であればその文書を選択
        elif cntr <= select_sentences:
            fact = get_text_by_words(textlist,words[idx],"")

        # 最小の文書数が3より大きい場合はコサイン類似度で選択
        else:
            fact = get_text_by_cos(textlist,words[idx],"",I)

    # 空の質問の場合の前情報を保存
    prev_question = question
    prev_fact = fact

    return fact
    
# 各名詞が含まれる文書の数を算,出
def get_candidate_num(toklist,textlist):
    cntr = 0
    words = []
    mark = {}
    markcntr = 0
    cn ={} 
    for j in range(len(toklist)):
        for i in range(len(textlist)):
            if (toklist[j] in np.array(textlist)[i]):
                cntr += 1
                print("s ",toklist[j]," ",i, " ",markcntr)
        if (cntr > 0):
            words.append(toklist[j])
            cn[toklist[j]] = cntr
            if (cntr < 15):
                mark[toklist[j]] = 1
                markcntr += 1
            else:
                mark[toklist[j]] = 0
            cntr = 0
        else:
            mark[toklist[j]] = 0
    return cn, markcntr, mark, words

# 名詞2つのコンビネーションを探索
def get_2conbination(toklist,textlist,markcntr,mark):
    word1 = []
    word2 = []
    cntr = 0
    cn ={} 
    flg = 0
    for k in range(len(toklist)):
        for j in range(k+1,len(toklist)):
            if (mark[toklist[k]]==1)&(mark[toklist[j]]==1):
                for i in range(len(textlist)):
                    if (toklist[j] in np.array(textlist)[i])and(toklist[k] in np.array(textlist)[i]):
                        cntr += 1
                        print("s2 ",toklist[k]," ",toklist[j]," ",i)

                if (cntr > 0):
                    word1.append(toklist[k])
                    word2.append(toklist[j])
                    cn[toklist[k]+toklist[j]] = cntr
                    cntr = 0
                    flg = 1
    return flg, cn, word1, word2

# 文書数が最小の名詞を選択
def get_word_num(word1,word2,cn,textlist):
    cntr = len(textlist)
    idx = -1
    for i in range(len(word1)):
        if len(word2) == 0:
            print("c1 ",word1[i],"  ",cn[word1[i]]," ",i)
            if cn[word1[i]] < cntr:
                cntr = cn[word1[i]]
                idx = i
        else:
            print("c2 ",word1[i]," ",word2[i]," ",cn[word1[i]+word2[i]]," ",i)
            if cn[word1[i]+word2[i]] < cntr:
                cntr = cn[word1[i]+word2[i]]
                idx = i
    return cntr, idx

# 単語が含まれる文書を選択
def get_text_by_words(textlist,word_1,word_2):
    fact = ""
    for i in range(len(textlist)):
        if word_2 == "":
            if (word_1 in np.array(textlist)[i]):
                print("f1 ",i)
                fact += np.array(textlist)[i]
        else:
            if (word_1 in np.array(textlist)[i])and(word_2 in np.array(textlist)[i]):
                print("f2 ",word_1," ",word_2, " ",i)
                fact += np.array(textlist)[i]
    return fact

# コサイン類似度で選択
def get_text_by_cos(textlist,word_1,word_2,I):
    cntr = 0
    fact = ""
    for i in I[0]:
        if word_2 == "":
            if (word_1 in textlist[i]):
                fact += np.array(textlist)[i]
                print("e1 ",i)
                cntr += 1
                if (cntr > 3):
                    break
        else:
            if (word_1 in np.array(textlist)[i])and(word_2 in np.array(textlist)[i]):
                fact += np.array(textlist)[i]
                print("e2 ",i)
                cntr += 1
                if (cntr > select_sentences):
                    break
    return fact

# openaiへの問い合わせ
def completion(new_message_text:str, settings_text:str = '', past_messages:list = []):
    if len(past_messages) == 0 and len(settings_text) != 0:
        system = {"role": "system", "content": settings_text}
        past_messages.append(system)
    new_message = {"role": "user", "content": new_message_text}
    past_messages.append(new_message)

    result = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=past_messages,
        max_tokens=512
    )
    response_message = {"role": "assistant", "content": result.choices[0].message.content}
    past_messages.append(response_message)
    response_message_text = result.choices[0].message.content
    return response_message_text, past_messages

# prompt作成
def fact_qa(fact, question):
    system_text = "あなたは参考文章をもとに質問に回答するシステムです。参考文章をもとに、段階的に考えて論理的に回答してください。"
    question_prompt = f"""## 参考文章

{fact}

## 質問

{question}"""
    answer, _ = completion(question_prompt, system_text, [])
    return answer

# メイン関数
if __name__ == '__main__':
    app.run(debug=True)

