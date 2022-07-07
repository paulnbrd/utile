import requests


def shorten(url: str):
    sess = requests.Session()
    sess.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
        "Alt-Used": "bitly.com",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Host": "bitly.com",
        "Origin": "https://bitly.com",
        "Referer": "https://bitly.com"
    }
    sess.get("https://bitly.com")
    return sess.post("https://bitly.com/data/anon_shorten", {
        "url": url
    }).text
    

if __name__ == "__main__":
    print(shorten("https://google.com"))
