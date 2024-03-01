import heapq
from flask import *
import bs4 as bs
import urllib.request
import re
import math
import nltk
nltk.download('stopwords')
nltk.download('punkt')

app = Flask(__name__)

@app.route('/')
def indexpage():
    return render_template('index.html')


@app.route('/home')
def inputtext():
    return render_template('home.html')


@app.route('/url')
def inputurl():
    return render_template('url.html')


@app.route('/urlresult', methods=['GET', 'POST'])
def summaryurl():
    if request.method == 'POST':
        link = request.form['url']

    # Getting the data source
    source = urllib.request.urlopen(link).read()

    # Parsing the data/ creating BeautifulSoup object
    soup = bs.BeautifulSoup(source, 'html.parser')

    #Fetching the data
    text = ""
    for paragraph in soup.find_all('p'):
        text += paragraph.text

    #    Preprocessing the data
    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    clean_text = text.lower()
    clean_text = re.sub(r'\W', ' ', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text)

    # Tokenize sentences
    sentences = nltk.sent_tokenize(text)

    # Stopword list
    stop_words = nltk.corpus.stopwords.words('english')

    # Word counts
    word2count = {}
    for word in nltk.word_tokenize(clean_text):
        if word not in stop_words:
            if word not in word2count.keys():
                word2count[word] = 1
            else:
                word2count[word] += 1

    # Converting counts to weights
    max_count = max(word2count.values())
    for key in word2count.keys():
        word2count[key] = word2count[key]/max_count

    # Product sentence scores
    sent2score = {}
    for sentence in sentences:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word2count.keys():
                if len(sentence.split(' ')) < 25:
                    if sentence not in sent2score.keys():
                        sent2score[sentence] = word2count[word]
                    else:
                        sent2score[sentence] += word2count[word]

    # Gettings best lines
    n = len(sentences)
    if n<=10:
        best_sentences = sentences
    elif n<50 and n > 10:
        best_sentences = heapq.nlargest(8, sent2score, key=sent2score.get)
    elif n>= 50 and n < 100:
        best_sentences = heapq.nlargest(15, sent2score, key=sent2score.get)
    elif n >= 100 and n < 200:
        best_sentences = heapq.nlargest(20, sent2score, key=sent2score.get)
    elif n>= 200 and n< 500:
        best_sentences = heapq.nlargest(25, sent2score, key=sent2score.get)
    elif n >= 500 and n < 1000:
        best_sentences = heapq.nlargest(30, sent2score, key=sent2score.get)
    elif n >= 1000:
        final = int(math.ceil(0.03 * n))
        best_sentences = heapq.nlargest(final, sent2score, key=sent2score.get)

    final_summary = ""
    for sentence in sentences:
        if sentence in best_sentences:
            final_summary += sentence + " "

    return render_template("urlresult.html", summary=final_summary)

@app.route('/result', methods=['GET', 'POST'])
def summary():

    #Fetching the data
    if request.method == 'POST':
        text = request.form['textinput']
        originaltext = text


    #    Preprocessing the data
    text = re.sub(r'\[[0-9]*\]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    clean_text = text.lower()
    clean_text = re.sub(r'\W', ' ', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text)

    # Tokenize sentences
    sentences = nltk.sent_tokenize(text)

    # Stopword list
    stop_words = nltk.corpus.stopwords.words('english')

    # Word counts
    word2count = {}
    for word in nltk.word_tokenize(clean_text):
        if word not in stop_words:
            if word not in word2count.keys():
                word2count[word] = 1
            else:
                word2count[word] += 1

    # Converting counts to weights
    max_count = max(word2count.values())
    for key in word2count.keys():
        word2count[key] = word2count[key]/max_count

    # Product sentence scores
    sent2score = {}
    for sentence in sentences:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word2count.keys():
                if len(sentence.split(' ')) < 25:
                    if sentence not in sent2score.keys():
                        sent2score[sentence] = word2count[word]
                    else:
                        sent2score[sentence] += word2count[word]

    # Gettings best lines
    n = len(sentences)
    if n<=10:
        best_sentences = sentences
    if n<50 and n > 10:
        best_sentences = heapq.nlargest(8, sent2score, key=sent2score.get)
    elif n>= 50 and n < 100:
        best_sentences = heapq.nlargest(15, sent2score, key=sent2score.get)
    elif n >= 100 and n < 200:
        best_sentences = heapq.nlargest(20, sent2score, key=sent2score.get)
    elif n>= 200 and n< 500:
        best_sentences = heapq.nlargest(85, sent2score, key=sent2score.get)
    elif n >= 500 and n < 1000:
        best_sentences = heapq.nlargest(85, sent2score, key=sent2score.get)
    elif n >= 1000:
        final = int(math.ceil(0.03 * n))
        best_sentences = heapq.nlargest(final, sent2score, key=sent2score.get)


    final_summary = ""
    for sentence in sentences:
        if sentence in best_sentences:
            final_summary += sentence + " "

    return render_template("result.html", summary=final_summary, original=originaltext)


if __name__ == '__main__':
    app.run(debug=True)
