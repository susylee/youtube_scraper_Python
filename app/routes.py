from flask import render_template, redirect, request, url_for
from app import app
from app.forms import SearchForm
# from bs4 import BeautifulSoup
from selenium import webdriver 
# import requests
import re, json, time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        driver = webdriver.Chrome()
        driver.get(f'https://www.youtube.com/results?search_query={search_form.data["query"]}')

        try:
            channel_section=driver.find_element(By.TAG_NAME,'ytd-channel-renderer')
        except NoSuchElementException:
            channel_section=None
        
        if not channel_section:
            return redirect(url_for('notfound'))

        print("found it")
        youtube_data = []

        # response = requests.get(f'https://www.youtube.com/results?search_query={search_form.data["query"]}')
        # # print(response) #200
        # soup = BeautifulSoup(response.content, 'html.parser')
        # # We locate the JSON data using a regular-expression pattern
        # data = re.search(r"var ytInitialData = ({.*});", str(soup)).group(1)
        # # json_data = json.loads(data)

        # with open('readme.txt', 'w') as f:
        #     f.write(data)
        
        # # print(json_data)
        # # Uncomment to view all the data
        # # print(json.dumps(data))
        # # search = soup.select("#search")
        # # print(soup.prettify())
        # # print(soup.find('#contents'))
        # print(search_form.errors)

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

