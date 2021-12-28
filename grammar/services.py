import requests
import json
import string

def spell_sentence(text):

    api_key = "574641672a0a483cb161517695d024b6"
    #text = "needir bu sevg, dedigin?"
    endpoint = "https://api.bing.microsoft.com/v7.0/SpellCheck"

    # Convert sentence to word list
    word_list = text.split(" ")


    # Separate punctuation if exists. Bing Spell Check API uses tokenized words.
    # If you post "sevg,", it will give you "sevgi" without comma.

    # Prepare data, params and headers
    data = {'text': text}

    params = {
        'mode': 'spell' 
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Ocp-Apim-Subscription-Key': api_key
    }

    response = requests.post(endpoint, headers=headers, params=params, data=data)

    json_response = response.json()

    # Convert json to array
    changedTokens = json_response['flaggedTokens']
    new_sentence = []
    for word in word_list:
        word = word.translate(str.maketrans('', '', string.punctuation))
        for changed_elem in changedTokens:
            if word == changed_elem['token']:
                print("Previous word", word)
                word = changed_elem['suggestions'][0]['suggestion']
                print("Changed word:", word)
        new_sentence.append(word)

        # TODO: Below code will be used to punctuations if original word has
        #       after replacing the suggested word from Bing API
        #if any(w in string.punctuation for w in word):
            #print("Punc:", word)
    print("New Sentence:", ' '.join(new_sentence))

    return ' '.join(new_sentence)
