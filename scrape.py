import pandas as panda
import flask

from classes.coronavirus import Coronavirus

app = flask.Flask(__name__, static_folder='static')


@app.route('/')
def index():
    covid = Coronavirus('All')
    columns = ['Ölkə', 'Xəstələr', 'Yeni Xəstələr', 'Ölüm', 'Yeni Ölüm', 'Sağalıb']
    panda.set_option('display.max_rows', None)
    rows = covid.get_table_rows()
    stats = {k: v.replace(',', '') for (k, v) in covid.get_stats().items()}
    panda_table = panda.DataFrame(rows, columns=columns)
    return flask.render_template('index.html',
                                 stats=stats,
                                 table=panda_table.to_html(
                                     header='true',
                                     classes=['display', 'compact'],
                                     border=0,
                                     justify='left'
                                 ))
