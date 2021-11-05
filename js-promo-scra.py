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
import pickle as pickle




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

        
        try:
            
          
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


            directory = os.path.dirname(__file__)
            filename = "cookie.pkl"
            file_path = os.path.join(directory, filename)
            cookies = pickle.load(open(file_path, 'rb'))
            for cookie in cookies:
                driver.add_cookie(cookie)
            
            r = driver.page_source
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

            # element = driver.find_element_by_css_selector("#comments")
            # html = driver.execute_script("return arguments[0].innerHTML;", element)
            
            # main = driver.execute_script("return document.body.innerHTML;")
            soup = BeautifulSoup(r, 'lxml')

        #--------------------------------------------------------------------------------------------------------------------#   
        # append URL to list

            try:
                url.append(urls)
            except:
                url.append(None)


        #--------------------------------------------------------------------------------------------------------------------#   

                # check for top comment, username and thumbs up
            try:
                
                if soup.find_all('span',{'class':'lbox--v-3 space--l-2 size--all-m size--fromW2-l text--b'}):
                    find_comments = soup.find_all('span',{'class':'lbox--v-3 space--l-2 size--all-m size--fromW2-l text--b'})
                    for elements in find_comments:
                        # check for top comments
                        if 'Mejores comentarios' in elements.text:
                            # if there is, find the username (first matching element) and append to list
                            if soup.find('span',{'class': 'userInfo-username'}).text:
                                user_name = soup.find('span',{'class': 'userInfo-username'}).text
                                top_comment_user.append(user_name)
                            else:
                                top_comment_user.append(None)

                            # check for thumbs up amount and append to list
                            if soup.find('span', {'class': 'comment-like'}).text:
                                thumbs_up_count = soup.find('span', {'class': 'comment-like'}).text
                                thumbs_up.append(thumbs_up_count)
                            else:
                                thumbs_up.append(None)


                            # check for the parent div for comments
                            if soup.find('div',{'class':'commentList-item'}):
                                # assign it to a variable
                                parent = soup.find('div',{'class':'commentList-item'})
                                # check for top comment(first entry)
                                if parent.find('div',{'class':'comment-body'}):
                                    # grab text
                                    comment_text = parent.find('div',{'class':'comment-body'}).text
                                    # if there is no text, it is assumed to be a graphic or image
                                    if comment_text == '':
                                        top_comment.append('Graphic instead of text (image/meme)')
                                        # append text if there is
                                    else:
                                        top_comment.append(comment_text)
                                else:
                                    top_comment.append(None)


                            else:
                                top_comment.append(None)

                        else:
                            top_comment_user.append(None)
                            top_comment.append(None)
                            thumbs_up.append(None)
                    else:
                        top_comment_user.append(None)
                        top_comment.append(None)
                        thumbs_up.append(None)
                
            except:
                top_comment_user.append(None)
                top_comment.append(None)
                thumbs_up.append(None)
                        
                    
        #--------------------------------------------------------------------------------------------------------------------#   
                    

        except:
            
            url.append(None)
            top_comment_user.append(None)
            top_comment.append(None)
            thumbs_up.append(None)

        if (count_url % 1000) == 0:

            data_dict = {'top_comment_user':top_comment_user,'top_comment':top_comment,'thumbs_up':thumbs_up}
            df_nuevas_data = pd.DataFrame.from_dict(data_dict)
            df_nuevas_data.index += 1

            # df_nuevas_data.to_csv('promodescuentos-nuevas-sixmonths' + str(count_url) + '.csv')
            # df_nuevas_data.to_excel('promodescuentos-nuevas-sixmonths' + str(count_url) + '.xlsx', encoding='utf-8')

            # directory = os.path.dirname(os.path.realpath(__file__))
            # filename = "nuevas_data-test-" + str(count_url) + ".csv"
            # file_path = os.path.join(directory, 'csv/', filename)
            # # # Save to csv format to handle encoding
            # df_nuevas_data.to_csv(file_path)

            
            # save to git using PyGithub
            github = Github(os.environ.get('GIT_KEY'))
            repository = github.get_user().get_repo('Web-scraping-www.promodescuentos.com-js')
            #path in the repository
            filename = 'promodescuentos-nuevas-' + str(count_url) + '.csv'
            # content to write
            df = df_nuevas_data.to_csv(sep=',', index=False)
            content = df
        

            #create a commit message
            f = repository.create_file(filename, "create updated scraper csv", content)
                


    # Save complete file

    data_dict = {'top_comment_user':top_comment_user,'top_comment':top_comment,'thumbs_up':thumbs_up}
    df_nuevas_data = pd.DataFrame.from_dict(data_dict)

    df_nuevas_data.index += 1

    # directory = os.path.dirname(os.path.realpath(__file__))
    # filename = "nuevas_data-final.csv"
    # file_path = os.path.join(directory, 'csv/', filename)
    # # # Save to csv format to handle encoding
    # df_nuevas_data.to_csv(file_path)

    

    #save to git using PyGithub
    github = Github(os.environ.get('GIT_KEY'))
    repository = github.get_user().get_repo('Web-scraping-www.promodescuentos.com-js')
    #path in the repository
    filename = 'promodescuentos-nuevas-' + str(count_url) + '.csv'
    # content to write
    df = df_nuevas_data.to_csv(sep=',', index=False)
    content = df


    #create a commit message
    f = repository.create_file(filename, "create updated scraper csv", content)
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


# x = job()
# pprint.pprint(x)

# x.to_csv('test.csv')



