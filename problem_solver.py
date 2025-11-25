import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
import json

class ProblemSolver:
    def __init__(self):
        with open('data.json', 'r', encoding='utf-8') as file:
            json_data = json.load(file)

        data = []
        for intent, directions in json_data.items():
            for direction, phrases in directions.items():
                for phrase in phrases:
                    data.append((phrase['phrase'], intent))

        messages, labels = zip(*data)

        X_train, X_test, y_train, y_test = train_test_split(messages, labels, test_size=0.2, random_state=42)
        self.model = make_pipeline(CountVectorizer(), MultinomialNB())

        self.model.fit(X_train, y_train)
        accuracy = self.model.score(X_test, y_test)
        print(accuracy)

    def classify_message(self, message):
        predictions = self.model.predict([message])
        predicted_intent = predictions[0]
        entity = message.split()[-1]
        print(f"Сообщение: '{message}' -> Намерение: '{predicted_intent}', Сущность: '{entity}'")
        return [str(predicted_intent), entity]
    
    def ask_message(self, data):
        if data[0] == 'greeting':
            return "Привет!"
        if data[0] == 'fight':
            return "Ты пронзаешь соперника мечом"
        if data[0] == 'movement':
            return "Ты переходишь на одну клетку" + data[1]
        



