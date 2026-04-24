import pandas as pd
import requests
import os

def fetch_phish_data():
    phishing_urls = []
    print("Fetching Phishing URLs from OpenPhish...")
    try:
        r = requests.get("https://openphish.com/feed.txt", timeout=15)
        if r.status_code == 200:
            phishing_urls = r.text.splitlines()[:500] 
    except Exception as e:
        print(f"OpenPhish Error: {e}. Using Emergency Backup.")
        phishing_urls = [
            "http://login-microsoft-verify.com", "http://paypal-secure-update.net",
            "http://cbe-ebanking-login.ga", "http://ethio-telecom-award.tk",
            "http://netflix-billing-fix.xyz", "http://facebook-security-check.co"
        ]
    return pd.DataFrame({'url': list(set(phishing_urls)), 'label': 1})

def fetch_safe_data():
    print("Generating expanded Safe URL list...")
    # Expanded list to improve accuracy and balance
    safe_domains = [
        "google.com", "youtube.com", "facebook.com", "wikipedia.org", "twitter.com",
        "instagram.com", "linkedin.com", "apple.com", "microsoft.com", "amazon.com",
        "netflix.com", "github.com", "reddit.com", "bing.com", "yahoo.com",
        "quora.com", "medium.com", "wordpress.com", "tumblr.com", "imdb.com",
        "pinterest.com", "whatsapp.com", "spotify.com", "adobe.com", "dropbox.com",
        "slack.com", "zoom.us", "vimeo.com", "bitly.com", "archive.org",
        "jimma.edu.et", "cbe.com.et", "ethiotelecom.et", "moe.gov.et", "pmo.gov.et",
        "aau.edu.et", "dstv.com", "goal.com", "bbc.com", "cnn.com", "reuters.com",
        "nytimes.com", "theguardian.com", "forbes.com", "bloomberg.com",
        "stackoverflow.com", "w3schools.com", "geeksforgeeks.org", "khanacademy.org",
        "udemy.com", "coursera.org", "edx.org", "mit.edu", "stanford.edu", "harvard.edu",
        "paypal.com", "ebay.com", "walmart.com", "target.com", "nike.com"
    ]
    
    # Generate variations to increase safe link count
    urls = []
    for d in safe_domains:
        urls.append(f"https://{d}")
        urls.append(f"https://www.{d}")
        urls.append(f"https://{d}/login")
    
    return pd.DataFrame({'url': list(set(urls)), 'label': 0})

def update_dataset():
    phish_df = fetch_phish_data()
    safe_df = fetch_safe_data()
    
    final_df = pd.concat([phish_df, safe_df]).drop_duplicates(subset='url')
    final_df.to_csv("dataset.csv", index=False)
    
    s_count = len(final_df[final_df['label'] == 0])
    p_count = len(final_df[final_df['label'] == 1])
    print(f"Dataset Saved Successfully!")
    print(f"Safe Links (Label 0): {s_count}")
    print(f"Phish Links (Label 1): {p_count}")

if __name__ == "__main__":
    update_dataset()