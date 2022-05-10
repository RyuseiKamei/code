
from logging import root
from kivymd.app import MDApp
from kivy.config import Config
Config.set('kivy', 'keyboard_mode', 'systemandmulti')
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder, builder
from time import sleep
from kivymd.icon_definitions import md_icons
from kivymd.uix.list import OneLineIconListItem
from kivy.properties import StringProperty
import requests
from bs4 import BeautifulSoup
import pandas as pd

class UI(ScreenManager):
    results = StringProperty()
    

class Sample(MDApp):
    

    def build(self):
        return UI()

    def getNm(self):   #ユーザネーム入力
        NNM = self.root.ids.N_n.text
        print(NNM)

    

    def getKy(self):   #パスワード入力
        KKY = self.root.ids.K_k.text
        print(KKY)

    

    def getStr(self):    #メインファイル実行
        NNM = self.root.ids.N_n.text
        KKY = self.root.ids.K_k.text
        import os #csvファイルを削除するためのライブラリ
        from tqdm import tqdm
        from time import sleep #スリープ間隔をインストール
        from selenium import webdriver #seleniumからwebdriverをインストール
        from selenium.webdriver.support.ui import WebDriverWait #seleniumから　waitをインポート
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as EC #処理待機をさせるライブラリをインポート
        from webdriver_manager.chrome import ChromeDriverManager #マネージャでchromeを立ち上げ
        bar1 = tqdm(total = 10) #プログレスバーで進捗状況を可視化

        from selenium.webdriver.chrome.options import Options
        options = Options()
        options.add_argument('--headless')
        browser = webdriver.Chrome(ChromeDriverManager().install()) #chromedriverマネージャを強制インストール #,options=options
        bar1.update(1)
        sleep(0.1)
        url = 'https://www.instagram.com/accounts/access_tool/' #ログイン画面表示
        browser.get(url)
        sleep(1)
        elem_username = browser.find_element_by_name('username') #ユーザーネーム入力
        elem_username.send_keys(NNM)
        elem_password = browser.find_element_by_name('password') #パスワード入力
        elem_password.send_keys(KKY)
        elem_password.submit() #ログインボタンのクリック
        sleep(2)
        elem_after = browser.find_element_by_class_name('sqdOP.yWX7d.y3zKF') #ログイン情報の保存をキャンセル
        elem_after.click()
        
        bar1.update(1)
        sleep(0.1)
        #フォロワー　一覧
        url2 = 'https://www.instagram.com/accounts/access_tool/accounts_following_you' #フォロワーデータの表示
        browser.get(url2)

        #要素指定からクリックまでの処理を関数化
        def more_look():
            WebDriverWait(browser, 7).until(EC.element_to_be_clickable((By.CLASS_NAME, "sqdOP.L3NKy.y3zKF")))
            elem_look = browser.find_element_by_class_name('sqdOP.L3NKy.y3zKF') #btnクリック
            elem_look.click()

        #while関数でtryをループ
        while True: #もっと見るbtnのクリック処理の繰り返しでデータ一覧を全表示
            try:
                more_look()
        
            except:
                print('フォロワー読み込み完了')
                break

        bar1.update(1.5)
        sleep(0.1)
        #フォロワー　抽出
        followers = []
        followers_name = browser.find_elements_by_class_name('-utLf') #フォロワーデータのクラスをまとめて抽出

        #抽出したクラスを全て一覧表示
        for follower_name in followers_name:
            follower = follower_name.text
            followers.append(follower)
        #CSVに抽出
        import pandas as pd
        df_1=pd.DataFrame()
        df_1['Follower']= followers
        df_1.to_csv('Follower.csv',index=False)

        bar1.update(1)
        sleep(0.1)
        #フォロー　一覧
        url3 = 'https://www.instagram.com/accounts/access_tool/accounts_you_follow' #フォローデータの表示
        browser.get(url3)

        #要素指定からクリックまでの処理を関数化
        def more_look():
            WebDriverWait(browser, 7).until(EC.element_to_be_clickable((By.CLASS_NAME, "sqdOP.L3NKy.y3zKF")))
            elem_look = browser.find_element_by_class_name('sqdOP.L3NKy.y3zKF') #btnクリック
            elem_look.click()

        bar1.update(1)
        sleep(0.1)

        #while関数でtryをループ
        while True: #もっと見るbtnのクリック処理の繰り返しでデータ一覧を全表示
            try:
                more_look()
        
            except:
                print('フォロー読み込み完了')
                break 

        bar1.update(1.5)
        sleep(0.1)
        #フォロー　抽出
        follows = []
        follows_name = browser.find_elements_by_class_name('-utLf') #フォロワーデータのクラスをまとめて抽出

        bar1.update(1)
        sleep(0.1)
        #抽出したクラスを全て一覧表示
        for follow_name in follows_name:
            follow = follow_name.text
            follows.append(follow)

        bar1.update(1)
        sleep(0.1)
        #CSVに抽出
        import pandas as pd
        df_2=pd.DataFrame()
        df_2['Follow']= follows
        df_2.to_csv('Follow.csv',index=False)

        #各CSVデータをmergeで比較し新たにCSVファイル”管理”として抽出し保存
        import pandas as pd
        df_a = pd.read_csv('Follower.csv')
        df_b = pd.read_csv('Follow.csv')
        df_a_b = pd.merge(df_a,df_b,left_on = ['Follower'],right_on = ['Follow'],how = 'outer',indicator = True)
        df_a_b.to_csv('管理表.csv',index=False)

        #各データごとにCSVファイルを作成
        #相互
        df_both = df_a_b[df_a_b["_merge"] == 'both']
        df_both.to_csv('相互.csv',index=False)

        #ファン
        df_fans = df_a_b[df_a_b["_merge"] == 'left_only']
        df_fans.to_csv('Fans.csv',index=False)

        #アンフォロバ
        df_unflbk = df_a_b[df_a_b["_merge"] == 'right_only']
        df_unflbk.to_csv('Nofb.csv',index=False)

        sleep(1)

        bar1.update(1)
        sleep(0.1)
        #csvから必要な列データ抽出
        EACH = pd.read_csv('相互.csv', encoding = 'SHIFT_JIS')
        Each = EACH.loc[:,['Follower']]

        FAN = pd.read_csv('Fans.csv', encoding = 'SHIFT_JIS')
        Fan = FAN.loc[:,['Follower']]

        NOFB = pd.read_csv('Nofb.csv', encoding = 'SHIFT_JIS')
        Nofb = NOFB.loc[:,['Follow']]

        sleep(1)

        #実行結果を表示
        pd.set_option('display.max_rows', None)
        print('フォローバックされていないユーザーは下記の一覧です。')
        NoFb = Nofb.replace('        ','')
        print(NoFb)

        #osライブラリでcsvファイルを削除
        import os
        os.remove('Fans.csv')
        os.remove('Follow.csv')
        os.remove('Follower.csv')
        os.remove('Nofb.csv')
        os.remove('管理表.csv')
        os.remove('相互.csv')
    
        #Lineへ通知
        headers = {
            'Authorization': 'Bearer oOSKQ1sVBtTBimQP7avixGc7QpJdiOHINcwxSqLxiaa', #トークン発行
        }
        
        files = {
            'message': (None, 'フォローバックされていないユーザー',NoFb), #メッセージテキスト送信
        }

        requests.post('https://notify-api.line.me/api/notify', headers=headers, files=files) #LINEapiのアクセス




    def getRes(self):
        global BQB
        BQB = "abcdefg"
        self.results = BQB
        print(self.results)



    def parse_html(url):

        sleep(1)

        html = requests.get(url)

        return BeautifulSoup(html.text, 'html.parser')


Sample().run()

#二段階認証をoffにする
#認証機能付きWifiネットワークでは実行不可(セキュリティにより)
#instagramの二段階認証をオンにしてるアカウントではログイン不可
#プログラムを実行とサーチを開始の間のスペースにタイマー機能を追加する
#ユーザはタイマーの時間を目安に処理時間を参考に待つ
#pyファイルのグローバル変数をkvファイルで扱えるようにする
#kvファイルから変数をウィンドウ表示させる。
#closeボタンを設置もしくはHomeボタンに全プログラムの停止と削除処理を追加する

