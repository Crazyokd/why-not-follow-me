import requests
import time
import pyquery
import re
import os

# os.environ['NO_PROXY']="github.com"

proxies = { "http": None, "https": None}   # close proxy

headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'
    ,'Host': 'github.com'
    ,'Connection': 'close' # close keep-alive
}

followers_num = 0
following_num = 0

followers_usernames = []
following_usernames = []

followers_nicknames = []
following_nicknames = []

def visit(tab:str):
    url = f"https://github.com/Crazyokd?tab={tab}"
    response = requests.get(url=url,timeout=10,headers=headers,proxies=proxies)
    if response.status_code == 200:
        print(f"Successful visit {url}")
        print()

    # parse html
    html = pyquery.PyQuery(response.text)
    match_str = '.container-xl div .Layout-main div div.position-relative'
    text = html(match_str).html()
    if text == None:
        raise Exception("match string error! please check the match string")
    # write to file
    with open(f'{tab}.txt','w',encoding='utf-8') as f:
        f.write(text)


def handle_data(tab:str):
    with open(f'{tab}.txt','r',encoding='utf-8') as f:
        text = f.read()
    re_nickname = re.compile('<span class="f4 Link--primary(.*?)/.*?>',re.S)
    re_username = re.compile('<span class="Link--secondary.*?">(.*?)</span>',re.S)
    nicknames = re.findall(re_nickname,text)
    # print(nicknames)    # print all nicknames
    usernames = re.findall(re_username,text)
    # print(usernames)    # print all usernames

    # preprocess data
    for i in range(len(nicknames)):
        nicknames[i] = nicknames[i][1:].replace('>','').replace('<','')

    num = len(usernames)
    if tab == "followers":
        global followers_num
        global followers_nicknames
        global followers_usernames
        followers_num = num
        followers_nicknames = nicknames
        followers_usernames = usernames
    else:
        global following_num
        global following_nicknames
        global following_usernames
        following_num = num
        following_nicknames = nicknames
        following_usernames = usernames


def print_separator():
    for i in range(40):
        print("=",end="=")
    print()


def get_data(tab:str):
    success = False
    while not success:
        try:
            # visit(tab)
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


def get_result():
    # declare global variable
    global followers_nicknames
    global followers_usernames
    global following_num
    global following_nicknames
    global following_usernames

    # You follow to the other person and who doesn't follow you
    print()
    print("You follow to the other person and who doesn't follow you:\n")
    i = 0
    for i in range(following_num):
        try:
            index = followers_nicknames.index(following_nicknames[i])
        except ValueError:
            print(f"[{following_nicknames[i]}](https://github.com/{following_usernames[i]})")
        else:
            followers_nicknames.pop(index)
            followers_usernames.pop(index)
        

    print_separator()

    # Anothor person follow you and you doesn't follow him/her.
    print("Anothor person follow you and you doesn't follow him/her:\n")
    for i in range(len(followers_nicknames)):
        print(f"[{followers_nicknames[i]}](https://github.com/{followers_usernames[i]})")

def start():
    get_data("followers")
    # print separator
    print_separator()
    get_data("following")

    get_result()

if __name__=='__main__':
    # start application
    start()