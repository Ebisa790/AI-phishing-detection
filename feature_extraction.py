import re
import math
from urllib.parse import urlparse
from collections import Counter

def entropy(url):
    prob = [n_x / len(url) for x, n_x in Counter(url).items()]
    return -sum([p * math.log2(p) for p in prob])



def extract_features(url):

    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path
    
    features = []
    

    suspicious_words = ["login", "verify", "bank", "secure", "cbe", "tele", "jimma"]
    features.append(sum(word in domain.lower() for word in suspicious_words)) # High risk
    features.append(sum(word in path.lower() for word in suspicious_words))   # Medium risk


    return features