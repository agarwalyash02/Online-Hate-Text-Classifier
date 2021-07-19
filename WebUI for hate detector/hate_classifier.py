import pickle
import re
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import nltk.corpus

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
sw = set(stopwords.words("english"))



model = load_model("/home/ec2-user/Webserver/static/new_model_03")


with open("/home/ec2-user/Webserver/static/word_to_idx.pkl","rb") as w2i:
    word_to_idx=pickle.load(w2i)


def filter_words(word_list):
    useful_words = [ w for w in word_list if w not in sw ]
    return(useful_words)

def preprocess_data(dataset):
    data = dataset.copy()
    t = []
    for i in data:
        sentence = str(i)
        sentence = sentence.lower()
        sentence = re.sub(r'@\w+ | http | #\w+', '', sentence)
        t.append(sentence)


    #Removing punctuations, special characters and lemmatizing words to their base form
    val = [''.join([WordNetLemmatizer().lemmatize(re.sub('[^A-Za-z]',' ',text)) for text in lis]) for lis in t]
    
    a=[]
    for text in val:
        word_list = word_tokenize(text)
        text=filter_words(word_list)
        a.append(text)  
    
    train_text = []
    for i in a:
      train_text.append(' '.join(i))

    return train_text


max_len=40
def data_generator(texts):
    desc = preprocess_data([texts])[0]
    seq = [word_to_idx[word] for word in desc.split() if word in word_to_idx]
    xi = pad_sequences([seq],maxlen=max_len,value=0,padding='post')[0]
    xi = xi.reshape((1,max_len))
    return xi

def get_prediction(text):
    data = data_generator(text)
    val = model.predict_classes(x=data)[0][0]
    if val==1:
        return "hate or negative"
    else:
        return "positive"
