import requests
import time
import pyquery
import re
import os

from requests.models import ReadTimeoutError

# os.environ['NO_PROXY']="github.com"

proxies = { "http": None, "https": None}   # close proxy

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
    ,'Host': 'github.com'
    ,'Connection': 'close' # close keep-alive
}

def visit(tab:str):
    response = requests.get(url=f"https://github.com/Crazyokd?tab={tab}",timeout=10,headers=headers,proxies=proxies)
    if response.status_code == 200:
        print("visit success")

    html = pyquery.PyQuery(response.text)
    match_str = '.container-xl div .Layout-main div div.position-relative '
    followers = html(match_str)
    text = followers.html()
    if text == None:
        raise Exception("match string error! please check the match string")
    with open(f'{tab}.txt','w',encoding='utf-8') as f:
        f.write(text)


def handle_data(tab:str):
    with open(f'{tab}.txt','r',encoding='utf-8') as f:
        text = f.read()
    re_nickname = re.compile('<span class="f4 Link--primary">(.*?)</span>',re.S)
    re_username = re.compile('<span class="Link--secondary pl-1">(.*?)</span>',re.S)
    nicknames = re.findall(re_nickname,text)
    print(nicknames)
    usernames = re.findall(re_username,text)
    print(usernames)


def get_data(tab:str):
    success = False
    while not success:
        try:
            visit(tab)
            handle_data(tab)
            success = True
        except requests.exceptions.ReadTimeout:
            error_msg = 'ReadTimeout!'
        except requests.exceptions.ConnectionError:
            error_msg = 'ConnectionError!'
        except Exception as e:
            print(e)
            break
        if not success:
            print(f"%s auto retry after 5 seconds ..." % error_msg)
            time.sleep(5)


if __name__=='__main__':
    get_data("followers")
    # print separator
    for i in range(20):
        print("=",end="=")
    print()
    get_data("following")