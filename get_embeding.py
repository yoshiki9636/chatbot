import sys
import faiss
import numpy as np
import pandas as pd
import token_embeding

filename = sys.argv[1]
textlist = []
te = token_embeding.tokenEmbeding()

# textlist作成
df = pd.read_csv(filename, header=None)
for index, i in df.iterrows():
    txt = i[0] + " " + i[1]
    textlist.append(txt)
print(len(textlist))
tlist = te.remove_http(textlist)

np.save('./npy/textlist.npy',textlist,fix_imports=False)

# embedingのindex作成
tmp_embeds = list(map(te.calc_embedding, tlist))
embeddings = []
for embed in tmp_embeds:
    embeddings.append(embed[0])

index = faiss.IndexFlatIP(embeddings[0].shape[0])
index.add(np.array(embeddings))

np.save('./npy/index.npy',index,fix_imports=False)
