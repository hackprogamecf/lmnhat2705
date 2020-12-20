
import datetime
from flask import Flask, render_template
from google.cloud import datastore
datastore_client = datastore.Client()
app = Flask(__name__)
def store_time(dt):
    entity = datastore.Entity(key=datastore_client.key('visit'))
    entity.update({
        'timestamp': dt
    })

    datastore_client.put(entity)


def fetch_times(limit):
    query = datastore_client.query(kind='visit')
    query.order = ['-timestamp']
    times = query.fetch(limit=limit)
    return times


@app.route('/')
def root():
    store_time(datetime.datetime.now())
    times = fetch_times(10) #Lấy thời gian 10 lượt truy cập gần nhất
    return render_template(
        'index.html', times=times)  #Đưa vào index hiển thị



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)    #Chạy trên port 8080 và localhost: 127.0.0.1
