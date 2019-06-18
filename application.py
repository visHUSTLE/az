# from flask import Flask
from flask import Flask, request, render_template
import pyodbc
import time
import redis
import pickle

app = Flask(__name__)

server = 'mysqlserver644.database.windows.net'
database = 'mySampleDatabase'
username = 'azureuser'
password = 'Cloud@20'
driver = '{ODBC Driver 17 for SQL Server}'

cacheName = 'vishnu'
rd = redis.StrictRedis(host='vishnu.redis.cache.windows.net', port=6380, db=0,
                           password='cbeRE1b5xwb4VErP7rD29FFOvUbZ4FHW20oUJhcW4gQ=', ssl=True)


def db_operation(sql):
    cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server
                          + ';PORT=1443;DATABASE=' + database
                          + ';UID=' + username + ';PWD=' + password)

    cursor = cnxn.cursor()
    starttime = time.time()
    cursor.execute(sql)
    rows = cursor.fetchall()
    endtime = time.time()
    duration = endtime - starttime
    #print(duration)
    cursor.close()
    cnxn.close()
    return rows

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/searchMag', methods=['POST','GET'])
def my_form():
    mag = request.form['mag']
    count = request.form['count']
    starttime = time.time()
    for i in range(0,int(count)):

        sql = "select * from all_month where MAG>{}".format(mag)

        results = db_operation(sql)
    endtime = time.time()
    duration = endtime - starttime
    return render_template('index.html', results = results, time=duration)




@app.route('/quakeRangeRedis', methods=['POST','GET'])
def quakeRangeRedis():
    mag = request.form['mag']
    mag1 = request.form['mag1']
    count = request.form['count']
    if rd.exists(cacheName):
        print('Found Cache')
        start_time = time.time()
        results = pickle.loads(rd.get(cacheName))
        end_time = time.time()

    else:
        print("Cache Not Found")
        cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server
                              + ';PORT=1443;DATABASE=' + database
                              + ';UID=' + username + ';PWD=' + password)
        cursor = cnxn.cursor()

        start_time = time.time()
        for i in range(0, int(count)):
            cursor.execute("select * from all_month where MAG between {} and {}".format(mag, mag1))
        end_time = time.time()

        columns = [column[0] for column in cursor.description]

        results = []
        for row in cursor.fetchall():
            # results.append(row)
            results.append(dict(zip(columns, row)))
            # print(row[0])

        # print(results)
        cursor.close()
        cnxn.close()

        # r.set( cacheName, results)
        # r.get('foo')
        rd.set(cacheName, pickle.dumps(results))

    total_time = end_time - start_time
    return render_template('city.html', ci=results, time=total_time)



if __name__ == '__main__':
  app.run()
