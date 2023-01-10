from flask import render_template, redirect, request, url_for
from app import app
from app.forms import SearchForm
# from bs4 import BeautifulSoup
from selenium import webdriver 
# import requests
import re, json, time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import requests
from bs4 import BeautifulSoup
import re
import json

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        # driver = webdriver.Chrome()
        # driver.get(f'https://www.youtube.com/results?search_query={search_form.data["query"]}')

        # try:
        #     channel_section=driver.find_element(By.TAG_NAME,'ytd-channel-renderer')
        # except NoSuchElementException:
        #     channel_section=None
        
        # if not channel_section:
        #     return redirect(url_for('notfound'))

        # print("found it")
        # youtube_data = []

        headers={
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
        }
        response = requests.get(f'https://www.youtube.com/results?search_query={search_form.data["query"]}', headers=headers)
        #print(response) #200
        time.sleep(3)
        soup = BeautifulSoup(response.text, 'html.parser')
        aid=soup.find('script',string=re.compile('ytInitialData'))
        extracted_josn_text=aid.text.split(';')[0].replace('window["ytInitialData"] =','').strip()
        print(extracted_josn_text)
        # video_results=json.loads(extracted_josn_text)
        # #print(item_section=video_results["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][1])
        # item_section=video_results["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]

        # for item in item_section:
        #     try:
        #         video_info=item["videoRenderer"]
        #         title=video_info["title"]["simpleText"]
        #         url=video_info["navigationEndpoint"]["commandMetadata"]["webCommandMetadata"]["url"]
        #         print('Title:',title)
        #         print('Url:',url, end="\n----------\n")
        #     except KeyError:
        #             pass



        return redirect(url_for('results', keyword=search_form.data['query']))
    return render_template('index.html', form=search_form)


@app.route('/results')
def results():  
    keyword = request.args.get("keyword")
    # print(keyword)
    if keyword == None:
        return redirect(url_for('notfound'))
    return render_template('results.html',keyword=keyword)


@app.route('/notfound')
def notfound():
    return render_template('404.html')

