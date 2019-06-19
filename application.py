# from flask import Flask
from flask import Flask, request, render_template
import pyodbc
import time
import redis
import pickle
import random
import matplotlib.pyplot as plt

app = Flask(__name__)

server = 'mysqlserver644.database.windows.net'
database = 'mySampleDatabase'
username = 'azureuser'
password = 'Cloud@20'
driver = '{ODBC Driver 13 for SQL Server}'

cacheName1 = 'testQueryRes1'
cacheName2 = 'testQueryRes2'
cacheName3 = 'testQueryRes3'
cacheName4 = 'testQueryRes4'
rds = redis.StrictRedis(host='vishnu.redis.cache.windows.net', port=6380, db=0,
                           password='cbeRE1b5xwb4VErP7rD29FFOvUbZ4FHW20oUJhcW4gQ=', ssl=True)


def db_operation(sql , count):
	print('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1443;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
	cnxn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server+ ';PORT=1443;DATABASE=' + database+ ';UID=' + username + ';PWD=' + password)
	print(cnxn)
	cursor = cnxn.cursor()
	if count != 0:
		starttime = time.time()
		for x in range(count):
			cursor.execute(sql)
		endtime = time.time()
		duration = endtime - starttime
		return duration

	cursor.execute(sql)
	rows = cursor.fetchall()
	cursor.close()
	cnxn.close()
	print(rows)
	return rows

@app.route("/")
def home():
 	return render_template('index1.html')

@app.route("/query1" ,methods=['POST','GET'])
def query1():
	derror1 = (int)(request.form['derror1'])
	derror2 = (int)(request.form['derror2'])
	#long = request.form['long']
	count = request.form['count']
	print(type(derror1) ,type(derror2))
	dic= {}
	#for i in range(0, int(count)):
	starttime = time.time()
	for i in range(0,int(count)):
		random1 = random.randint(derror1, derror2)
		random2 = random.randint(derror1, derror2)
		print(random1,random2)
		sql = "select * from quake6_1 where depthError between {} and {}".format(random1,random2)
		print(sql)
		duration = db_operation(sql,0)
		dic.update({str(random1)+"," +str(random2) : duration})
		print(dic)
	endtime = time.time()
	duration = endtime - starttime
	return render_template("1result.html", result=dic,time = duration )


        #sql = "select latitude,longitude,time,depthError from quake6_1 where depthError between {} and {}".format( derror1, derror2)
        #duration = db_operation(sql,0)
    #return render_template("1result.html",result = duration)


@app.route("/query1WithCache" ,methods=['POST','GET'])
def query11():
    derror1 = (int)(request.form['derror1'])
    derror2 = (int)(request.form['derror2'])
    count=(int)(request.form['count'])
    dic = {}
    print(type(count))
    if rds.exists(cacheName1):
        isCache = 'True'
        start_time = time.time()
        for i in range(0,count):
            results = pickle.loads(rds.get(cacheName1))
        end_time = time.time()
        rds.delete(cacheName1)
        duration = end_time - start_time
    else:
        isCache = 'False'
        random1 = random.randint(derror1, derror2)
        random2 = random.randint(derror1, derror2)
        sql = "select * from quake6_1 where depthError between {} and {}".format(random1,random2)
        duration = db_operation(sql,count)
        dic.update({str(random1) + "," + str(random2): duration})
        rds.set(cacheName1, pickle.dumps(duration))
    return render_template('cacheresult.html',isCache=isCache, time=duration)

# @app.route('/query2', methods=['GET','POST'])
# def query2():
# 	derror1 = (int)(request.form['derror1'])
# 	derror2 = request.form['derror2']
# 	long = (int) (request.form['long'])
# 	combined_result = []
# 	header = []
# 	result = []
#     #sql = "select * from quake6 where longitude > {} and depthError between {} and {}".format(long, derror1, derror2)
#
#
#     #sql = "select * from quake6 where longitude > {} and depthError between {} and {}".format(long, derror1, derror2)
#     #duration = db_operation(sql,count)
#
#
# 	#return render_template('1result.html', result = duration)
#
# @app.route('/query2WithCache', methods=['GET','POST'])
# def query22():
# 	km = (int)(request.form['km'])
# 	location = request.form['location']
# 	count = (int) (request.form['count'])
# 	if rds.exists(cacheName2):
# 		isCache = 'True'
# 		start_time = time.time()
# 		for i in range(0,count):
# 			results = pickle.loads(rds.get(cacheName2))
# 		end_time = time.time()
# 		rds.delete(cacheName2)
# 		duration = end_time - start_time
# 	else:
# 		isCache = 'False'
# 		sql = "select * from all_month where ((place LIKE %s) AND (substring(place,1,1) between '0' and %s) AND (substring(place,2,2) = 'km'))" % (
# 		'\'%' + location + '%\'', km)
# 		duration = db_operation(sql,count)
# 		rds.set(cacheName2, pickle.dumps(duration))
# 	return render_template('cacheresult.html',isCache=isCache, time=duration)
#
#
#
# @app.route('/searchbwdatesAndMag' ,methods=['GET','POST'])
# def query3():
# 	count = (int)(request.form['count'])
# 	start = request.form['startdate']
# 	start = start[0:10]
# 	end = request.form['enddate']
# 	end = end[0:10]
# 	frmRange = request.form['mag1']
# 	toRange = request.form['mag2']
# 	print(start , end , type(start) ,  type(end))
# 	#sql = "select * from QUAKES where (to_date(substring(TIME,1,10),'YYYY-MM-DD') between %s and %s) AND (DEPTH between %s and %s)" % ('\'' + start + '\'', '\'' + end + '\'', frmRange, toRange)
# 	sql ="select * from ASSIGNMENT3.quakes where (select CONVERT(DATE, substring(quakes.TIME,1,10))) BETWEEN (SELECT CONVERT(DATE,'{}')) AND (SELECT CONVERT(DATE,'{}')) AND (quakes.MAG between {} and {})".format(start,end,frmRange,toRange)
# 	print(sql)
# 	# select * from ASSIGNMENT3.quakes where (select CONVERT(DATE, substring(quakes.TIME,1,10))) BETWEEN (SELECT CONVERT(DATE,'2019-05-08')) AND (SELECT CONVERT(DATE,'2019-05-31')) AND (quakes.DEPTH between 5 and 7)
# 	print(sql)
# 	duration = db_operation(sql, count)
# 	return render_template("result1.html", result=duration)
#
# @app.route('/searchbwdatesAndMagCache' ,methods=['GET','POST'])
# def query33():
# 	count = (int)(request.form['count'])
# 	start = request.form['startdate']
# 	start = start[0:10]
# 	end = request.form['enddate']
# 	end = end[0:10]
# 	frmRange = request.form['mag1']
# 	toRange = request.form['mag2']
# 	print(start, end, type(start), type(end))
# 	if rds.exists(cacheName3):
# 		isCache = 'True'
# 		start_time = time.time()
# 		for i in range(0,count):
# 			results = pickle.loads(rds.get(cacheName3))
# 		end_time = time.time()
# 		rds.delete(cacheName3)
# 		duration = end_time - start_time
# 	else:
# 		isCache = 'False'
# 		sql = "select * from ASSIGNMENT3.quakes where (select CONVERT(DATE, substring(quakes.TIME,1,10))) BETWEEN (SELECT CONVERT(DATE,'{}')) AND (SELECT CONVERT(DATE,'{}')) AND (quakes.MAG between {} and {})".format(
# 			start, end, frmRange, toRange)
# 		duration = db_operation(sql,count)
# 		rds.set(cacheName3, pickle.dumps(duration))
# 	return render_template('cacheresult.html',isCache=isCache, time=duration)
#
# @app.route('/getearthquakedatabetweenMag' ,methods=['GET','POST'])
# def getEarthquakes():
# 	mag1 = (int)(request.form['magnitude1'])
# 	mag2 = (int)(request.form['magnitude2'])
# 	count = (int)(request.form['count'])
# 	sql = "select * from ASSIGNMENT3.quakes where MAG between  {} AND {}".format(mag1, mag2)
# 	print(sql)
# 	duration = db_operation(sql, count)
# 	return render_template("result1.html", result=duration)
#
# @app.route('/getearthquakedatabetweenMagcache' ,methods=['GET','POST'])
# def getEarthquakesCache():
# 	mag1 = (int)(request.form['magnitude1'])
# 	mag2 = (int)(request.form['magnitude2'])
# 	count = (int)(request.form['count'])
# 	if rds.exists(cacheName4):
# 		isCache = 'True'
# 		start_time = time.time()
# 		for i in range(0,count):
# 			results = pickle.loads(rds.get(cacheName4))
# 		end_time = time.time()
# 		rds.delete(cacheName4)
# 		duration = end_time - start_time
# 	else:
# 		isCache = 'False'
# 		sql = "select * from ASSIGNMENT3.quakes where MAG between  {} AND {}".format(mag1, mag2)
# 		duration = db_operation(sql,count)
# 		rds.set(cacheName4, pickle.dumps(duration))
# 	return render_template('cacheresult.html',isCache=isCache, time=duration)
#
# @app.route('/populationRange',methods=['GET','POST'])
# def getPopulationRange():
# 	pop1 = (int)(request.form['pop1'])
# 	pop2 = (int)(request.form['pop2'])
# 	year = (int)(request.form['year'])
# 	starttime = time.time()
# 	# select ASSIGNMENT3.population.State from ASSIGNMENT3.population where ASSIGNMENT3.population.[2011] between  713906 and 4785448
# 	sql ="select State from population where [{}] between  {} and {}".format(year,pop1,pop2)
# 	print(sql)
# 	results = db_operation(sql,0)
# 	endtime = time.time()
# 	duration = endtime - starttime
# 	return render_template('populationRange.html',data=results,time=duration)
#
# @app.route('/getStateCode',methods=['GET','POST'])
# def getStateCode():
# 	statecode = request.form['statecode']
# 	starttime = time.time()
# 	# sql = "SELECT population.state, population.["+year+"] FROM population, statecode\
# 	#        where statecode.code = \'"+ code +"\' and population.state = statecode.state"
# 	sql = "SELECT state from ASSIGNMENT3.statecode where CONVERT(VARCHAR, ASSIGNMENT3.statecode.code) = CONVERT(VARCHAR, '{}')".format(statecode)
# 	print(sql)
# 	results = db_operation(sql, 0)
# 	print(results[0][0])
# 	sql = "SELECT * from ASSIGNMENT3.counties where CONVERT(VARCHAR, ASSIGNMENT3.counties.State) = CONVERT(VARCHAR, '{}')".format(results[0][0])
# 	print(sql)
# 	results = db_operation(sql, 0)
# 	print(results)
# 	# sql = "SELECT ASSIGNMENT3.counties.state, count(ASSIGNMENT3.counties.county) from ASSIGNMENT3.counties where CONVERT(VARCHAR, ASSIGNMENT3.counties.State) = CONVERT(VARCHAR, '{}')".format(results[0][0])
# 	sql = "SELECT ASSIGNMENT3.counties.State, count(CONVERT(VARCHAR,ASSIGNMENT3.counties.county)) from ASSIGNMENT3.counties where CONVERT(VARCHAR, ASSIGNMENT3.counties.State) = CONVERT(VARCHAR, '{}')".format(results[0][0])
# 	print(sql)
# 	count = db_operation(sql, 0)
# 	print(count)
# 	endtime = time.time()
# 	duration = endtime - starttime
# 	return render_template('stateCounty.html', data=results, count = count[0], time=duration)




if __name__ == '__main__':
  app.run()
