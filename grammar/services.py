import requests
import json
import string

def spell_sentence(text):

    api_key = "6b30752ba3fe4c36b5ca90216a8c0a81"
    #text = "needir bu sevg, dedigin?"
    endpoint = "https://api.bing.microsoft.com/v7.0/SpellCheck"

    # Convert sentence to word list
    word_list = text.split(" ")


    # Separate punctuation if exists. Bing Spell Check API uses tokenized words.
    # If you post "sevg,", it will give you "sevgi" without comma.

    # Prepare data, params and headers
    data = {'text': text}

    params = {
        'mode': 'spell',
        'text': text,
        'mkt': 'tr-TR' 
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Ocp-Apim-Subscription-Key': api_key
    }

    response = requests.get(endpoint, headers=headers, params=params)

    json_response = response.json()
    print("Main function")
    # Convert json to array
    changedTokens = json_response['flaggedTokens']
    print("Changed tokens:", changedTokens)
    new_sentence = []
    
    for word in word_list:
        punctuation = ''
        punc_word = word
        for i in punc_word:
            if i in string.punctuation:
                punctuation = i
                print("Punctuation:", i)
        word = word.translate(str.maketrans('', '', string.punctuation))
        for changed_elem in changedTokens:
            if word == changed_elem['token']:
                print("Previous word", word)
                word = changed_elem['suggestions'][0]['suggestion']
                print("Changed word:", word)
        
        word = word + punctuation
        print("Word:", word)
        new_sentence.append(word)

        # TODO: Below code will be used to punctuations if original word has
        #       after replacing the suggested word from Bing API
        #if any(w in string.punctuation for w in word):
            #print("Punc:", word)
    print("New Sentence:", ' '.join(new_sentence))

    return ' '.join(new_sentence)


def spell_sentence_with_mark(text):

    api_key = "6b30752ba3fe4c36b5ca90216a8c0a81"
    endpoint = "https://api.bing.microsoft.com/v7.0/spellcheck"

    # Convert sentence to word list
    word_list = text.split(" ")


    # Separate punctuation if exists. Bing Spell Check API uses tokenized words.
    # If you post "sevg,", it will give you "sevgi" without comma.

    # Prepare data, params and headers
    data = {'text': text}

    params = {
        'mode': 'spell',
        'text': text,
        'mkt': 'tr-TR' 
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Ocp-Apim-Subscription-Key': api_key
    }

    # response = requests.get(endpoint, headers=headers, params=params, data=data)
    response = requests.get(endpoint, headers=headers, params=params)
    
    json_response = response.json()
    print(json_response)
    print("Second function")
    # Convert json to array
    changedTokens = json_response['flaggedTokens']
    print("Changed tokens:", changedTokens)
    new_sentence = []
    
    for word in word_list:
        punctuation = ''
        punctuation = ''
        punc_word = word
        for i in punc_word:
            if i in string.punctuation:
                punctuation = i
                print("Punctuation:", i)
        word = word.translate(str.maketrans('', '', string.punctuation))
        score = 0 # Initiate score as 0
        wrong_word = '' # Initiate empty 
        for changed_elem in changedTokens:
            if word == changed_elem['token']:
                print("Previous word", word)
                wrong_word = word
                word = changed_elem['suggestions'][0]['suggestion']
                print("Changed word:", word)
                score = 1 # Make score 1 if the word is changed. Used to mark the word
        word = word + punctuation
        print("Word:", word)
        new_sentence.append([word, score, wrong_word])

        # TODO: Below code will be used to punctuations if original word has
        #       after replacing the suggested word from Bing API
        #if any(w in string.punctuation for w in word):
            #print("Punc:", word)
    print("New Sentence:", new_sentence)

    return new_sentence