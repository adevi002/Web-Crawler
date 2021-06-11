from urllib.parse import urlparse       #  14


# extracting domain name (example.com)
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')  # splits up name.example.com into three pieces (based on where '.' is)
        return results[-2] + '.' + results[-1]         # takes last two elements and returns them with a '.' in the middle
    except:
        return ''

# Get sub domain name (name.example.com)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''