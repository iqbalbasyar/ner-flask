
from flask import Flask,render_template,url_for,request, jsonify
import re
import pandas as pd
import spacy
from spacy import displacy
import en_core_web_md
import json 

nlp = en_core_web_md.load()


app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/process',methods=["POST"])
def process():
    if request.method == 'POST':
        choice = request.form['taskoption']
        rawtext = request.form['rawtext']
        doc = nlp(rawtext)
        d = []
        for ent in doc.ents:
            d.append((ent.label_, ent.text))
            df = pd.DataFrame(d, columns=('named entity', 'output'))
            ORG_named_entity = df.loc[df['named entity'] == 'ORG']['output']
            PERSON_named_entity = df.loc[df['named entity'] == 'PERSON']['output']
            GPE_named_entity = df.loc[df['named entity'] == 'GPE']['output']
            MONEY_named_entity = df.loc[df['named entity'] == 'MONEY']['output']
        if choice == 'organization':
            results = ORG_named_entity
            num_of_results = len(results)
        elif choice == 'person':
            results = PERSON_named_entity
            num_of_results = len(results)
        elif choice == 'geopolitical':
            results = GPE_named_entity
            num_of_results = len(results)
        elif choice == 'money':
            results = MONEY_named_entity
            num_of_results = len(results)
        elif choice == 'Select Category':
            results = pd.DataFrame() #create empty dataframe
            num_of_results = len(results)
		
    return render_template("index.html",results=results,num_of_results = num_of_results, original_text = rawtext)

@app.route('/test', methods=['POST'])
def foo():
    data = request.get_json() # load received json data
    text = data['text'] # extract 'text' element 
    doc = nlp(text) #
    d = [(ent.label_, ent.text) for ent in doc.ents]
    df = pd.DataFrame(d, columns=['category', 'value'])
    dictionary = {}
    for i in df['category'].unique():
        values = df.query(f"category == '{i}' ")['value'].to_list()
        dictionary[i] = values
    return json.dumps(dictionary)


@app.route('/endpoint_multi', methods=['GET', 'POST'])
def multi_method():
    if request.method == 'POST':
        return ("Nilai ini akan dikembalikan jika endpoint ini diakses dengan method POST")
    else : 
        return ("Nilai ini akan dikembalikan jika endpoint ini diakses dengan method GET")



if __name__ == '__main__':
    app.run(debug=True)
