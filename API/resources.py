from flask import session, jsonify
from flask_restful import Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import json
import re

db = SQLAlchemy()
class AnalyzeText(Resource):
    def post(self):
        data = text_parser.parse_args()
        pathname = data['pathname']
        sentence_arr = []
        text_file =  open(pathname)
        sentences = split_into_sentences(text_file)
        sentence_arr = []
        for sentence in sentences:
            sentence_dict = {}
            sentence_dict["sentence"] = sentence
            sentence_dict["color"] = color_pick(len(sentence))
            sentence_arr.append(sentence_dict)
        return sentence_arr

def color_pick(length):
    if(len <= 1):
        return "white"
    elif(len <= 4):
        return "red"
    elif(len <= 8):
        return "orange"
    elif(len <= 12):
        return "yellow"
    elif(len <= 20):
        return "green"
    elif(len <= 28):
        return "teal"
    elif(len <= 32):
        return "blue"
    elif(len > 32):
        return "purple"

#Thanks to user D Greenburg who posted this sentence splitting code on Stack Overflow
#Question: https://stackoverflow.com/questions/4576077/python-split-text-on-sentences
#User: https://stackoverflow.com/users/5133085/d-greenberg
#Will eventually switch this over to a library call, but wanted to get it working for now
def split_into_sentences(text):
    caps = "([A-Z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov)"
    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = re.sub(prefixes, "\\1<prd>", text)
    text = re.sub(websites, "<prd>\\1", text)
    if "Ph.D" in text: text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    text = re.sub("\s" + caps + "[.] ", " \\1<prd> ", text)
    text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
    text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
    text = re.sub(caps + "[.]" + caps + "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
    text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
    text = re.sub(" " + caps + "[.]", " \\1<prd>", text)
    if "”" in text: text = text.replace(".”", "”.")
    if "\"" in text: text = text.replace(".\"", "\".")
    if "!" in text: text = text.replace("!\"", "\"!")
    if "?" in text: text = text.replace("?\"", "\"?")
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences