import markovify
import spacy

import random
import time
import re

# This is an attempt to generate interesting titles with the markovify algorithm.
# No matter the params the titles were just too close to the original ones.
# Also, I could only realistically generate about 5k "decent" ones.

nlp = spacy.load("en_core_web_sm")

class POSifiedText(markovify.NewlineText):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

def get_model(state_size, nlp_text = False):
    # Read in original data.
    text = ""
    with open("titles.txt") as f:
        text = f.read()
    # Shuffle it around?  Not sure if that changes the model.
    if nlp_text: 
        model = POSifiedText(text, state_size = state_size)
    else:
        model = markovify.NewlineText(text, state_size = state_size)
    return model

# Removing duplicate entries.
def remove_duplicates(old_file, new_file, filter_out = True):
    data = {}
    with open(old_file, "r") as f:
        for line in f.readlines():
            data[line] = True
    with open(new_file, "w+") as f:
        for key in data.keys():
            f.write(key)

def generate_messages_for_website(total_messages, state_size = 5):
    model = get_model(state_size)
    message_count = 0
    results_file = open("results_markovify.txt", "w+")
    while message_count < total_messages:
        message = model.make_sentence()
        if (message == None):
            continue
        elif message_count % 1_000 == 0:
            print("Processed: " + str(message_count) + " of " + str(total_messages))
        results_file.write(message + '\n')
        message_count += 1
    results_file.close()


if __name__ == "__main__":
    generate_messages_for_website(100_000, state_size = 2)
    remove_duplicates("results_markovify.txt", "processed-results.txt")