#!/bin/bash

rm ./csv/all.csv
touch ./csv/all.csv
for i in ./json/*.json; do
	python3 parser_action_only.py ${i} >> ./csv/all.csv
done

python3 get_embeding.py ./csv/all.csv

