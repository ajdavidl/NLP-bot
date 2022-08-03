# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted
from datetime import datetime, date, timedelta

from textblob import TextBlob
import spacy
from wordfreq import word_frequency
import requests
from wiktionaryparser import WiktionaryParser
import wikipedia
import wikipediaapi
from transformers import pipeline

TextGenerationBloom = pipeline(
    "text-generation", model="bigscience/bloom-760m")


class translate(Action):
    def name(self) -> Text:
        return "action_translate"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = tracker.latest_message['text']
        list_words = message.split(' ')
        idiomaFrom = list_words[1]
        idiomaTo = list_words[2]
        query = ' '.join(list_words[3:])

        blob = TextBlob(query).translate(to=idiomaTo, from_lang=idiomaFrom)
        string = str(blob)

        dispatcher.utter_message(string)
        return []


class parse(Action):
    def name(self) -> Text:
        return "action_parse"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = tracker.latest_message['text']
        list_words = message.split(' ')
        idioma = list_words[1]
        sentence = ' '.join(list_words[2:])

        if idioma == 'pt':
            nlp = spacy.load("pt_core_news_sm")
        elif idioma == 'en':
            nlp = spacy.load("en_core_web_sm")
        elif idioma == 'es':
            nlp = spacy.load("es_core_news_sm")
        elif idioma == 'it':
            nlp = spacy.load("it_core_news_sm")
        elif idioma == 'fr':
            nlp = spacy.load("fr_core_news_sm")
        elif idioma == 'de':
            nlp = spacy.load("de_core_news_sm")
        else:
            dispatcher.utter_message("language not found.")
            return []

        doc = nlp(sentence)
        text = "Token → POS → Tag → Dep\n"
        for token in doc:
            text += token.text + ' → ' + token.pos_ + \
                ' → ' + token.tag_ + ' → ' + token.dep_ + '\n'

        dispatcher.utter_message(text)
        return []


class wordFreq(Action):
    def name(self) -> Text:
        return "action_wordFreq"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = tracker.latest_message['text']
        list_words = message.split(' ')
        if len(list_words) < 3:
            dispatcher.utter_message("Sorry, imcomplete query.")
            return []
        idioma = list_words[1]
        word = list_words[2]
        freq = word_frequency(word=word, lang=idioma)
        dispatcher.utter_message(str(freq))
        return []


class conceptnet(Action):
    def name(self) -> Text:
        return "action_conceptnet"

    def conceptnetQuery(self, lang, word, num=20):
        url = 'http://api.conceptnet.io/c/' + lang + \
            '/'+word+'?offset=0&limit='+str(num)

        obj = requests.get(url).json()
        length = len(obj['edges'])

        text = 'Concepts related to ' + word + '          '
        for i in range(length):
            try:
                edge = str(i+1) + ") " + obj['edges'][i]['start']['label'] + \
                    " (" + obj['edges'][i]['start']['language'] + ") " + \
                    obj['edges'][i]['rel']['label'] + " " + \
                    obj['edges'][i]['end']['label'] + \
                    " (" + obj['edges'][i]['end']['language'] + ')\n '
                text += edge
            except Exception as e:
                print("Oops!", e.__class__, "occurred.")
                continue
        return text

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = tracker.latest_message['text']
        list_words = message.split(' ')
        idioma = list_words[1]
        word = list_words[2]
        if len(list_words) == 4:
            number = list_words[3]
        else:
            number = 20
        text = self.conceptnetQuery(idioma, word, number)

        dispatcher.utter_message(text)
        return []


class wiktionary(Action):
    def name(self) -> Text:
        return "action_definition"

    def wiktionary(self, lang, query):
        if lang == 'pt':
            lang = 'portuguese'
        elif lang == 'en':
            lang = 'english'
        elif lang == 'es':
            lang = 'spanish'
        elif lang == 'it':
            lang = 'italian'
        elif lang == 'fr':
            lang = 'french'
        elif lang == 'de':
            lang = 'german'
        else:
            lang = 'english'
        parser = WiktionaryParser()
        parser.set_default_language(lang)
        try:
            data = parser.fetch(query)
        except Exception as e:
            return "Sorry! Error in wiktionary package!!"
        if len(data) > 0:
            if 'definitions' in data[0].keys():
                if len(data[0]['definitions']) > 0:
                    definitions = data[0]['definitions'][0]['text']
                    text = "Definitions: "
                    for i in range(len(definitions)):
                        text += data[0]['definitions'][0]['text'][i]+'\n'
                    return text
                else:
                    return "No text inside definitions data from wiktionary."
            else:
                return "No definitions found in wiktionary data."
        else:
            return "Empty data from wiktionary."

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = tracker.latest_message['text']
        list_words = message.split(' ')
        idioma = list_words[1]
        query = list_words[2]
        text = self.wiktionary(idioma, query)
        dispatcher.utter_message(text)

        return []


class wikipedia_(Action):
    def name(self) -> Text:
        return "action_wikipedia"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        message = tracker.latest_message['text']
        list_words = message.split(' ')
        idioma = list_words[1]
        query = ' '.join(list_words[2:])

        wikipedia.set_lang(idioma)
        results = wikipedia.search(query)
        if len(results) == 0:
            dispatcher.utter_message("Page not found!")
            return []
        wiki_wiki = wikipediaapi.Wikipedia(idioma)
        page = wiki_wiki.page(results[0])
        if 'may refer to' in page.summary:
            page = wiki_wiki.page(results[1])
        dispatcher.utter_message(page.summary)
        return []


class text_generation_bloom(Action):
    def name(self) -> Text:
        return "action_text_generation_bloom"

    def generate_text(self, textSeed, textSize=80):
        result = TextGenerationBloom(textSeed, max_length=textSize,
                                     num_return_sequences=1)
        return(result[0]['generated_text'])

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        message = tracker.latest_message['text']
        list_words = message.split(' ')
        text = ' '.join(list_words[1:])
        textOutput = self.generate_text(text)
        dispatcher.utter_message(textOutput)
        return []
