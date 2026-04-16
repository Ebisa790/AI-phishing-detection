import re
import math
from urllib.parse import urlparse
from collections import Counter

def entropy(url):
    prob = [n_x / len(url) for x, n_x in Counter(url).items()]
    return -sum([p * math.log2(p) for p in prob])

# --- FIX IN feature_extraction.py ---

def extract_features(url):
    # Ensure URL has a scheme so urlparse works correctly
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    features = []
    # ... (rest of your code remains the same)

    # 1. Length of URL
    features.append(len(url))

    # 2. Number of dots
    features.append(url.count('.'))

    # 3. Presence of @
    features.append(1 if '@' in url else 0)

    # 4. HTTPS usage
    features.append(1 if url.startswith("https") else 0)

    # 5. IP address in URL
    features.append(1 if re.search(r'\d+\.\d+\.\d+\.\d+', url) else 0)

    # 6. Domain info
    domain = urlparse(url).netloc
    subdomains = domain.split('.')
    features.append(len(subdomains) - 2 if len(subdomains) > 2 else 0)

    # 7. Suspicious words
    suspicious_words = ["login", "verify", "bank", "secure", "account", "update"]
    features.append(sum(word in url.lower() for word in suspicious_words))

    # 8. Special characters
    features.append(sum(url.count(c) for c in ['-', '_', '?', '=', '&']))

    # 9. Domain length
    features.append(len(domain))

    # 🔥 10. Entropy (important for randomness detection)
    features.append(entropy(url))

    # 🔥 11. Suspicious TLD
    suspicious_tlds = [".xyz", ".top", ".tk", ".ml", ".ga", ".cf", ".gq"]
    features.append(1 if any(tld in url for tld in suspicious_tlds) else 0)

    # 🔥 12. HTTP inside HTTPS trick
    features.append(1 if "https" in url and "http" in url.replace("https", "") else 0)

    # 🔥 13. Long domain
    features.append(1 if len(domain) > 25 else 0)

    # 🔥 14. Count digits
    features.append(sum(c.isdigit() for c in url))

    # 🔥 15. Multiple // redirects
    features.append(1 if url.count("//") > 1 else 0)

    return features