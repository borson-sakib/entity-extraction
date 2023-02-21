import spacy
from spacy import displacy
from collections import Counter,defaultdict
from pprint import pprint


import en_core_web_sm
nlp = en_core_web_sm.load()
# nlp_keyword = spacy.load("en_core_sci_lg")


def naturalLP(doc):

    doc = nlp(doc)

    dick = [(X.text, X.label_) for X in doc.ents]

    html = displacy.render(doc,page=True, style='ent')

    # print(type(displacy.render(doc, page=True, style='ent')))
    # print(html)
    return html


def naturalLPlist(doc):

    doc = nlp(doc)

    dick = [(X.text, X.label_) for X in doc.ents]

    # html = displacy.render(nlp(doc), jupyter=True, style='ent')

    return dick

def group_entities_by_type(entity_list):
    entity_dict = {}
    for entity in entity_list:
        parts = entity.split('\n')
        entity_type = parts[2].strip()
        entity_name = parts[1].strip()
        if entity_type not in entity_dict:
            entity_dict[entity_type] = []
        entity_dict[entity_type].append(entity_name)
    return entity_dict

def extract_keywords(text, top_n=5):
    # Load the text and tokenize it
    doc = nlp(text)

    # Calculate the word frequency
    word_frequencies = defaultdict(int)
    for word in doc:
        if not word.is_stop and not word.is_punct:
            word_frequencies[word.text.lower()] += 1

    # Normalize the word frequencies
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] /= max_frequency

    # Calculate the sentence scores using TextRank algorithm
    sentence_scores = defaultdict(int)
    for sent in doc.sents:
        for word in sent:
            if word.text.lower() in word_frequencies:
                sentence_scores[sent] += word_frequencies[word.text.lower()]

    # Select the top n sentences
    top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:top_n]

    # Extract the top n keywords from the selected sentences
    keywords = []
    for sent in top_sentences:
        for word in sent:
            if not word.is_stop and not word.is_punct and word.pos_ in ["NOUN", "PROPN"]:
                keywords.append(word.text)

    return list(set(keywords))

# def keyextract(doc):

#     doc = nlp_keyword(doc)

#     return doc.ents