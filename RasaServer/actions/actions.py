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

        blob = TextBlob(query).translate(to=idiomaTo, from_lang = idiomaFrom)
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

        if idioma=='pt':
            nlp = spacy.load("pt_core_news_sm")
        elif idioma=='en':
            nlp = spacy.load("en_core_web_sm")
        elif idioma=='es':
            nlp = spacy.load("es_core_news_sm")
        elif idioma=='it':
            nlp = spacy.load("it_core_news_sm")
        elif idioma=='fr':
            nlp = spacy.load("fr_core_news_sm")
        elif idioma=='de':
            nlp = spacy.load("de_core_news_sm")
        else:
            dispatcher.utter_message("language not found.")
            return []
        
        doc = nlp(sentence)
        text = "Token → POS → Tag → Dep\n"
        for token in doc:
            text += token.text + ' → ' + token.pos_ + ' → ' + token.tag_ + ' → ' + token.dep_ + '\n'
        
        dispatcher.utter_message(text)
        return []