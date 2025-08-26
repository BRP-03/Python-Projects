from urllib.parse import urlparse

def is_url(url):
    try:
        result=urlparse(url)
        return all([result.scheme,result.netloc])
    except:
        return False
url="https://youtu.be/2_ufYaJNi7w?si=9JQrZnvT4NWN8IRF"
print("This is brp")