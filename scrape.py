import pandas as panda
import requests
from bs4 import BeautifulSoup
import flask

app = flask.Flask(__name__)

html = """
<! DOCTYPE html>
<html lang = "en">
<head>
    <meta charset = "UTF-8">
    <title>Confirmed Coronavirus Cases and Deaths by Country</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
</head>
<body>
{{table | safe}}
</body>
</html>
"""
 
class Coronavirus:
    __check_params = [None, 'All']
    __table_attribute = 'id'
    __attribute_value = 'main_table_countries'
    __website_url = 'http://www.worldometers.info/coronavirus'
 
    def __init__(self, country=None):
        self.country = country
        html = requests.get(self.__website_url)
        soup = BeautifulSoup(html.text, 'html.parser')
        self.table = soup.find('table', {self.__table_attribute: self.__attribute_value})
 
    def get_result(self):
        trs = self.find_all_trs()
        rows = []
        for tr in trs[1:]:
            tds = self.__find_all_tds(tr)
            rows.append(tds[:6])
            if self.country not in self.__check_params and self.country in tds[0]:
                return [tds[:6]]
        return rows
 
    def find_all_trs(self):
        return self.table.find_all('tr')
 
    @staticmethod
    def __find_all_tds(tr):
        return [td.get_text(strip=True) for td in tr.find_all('td')]
    
    
@app.route('/') 
def index():
    covid = Coronavirus('Azerbaijan')
    columns = ['Ölkə', 'Xəstələr', 'Yeni Xəstələr', 'Ölüm', 'Yeni Ölüm', 'Sağalıb']
    panda.set_option('display.max_rows', None)
    panda_table = panda.DataFrame(covid.get_result(), columns=columns)
    return flask.render_template_string (html, table = panda_table.to_html (header = 'true'))

