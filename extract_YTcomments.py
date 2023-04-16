#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# ChromeDriver起動
driver = webdriver.Chrome(ChromeDriverManager().install())

# YouTubeの動画ページを開く(/watch?v=任意のページID)
driver.get('https://www.youtube.com/watch?v=xxxxxxxxxxx')

# ページが完全に読み込まれるまで待機
time.sleep(15)

# ページを少しスクロール
driver.execute_script('window.scrollTo(0, 400);')
time.sleep(5)

# HTMLを取得
html = driver.page_source

# BeautifulSoupを使ってHTMLを解析
soup = BeautifulSoup(html, 'html.parser')

# コメントのセレクター
COMMENT_SELECTOR = '#content-text'

# コメントをすべて取得
def get_all_comments():
    # すべてのコメントを格納するリスト
    comments = []

    # コメントを取得
    while True:
        comment_elements = driver.find_elements_by_css_selector(COMMENT_SELECTOR)
        for comment_element in comment_elements:
            comment = comment_element.text.strip()
            if comment:
                comments.append(comment)

        # ページをスクロールして追加のコメントを表示
        driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);')
        time.sleep(5) # スクロールが完了するのを待つ

        # 新しいコメントが読み込まれなくなったらループを終了
        new_comment_elements = driver.find_elements_by_css_selector(COMMENT_SELECTOR)
        if len(new_comment_elements) == len(comment_elements):
            break

    return comments

# コメントを取得
comments = get_all_comments()
    
# CSVファイルに出力
import pandas as pd
df = pd.DataFrame(comments)
df = df.drop_duplicates() # 重複行の削除
df.to_csv('YouTubeComments.csv', index=None, encoding='cp932', errors='replace')

