import re

def clean_html(html_text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html_text).strip()