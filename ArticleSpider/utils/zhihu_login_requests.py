import requests
import re
try:
    import cookielib
except:
    import http.cookiejar as cookielib

session = requests.session()

agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
header = {
    "HOST":"www.zhihu.com",
    "Referer": "https://www.zhizhu.com",
    'User-Agent': agent
}

def get_xsrf():
    response = session.get('https://www.zhihu.com', headers=header)
    print(response.text)
    text = 'token&quot;:{&quot;xsrf&quot;:&quot;09913ba7-9614-4e36-bb65-8a2aead84669&quot;,&q'
    reg = 'token&quot;:{&quot;xsrf&quot;:&quot;?(.*)&quot;,&q'
    match_obj = re.match(reg, text)
    if match_obj:
        print(match_obj.group(1))
        return match_obj.group(1)
    else:
        return ''

def zhihu_login(account, password):
    post_url = 'https://www.zhihu.com/sign_in'
    post_data = {
        # '_xsrf': get_xsrf(),
        'username': account,
        'password': password
    }
    response_text = session.post(post_url, data=post_data, headers=header)

    session.cookies.save()

# get_xsrf()
zhihu_login(123, 123)