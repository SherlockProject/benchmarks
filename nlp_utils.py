"""
This is a script to perform a NER-tagging using the stanford ner-tagger. Written for python2 might work for python3.
"""

from os import popen, devnull
from os.path import abspath, dirname, sep
from string import punctuation
from subprocess import call, PIPE

import nltk
from nltk.tag.stanford import NERTagger


# specifies whether three or seven ner-tag classes are used
num_classes = 3


# PATH FOR STANFORD NAMED ENTITY TAGGER
local_path = dirname(abspath(__file__))
stanford_ner_path = abspath(local_path + sep + 'stanford-ner')
stanford_ner = stanford_ner_path + sep + 'stanford-ner.jar'
if num_classes == 3 :
    stanford_ner_classifier = stanford_ner_path + sep + 'classifiers' + sep + 'english.all.3class.distsim.crf.ser.gz'
else :
    stanford_ner_classifier = stanford_ner_path + sep + 'classifiers' + sep + 'english.muc.7class.distsim.crf.ser.gz'


def ner_tag(sents, silent=True) :
    """ Named Entety Recognition for sentences.

        Keyword arguments:
            sents -- Sentece, list of sentences or list of tokens.
        Returns :
            List of (word,neg-tag) pairs, that aims to preserve the structure of the sents input argument.
    """

    if len(sents) == 0 :
        return []

    # saves ner_tagger as global variable,
    # such that it is not recreated everytime ner_tag is executed
    if not 'ner_tagger' in globals():
        global ner_tagger
        ner_tagger = NERTagger(stanford_ner_classifier, stanford_ner)

    # if sentence not tokenized
    if type(sents) in [str,unicode] :
        sents = tokenize(sents,'sw')

    # bring input sents in right form
    elif type(sents[0]) in [str,unicode] :
        if ' ' in sents[0] :
            sents = [tokenize(s,'w') for s in sents]
        else :
            sents = [sents]

    tagged = ner_tagger.tag_sents(sents)

    if not silent :
        print('ner-tags:', tagged)

    return tagged


def tokenize(text_structure, types='psw') :
    """ Tokenize a text into paragraphs, sentences inclusive-or words.
        
        types - 'p' activates paragraph segmentation, 's' sentence and 'w' word.
    """

    #--> maybe 'text tilling' algorithm to split into multi-paragraph subtopics

    # split into paragraphs
    if 'p' in types :
        text_structure = _paragraph_tokenize(text_structure)

    # split into sentences
    if 's' in types :
        text_structure = _sent_tokenize(text_structure)

    # word tokenization
    if 'w' in types :
        text_structure = _word_tokenize(text_structure)

    return text_structure


def _paragraph_tokenize(text_structure):
    if hasattr(text_structure, '__iter__') :
        text_structure = [_paragraph_tokenize(substruc) for substruc in text_structure]
    else :
        # split into paragraphs
        text_structure = text_structure.split('\n')
        # remove leading and trailing whitespace characters of each paragraph
        text_structure = [sts.strip() for sts in text_structure]
        # remove empty paragraphs
        text_structure = [sts for sts in text_structure if sts!='']
    return text_structure


def _sent_tokenize(text_structure):
    if hasattr(text_structure, '__iter__') :
        text_structure = [_sent_tokenize(substruc) for substruc in text_structure]
    else :
        text_structure = nltk.sent_tokenize(text_structure)
    return text_structure


def _word_tokenize(text_structure):
    if hasattr(text_structure, '__iter__') :
        text_structure = [_word_tokenize(substruc) for substruc in text_structure]
    else :
        text_structure = nltk.word_tokenize(text_structure)
    return text_structure


def untokenize(tokens) :
    """ transforms an arbitrarily deep list of list of words
        into a string, so basically reverses the tokenization process """
    if len(tokens)>0 and tokens and hasattr(tokens[0], '__iter__') :
        return [untokenize(t) for t in tokens]
    return "".join([" "+i if not i.startswith("'") and i not in punctuation else i for i in tokens]).strip()


def text_to_speech(text, engine='google'):

    if engine == 'google' :

        # remove some unwanted characters
        text = text.replace('(',' ')
        text = text.replace(')',' ')
        text = text.replace('`','')
        text = text.replace("'",'')
        text = text.replace('"','')
        text = text.replace("-",' ')
        text = text.replace(",",' ')

        # the google speech synthesis accpets a maximal amount of characters
        n = 90
        
        # the text is split into sentences
        sents = tokenize(text, 's')

        for sent in sents :

            # split sentence into chunks of maximum n characters
            # ToDo: consider word boundaries
            chunks = [sent[i:i+n] for i in range(0, len(sent), n)]

            # call the speech.sh bash-script with each chunk
            for chunk in chunks :
                cmd = local_path + sep + 'speech.sh ' + '"' + chunk + '"'
                FNULL = open(devnull, 'w') # used to suppress error messages from mplayer
                call(cmd.split(), stderr=FNULL)

    elif engine == 'espeak' :
        cmd = 'espeak ' + '"' + text + '"'
        call(cmd.split())

    else :
        print('No such speech engine:', engine)

