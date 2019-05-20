import spacy
import nltk
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("wordnet")
from nltk.corpus import stopwords
from string import punctuation
from nltk.probability import FreqDist
import re
from nltk import wordpunct_tokenize
from nltk.stem import WordNetLemmatizer

# Detects language
def detectLanguage(text):
    ratios = {}
    tokens = wordpunct_tokenize(text)
    words = [word.lower() for word in tokens]
    for lang in stopwords.fileids():
        stopwords_set = set(stopwords.words(lang))
        words_set = set(words)
        common_words = words_set.intersection(stopwords_set)
        ratios[lang] = len(common_words)
    most_rated_language = max(ratios, key=ratios.get)
    return most_rated_language

# Normalizes the text: removes digits, punctuation, newlines...
def normalizeText(text):
    text = ''.join(c for c in text if not c.isdigit())
    text = ''.join(c for c in text if c not in punctuation).lower()
    text = re.sub('\s+', ' ', text)
    text = text.replace('\u00b7', ' ')
    text = text.replace('\n\n', '')
    text = text.replace('\n', '')
    text = text.replace('\t', '')
    text = text.replace(' » ',' ')
    text = text.replace(' « ',' ')
    text = text.replace('–',' ') 
    text = text.replace('\x92',' ')
    text = text.replace('§','')
    return text

# Strips non-ascii characters
def strip_non_ascii(s):
    s = (c for c in s if 0 < ord(c) < 255)
    s = ''.join(s)
    return s


def processText(text, language):

    text = normalizeText(text)

    STOPLIST = []
    if language == "french":
        STOPLIST = stopwords.words('french')
    elif language == "english":
        STOPLIST = stopwords.words('english')
    text = ' '.join([word for word in text.split() if word not in STOPLIST])

    text = strip_non_ascii(text)
    
    return text

# Tokenizes words and extracts n most frequent words
def getFreqWords(text,n):
    allWords = nltk.tokenize.word_tokenize(text)
    lemmatizer = WordNetLemmatizer() 
    topWords = [lemmatizer.lemmatize(word) for word in allWords]
    fdist = FreqDist(topWords)
    topWords = [word[0] for word in fdist.most_common(n)]
    return topWords

# Processes the whole document
def processDoc(doc,n=30):

    processedDoc = doc
    text = []
    allText = ' '.join([p for p in doc['text']])
    lang = detectLanguage(allText)

    for p in processedDoc['text']:
        text.append(processText(p,lang))

    allText = ' '.join(text)

    processedDoc['lang'] = lang
    processedDoc['text'] = text
    processedDoc['allText'] = allText
    processedDoc['freqWords'] = getFreqWords(allText,n)

    return processedDoc