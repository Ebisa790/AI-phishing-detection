import re
import math
from urllib.parse import urlparse
from collections import Counter

def entropy(url):
    prob = [n / len(url) for n in Counter(url).values()]
    return -sum(p * math.log2(p) for p in prob)

def extract_features(url):
    features = []

    # Basic features
    features.append(len(url))
    features.append(url.count('.'))
    features.append(1 if '@' in url else 0)
    features.append(1 if url.startswith("https") else 0)
    features.append(1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0)

    # Domain features
    domain = urlparse(url).netloc
    features.append(len(domain))

    subdomains = domain.split('.')
    features.append(len(subdomains) - 2 if len(subdomains) > 2 else 0)

    # Suspicious words
    suspicious_words = ["login", "verify", "bank", "secure", "account", "update"]
    features.append(1 if any(word in url.lower() for word in suspicious_words) else 0)
    features.append(sum(word in url.lower() for word in suspicious_words))

    # Special characters
    features.append(url.count('-'))
    features.append(url.count('_'))
    features.append(url.count('?'))
    features.append(url.count('/'))

    # Entropy (VERY IMPORTANT 🔥)
    features.append(entropy(url))

    # Shortener detection
    shorteners = ["bit.ly", "tinyurl", "t.co", "is.gd", "cutt.ly"]
    features.append(1 if any(s in url for s in shorteners) else 0)

    # Suspicious TLDs
    suspicious_tlds = [".xyz", ".top", ".tk", ".ml", ".ga"]
    features.append(1 if any(tld in url for tld in suspicious_tlds) else 0)

    # Weighted keyword score
    weights = {
        "login": 2,
        "verify": 3,
        "bank": 3,
        "secure": 2,
        "account": 2,
        "update": 1
    }
    score = sum(weight for word, weight in weights.items() if word in url.lower())
    features.append(score)

    return features