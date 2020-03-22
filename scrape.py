import flask

from classes.coronavirus import Coronavirus

app = flask.Flask(__name__, static_folder='static')


@app.route('/')
def home():
    covid19 = Coronavirus('All')
    columns = ['Ölkə', 'Xəstələr', 'Yeni Xəstələr', 'Ölüm', 'Yeni Ölüm', 'Sağalıb']
    rows = covid19.get_table_rows()
    stats = {k: v.replace(',', '') for (k, v) in covid19.get_stats().items()}
    return flask.render_template('home/index.html',
                                 stats=stats,
                                 rows=rows,
                                 columns=columns)


@app.route('/covid')
def covid():
    data = "Covid haqqında"
    return flask.render_template('covid/index.html', data=data)
