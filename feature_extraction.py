import re
import math
from urllib.parse import urlparse
from collections import Counter

# =========================
# ENTROPY (URL randomness)
# =========================
def entropy(url):
    if len(url) == 0:
        return 0
    prob = [count / len(url) for count in Counter(url).values()]
    return -sum(p * math.log2(p) for p in prob)


# =========================
# MAIN FEATURE FUNCTION
# =========================
def extract_features(url):
    features = []

    parsed_url = urlparse(url)
    domain = parsed_url.netloc.lower()

    suspicious_words = ["login", "verify", "bank", "secure", "account", "update"]

    shorteners = ["bit.ly", "tinyurl", "t.co", "is.gd", "cutt.ly"]
    suspicious_tlds = [".xyz", ".top", ".tk", ".ml", ".ga"]

    weights = {
        "login": 2,
        "verify": 3,
        "bank": 3,
        "secure": 2,
        "account": 2,
        "update": 1
    }

    # =========================
    # BASIC FEATURES
    # =========================
    features.append(len(url))                          # URL length
    features.append(url.count('.'))                   # dots
    features.append(1 if '@' in url else 0)           # @ symbol
    features.append(1 if url.startswith("https") else 0)
    features.append(1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0)

    # subdomains
    subdomains = domain.split('.')
    features.append(1 if len(subdomains) > 3 else 0)

    # suspicious words (binary)
    features.append(1 if any(word in url.lower() for word in suspicious_words) else 0)

    # special characters
    features.append(sum(url.count(c) for c in ['-', '_', '?']))

    # domain length
    features.append(len(domain))

    # suspicious word count
    features.append(sum(word in url.lower() for word in suspicious_words))

    # URL depth
    features.append(url.count("/"))

    # =========================
    # ADVANCED FEATURES
    # =========================

    # entropy (randomness)
    features.append(entropy(url))

    # URL shortener
    features.append(1 if any(s in url for s in shorteners) else 0)

    # suspicious TLD
    features.append(1 if any(tld in url for tld in suspicious_tlds) else 0)

    # weighted phishing score
    score = sum(weight for word, weight in weights.items() if word in url.lower())
    features.append(score)

    return features