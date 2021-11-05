## imports

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import pandas as pd
import re
import requests
import bs4
from bs4 import BeautifulSoup
import time
import pprint
from datetime import datetime
import urllib
import base64
import os.path
import schedule
import pytz
import openpyxl
import os
from github import Github
import lxml




def job():
    #read in URL csv - Load in from your own directory

    directory = os.path.dirname(__file__)
    filename = "csv/nuevas_urls.csv"
    file_path = os.path.join(directory, filename)
    df_url = pd.read_csv(file_path, index_col=False)


    # create a list of URLS to iterate over
    arr_url = [ x for x in df_url['urls']]


    # ------------------------------ Run Scraper ---------------------------------------- #
    # ----------------------------------------------------------------------------------- #


    #lists will become columns in dataframe

    url = []
    top_comment_user = []
    top_comment = []
    thumbs_up = []

    count_url = 1
    for urls in arr_url[0:11]:
        print(str(count_url) + ' ' + str(urls))
        count_url += 1

        
        # try:
            
          
        ### ------- Remote Driver --------###
        # add headless mode
        options = webdriver.ChromeOptions()
        options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
        options.add_argument("--headless") # Runs Chrome in headless mode.
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox") # Bypass OS security model
        s=Service(os.environ.get("CHROMEDRIVER_PATH"))
        driver = webdriver.Chrome(service=s, options=options)
        driver.get(urls)
        
        
        ## Session data for website 
        #     {'authority': 'www.promodescuentos.com',
        #     'cache-control': 'max-age=0',
        #     'sec-ch-ua': '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        #     'sec-ch-ua-mobile': '?0',
        #     'sec-ch-ua-platform': '"macOS"',
        #     'upgrade-insecure-requests': '1',
        #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
        #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        #     'sec-fetch-site': 'none',
        #     'sec-fetch-mode': 'navigate',
        #     'sec-fetch-user': '?1',
        #     'sec-fetch-dest': 'document',
        #     'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        #     'cookie': 'view_layout_horizontal=%221-1%22; show_my_tab=0; f_v=%229f0ea980-3230-11ec-a29c-0242ac110003%22; _ga=GA1.3.1054458069.1634794497; _gid=GA1.3.1552499565.1634794497; ab.storage.userId.7af503ae-0c84-478f-98b0-ecfff5d67750=%7B%22g%22%3A%22browser-1626960373888-6%22%2C%22c%22%3A1634794497594%2C%22l%22%3A1634794497605%7D; ab.storage.deviceId.7af503ae-0c84-478f-98b0-ecfff5d67750=%7B%22g%22%3A%2264eea135-5993-3f15-ebc4-09adf427628c%22%2C%22c%22%3A1634794497609%2C%22l%22%3A1634794497609%7D; discussions_widget_selected_option=%22popular%22; _hjid=ae0f1ed2-2d92-4f09-bf43-c7bc66931033; __gads=ID=0ce43e3eff6da5ec:T=1634794499:S=ALNI_Mad7QJuOXppxRjU5egRVkmABAHc-A; stg_returning_visitor=Thu%2C%2021%20Oct%202021%2005:35:35%20GMT; navi=%7B%22homepage%22%3A%22picked%22%7D; _hjIncludedInSessionSample=0; xsrf_t=%22HEKJhu3kbDLqi5JfV1bDT2SpB0casC7t8lYr123B%22; _hjAbsoluteSessionInProgress=0; _pk_ses.12dffd1a-d9f7-4108-953d-b1f490724bce.09fe=*; stg_externalReferrer=; stg_traffic_source_priority=1; browser_push_permission_requested=1634922729; _gat=1; pepper_session=%22O3fygKnag0an5mcXzMUY4Cte4ZhqyaiBdI8DDjVk%22; remember_6fc0f483e7f442dc50848060ae780d66=%22778370%7CXrIutHkF0kW4HvN6kagIuDIqsQmOzP4HwyizQpKc3jl642wfYMc55YZfHmph%7C%242y%2410%24UCA2KfcAHkp28h5luvz69eim1o4ljCHTkbPNiE.Gm%5C%2FdRld.JuV4ei%22; u_l=1; ab.storage.sessionId.7af503ae-0c84-478f-98b0-ecfff5d67750=%7B%22g%22%3A%226b6610eb-9a5d-5719-499c-6571b7fa98c8%22%2C%22e%22%3A2134922914462%2C%22c%22%3A1634794497601%2C%22l%22%3A1634922914462%7D; stg_last_interaction=Fri%2C%2022%20Oct%202021%2017:15:17%20GMT; _pk_id.12dffd1a-d9f7-4108-953d-b1f490724bce.09fe=6f429fab6ac98163.1634794500.12.1634922917.1634919759.'})


        ###------- Local Driver --------###
        # DRIVER_PATH = '/Users/Niall-McNulty/Desktop/Computer Science Projects:Courses/Web Scraping/Web-scraping-www.promodescuentos.com-js/chromedriver'
        # # add headless mode
        # options = webdriver.ChromeOptions()
        # options.add_argument("--headless") # Runs Chrome in headless mode.
        # options.add_argument("--disable-gpu")
        # options.add_argument("--disable-dev-shm-usage")
        # options.add_argument('--no-sandbox') # Bypass OS security model
        # driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
        # driver.get(urls)
        


        r = driver.page_source
        print(r)
#         soup = BeautifulSoup(r, 'html.parser')

#     #--------------------------------------------------------------------------------------------------------------------#   
#     # append URL to list

#         try:
    #             url.append(urls)
    #         except:
    #             url.append(None)


    # #--------------------------------------------------------------------------------------------------------------------#   

    #         # check for top comment, username and thumbs up
    #         try:
                
    #             if soup.find_all('span',{'class':'lbox--v-3 space--l-2 size--all-m size--fromW2-l text--b'}):
    #                 find_comments = soup.find_all('span',{'class':'lbox--v-3 space--l-2 size--all-m size--fromW2-l text--b'})
    #                 for elements in find_comments:
    #                     # check for top comments
    #                     if 'Mejores comentarios' in elements.text:
    #                         # if there is, find the username (first matching element) and append to list
    #                         if soup.find('span',{'class': 'userInfo-username'}).text:
    #                             user_name = soup.find('span',{'class': 'userInfo-username'}).text
    #                             top_comment_user.append(user_name)
    #                         else:
    #                             top_comment_user.append(None)

    #                         # check for thumbs up amount and append to list
    #                         if soup.find('span', {'class': 'comment-like'}).text:
    #                             thumbs_up_count = soup.find('span', {'class': 'comment-like'}).text
    #                             thumbs_up.append(thumbs_up_count)
    #                         else:
    #                             thumbs_up.append(None)


    #                         # check for the parent div for comments
    #                         if soup.find('div',{'class':'commentList-item'}):
    #                             # assign it to a variable
    #                             parent = soup.find('div',{'class':'commentList-item'})
    #                             # check for top comment(first entry)
    #                             if parent.find('div',{'class':'comment-body'}):
    #                                 # grab text
    #                                 comment_text = parent.find('div',{'class':'comment-body'}).text
    #                                 # if there is no text, it is assumed to be a graphic or image
    #                                 if comment_text == '':
    #                                     top_comment.append('Graphic instead of text (image/meme)')
    #                                     # append text if there is
    #                                 else:
    #                                     top_comment.append(comment_text)
    #                         else:
    #                             top_comment.append(None)


    #                     else:
    #                         top_comment.append(None)

    #             else:
    #                 top_comment_user.append(None)
    #                 top_comment.append(None)
    #                 thumbs_up.append(None)
                
    #         except:
    #             top_comment_user.append(None)
    #             top_comment.append(None)
    #             thumbs_up.append(None)
                
                
    # #--------------------------------------------------------------------------------------------------------------------#   
                

    #     except:
            
    #         url.append(None)
    #         top_comment_user.append(None)
    #         top_comment.append(None)
    #         thumbs_up.append(None)

    #     if (count_url % 1000) == 0:

    #         data_dict = {'top_comment_user':top_comment_user,'top_comment':top_comment,'thumbs_up':thumbs_up}
    #         df_nuevas_data = pd.DataFrame.from_dict(data_dict)
    #         df_nuevas_data.index += 1

    #         # df_nuevas_data.to_csv('promodescuentos-nuevas-sixmonths' + str(count_url) + '.csv')
    #         # df_nuevas_data.to_excel('promodescuentos-nuevas-sixmonths' + str(count_url) + '.xlsx', encoding='utf-8')

    #         # directory = os.path.dirname(os.path.realpath(__file__))
    #         # filename = "nuevas_data-test-" + str(count_url) + ".csv"
    #         # file_path = os.path.join(directory, 'csv/', filename)
    #         # # # Save to csv format to handle encoding
    #         # df_nuevas_data.to_csv(file_path)

            
    #         # save to git using PyGithub
    #         github = Github(os.environ.get('GIT_KEY'))
    #         repository = github.get_user().get_repo('Web-scraping-www.promodescuentos.com-js')
    #         #path in the repository
    #         filename = 'promodescuentos-nuevas-' + str(count_url) + '.csv'
    #         # content to write
    #         df = df_nuevas_data.to_csv(sep=',', index=False)
    #         content = df
        

    #         #create a commit message
    #         f = repository.create_file(filename, "create updated scraper csv", content)
                


    # # Save complete file

    # data_dict = {'top_comment_user':top_comment_user,'top_comment':top_comment,'thumbs_up':thumbs_up}
    # df_nuevas_data = pd.DataFrame.from_dict(data_dict)

    # df_nuevas_data.index += 1

    # # directory = os.path.dirname(os.path.realpath(__file__))
    # # filename = "nuevas_data-final.csv"
    # # file_path = os.path.join(directory, 'csv/', filename)
    # # # # Save to csv format to handle encoding
    # # df_nuevas_data.to_csv(file_path)

    

    # save to git using PyGithub
    # github = Github(os.environ.get('GIT_KEY'))
    # repository = github.get_user().get_repo('Web-scraping-www.promodescuentos.com-js')
    # #path in the repository
    # filename = 'promodescuentos-nuevas-'+str(count_url)+'.csv'
    # # content to write
    # df = df_nuevas_data.to_csv(sep=',', index=False)
    # content = df


    # #create a commit message
    # f = repository.create_file(filename, "create updated scraper csv", content)
    # # Print on screen
    # # df_nuevas_data.to_csv('promodescuentos-nuevas-sixmonths' + str(count_url) + '.csv')
    # # df_nuevas_data.to_excel('promodescuentos-nuevas-sixmonths' + str(count_url) + '.xlsx', encoding='utf-8')
    


        

schedule.every(2).minutes.do(job)
    # # # # # schedule.every().hour.do(job)
    # # # # # schedule.every().day.at('01:57').do(job)
    # # # # # schedule.every(5).to(10).minutes.do(job)
# schedule.every().friday.at('00:30').do(job)
# # # # # # schedule.every().thursday.at("17:24").do(job)
# # # # # # schedule.every().minute.at(":17").do(job)

while True:
    schedule.run_pending()
    time.sleep(1) # wait one second


# test locally ------


x = job()
pprint.pprint(x)

x.to_csv('test.csv')



