# Chatbot
Chatbot with ChatGP

# 1. Preparing data

You need to prepare data as csv/test.csv format, or you need to change get_embeding.py to get your text format.
After preparing data, do below command.

$ python3 ./get_embeding.py <yourcsvname>.csv 

After that, you will see 2 .npy files in npy/ directry.

# 2. Execution main script

You can run script as below after preparing data.

$ python3 app.py

After that, you will see web page with web browser access.

http://<your ip address>:5000

If you use wsl2 you can see the page just using 'localhost'

http://localhost:5000

Enjoy it!