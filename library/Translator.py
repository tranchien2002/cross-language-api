# -*- coding: utf-8 -*-
import pdb
import json
from googletrans import Translator
import goslate
import requests
def translate(text, src="vi", dest="en"):
    # translator = Translator()
    # text_translated = translator.translate(text, dest = dest)
    # return text_translated.text
    gs = goslate.Goslate()
    text_translated = gs.translate(text, dest)
    return text_translated

def translate_yandex(text, src="vi", dest="en"):
    text = text.replace('_', ' ')
    response = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20171210T144242Z.15fcdfc3fb78b303.0505cd3e5105cc8f96e30350651e309acd643605&lang=' +src + '-' + dest +'&text=' + text)
    print(response.content)
    response_json = json.loads(response.content)
    return (response_json['text'][0]).replace('"', '')