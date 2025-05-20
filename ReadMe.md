# Instagram Mass Reporter 🚨

A powerful tool to mass report Instagram accounts with automatic ban verification.

![Warning](https://img.shields.io/badge/WARNING-Use%20Responsibly-red) 
![Python](https://img.shields.io/badge/Python-3.7+-blue)

## Features ✨

- Mass reports target accounts using all available report types
- Automatic ban verification using Instagram's API
- Proxy support for anonymity
- Multi-threaded for maximum efficiency
- Real-time progress tracking
- Notification when target gets banned

## Installation ⚙️

### Prerequisites
- Python 3.7+
- Instagram account (for verification only)

## How to use


Options:
  -t, --target USERNAME   Target Instagram username
  -u, --username USERNAME Your Instagram username
  -p, --password PASSWORD Your Instagram password
  --proxy-file FILE       Path to proxy list file
  --scrape-proxies        Scrape fresh proxies automatically
  --no-verify            Skip ban verification (not recommended)

  
### Setup
```bash

git clone https://github.com/ropuk019/Insta-mass-report.git

cd insta-mass-report

pip install -r requirements.txt

python main.py

