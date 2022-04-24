from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time
import random
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import jieba
import jieba.analyse
import matplotlib.pyplot as plt
import os

def get_data():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
    
    
    browser.get('https://tw.news.yahoo.com/archive/')
    browser.maximize_window()
    wait = WebDriverWait(browser, 25)
    waitPopWindow = WebDriverWait(browser, 25)


    time.sleep(2)
    for i in range(10):
    # 指定像素
        jsCode = "var q=document.documentElement.scrollTop=130000"
        browser.execute_script(jsCode)
        time.sleep(1)
        
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    browser.quit()
    results = soup.select('li[class="StreamMegaItem"]')
    titles = []
    for result in results:
        title = result.select_one('h3[class="Mb(5px)"]').text.strip()
        titles.append(title)
        final =  " ".join(titles)
    return final
#中文分詞

# 載入自定義詞庫
# jieba.load_userdict(file_path)
# 加入字詞
# jieba.add_word(word, freq=None, tag=None)
# 刪除字詞
# jieba.del_word(word)
def get_stopword_list(file):
    with open(file, 'r', encoding='utf-8') as f:    # 
        stopword_list = [word.strip('\n') for word in f.readlines()]
    return stopword_list


# 分词 然后清除停用词语
def clean_stopword(str, stopword_list):
    result = []
    word_list = jieba.lcut(str)   # 分词后返回一个列表  jieba.cut(）   返回的是一个迭代器
    for w in word_list:
        if w not in stopword_list:
            result.append(w)
    return result


def word_pic(text):
    wc = WordCloud(font_path="華康POP1體W5 & 華康POP1體W5(P).ttc", #設置字體
               width=1600,
               height=800,
               background_color="white", #背景顏色
               max_words = 100 ,        #文字雲顯示最大詞數
               ).generate(text)   #停用字詞
    # wc = wc(width=1600, height=800).generate(text)
    wc.to_file('word_cloud.png')
    # 視覺化呈現
    # plt.imshow(wc)
    # plt.axis("off")
    # plt.figure(figsize=(20,10), dpi = 200)
    # plt.show()






if __name__ == '__main__':
    sents = get_data()
    stopword_file = 'stop.txt'
    stopword_list = get_stopword_list(stopword_file)    # 获得停用词列表
    jieba.load_userdict('dict.txt')
    jieba.load_userdict('user_dict.txt')
       # 打开要处理的文件
 
    
    targets = (clean_stopword(sents, stopword_list))
    text =  " ".join(targets)
    word_pic(text)
    # print(dest)
    
    
    


















# 默認模式
# seg_list = jieba.cut(Text, cut_all=False)
# # print('generator: ',seg_list)
# print(seg_list)
# for seg in seg_list:
#   results = seg,end=' '
  
# print(results)




