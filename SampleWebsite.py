from flask import Flask, render_template, request, send_file
import pandas as pd
import plotly.express as px
from plotly.io import write_image
import io

app = Flask(__name__)
df = pd.read_csv("Reports/01-27-2023.csv")

@app.route('/')
def index():
    cities = df['oras'].unique()
    cities.sort()
    zones = df['zona'].unique()
    return render_template('index.html', cities=cities, zones=zones)

@app.route('/show_graph')
def show_graph():
    city = request.args.get('city')
    # zone = request.args.get('zone')
    filtered_df = df[(df['oras'] == city)]# & (df['zona'] == zone)]
    # create graph using plotly
    fig = px.scatter(filtered_df, x='zona', y='pret', title=f'Price in {city}')
    # save the graph as a PNG file
    buf = io.BytesIO()
    write_image(fig,buf, format='png', width=800, height=600)
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run()
