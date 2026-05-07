from nltk import word_tokenize, download
from nltk.corpus import stopwords
try:
    download('punkt', quiet=True)
    download('punkt_tab', quiet=True)
    download('stopwords', quiet=True)
except:
    pass
try:
    sw = set(stopwords.words('english'))
except:
    sw = set()

def tokenize_and_remove_stopwords(text):
    tokens = word_tokenize(text)
    tokens = [t.lower() for t in tokens if t.isalpha()]
    filtered = [t for t in tokens if t not in sw]
    return tokens, filtered

def demo():
    doc = "The quick brown fox jumps over the lazy dog. This is a simple example to show tokenization and stopword removal."
    tokens, filtered = tokenize_and_remove_stopwords(doc)
    print('Original tokens:', tokens)
    print('After stopword removal:', filtered)
    try:
        from sklearn.feature_extraction.text import CountVectorizer
        vec = CountVectorizer(stop_words='english')
        X = vec.fit_transform([doc])
        print('Vocabulary:', vec.get_feature_names_out())
    except Exception as e:
        print('sklearn not available:', e)

if __name__ == '__main__':
    demo()
