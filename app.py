from flask import Flask,request,jsonify,send_from_directory,Response
from waitress import serve
import base64

from uuid import uuid4
import datetime
import sqlite3



app = Flask(__name__)


conn_trackDB= sqlite3.connect('tracker.db',check_same_thread=False)

conn_trackDB.execute('''CREATE TABLE IF NOT EXISTS generate_uid_table
         (id INTEGER NOT NULL PRIMARY KEY,
         ip TEXT,
         user_agent TEXT,
         uid TEXT,
         datetime TIMESTAMP);''')
conn_trackDB.commit()

conn_trackDB.execute('''CREATE TABLE IF NOT EXISTS track_table
         (id INTEGER NOT NULL PRIMARY KEY,
         uid TEXT,
         ip TEXT,
         user_agent TEXT,
         datetime TIMESTAMP);''')
conn_trackDB.commit()








@app.route('/static/signature.gif',methods=['GET'])
def staticc():
    try:
        ip_address=request.environ['HTTP_X_FORWARDED_FOR']
    except:
        return redirect("https://domain.com", code=302)

    user_agent=str(request.headers.get('User-Agent'))


    uid=request.args.get('uid')
    if uid==None:
        return send_from_directory('static', 'signature.gif', as_attachment=False)
    else:
        conn_trackDB.execute("INSERT INTO track_table(uid,ip,user_agent,datetime) values(?,?,?,?)" ,(uid,ip_address,user_agent,str(datetime.datetime.now())))
        conn_trackDB.commit()
        return send_from_directory('static', 'signature.gif', as_attachment=False)



@app.route('/track/generate',methods=['GET'])
def generate():
    try:
        ip_address=request.environ['HTTP_X_FORWARDED_FOR']
    except:
        return redirect("https://domain.com", code=302)
    
    user_agent=str(request.headers.get('User-Agent'))


    datetime_data=str(datetime.datetime.now().strftime('%Y-%m-%d;%H:%M:%S:%f,'))
    uuid_data=str(uuid4().hex)
    dd_uu=(datetime_data+uuid_data).encode()

    uid = base64.urlsafe_b64encode(dd_uu).decode()
    html_string="""<div dir="ltr"><br></div><img src="https://domain.com/static/signature.gif?uid="""+uid+"""" alt="" width="0" height="0" style="width:2px;max-height:0;overflow:hidden">"""

    conn_trackDB.execute("INSERT INTO generate_uid_table(ip,user_agent,uid,datetime) values(?,?,?,?)" ,(ip_address,user_agent,uid,str(datetime.datetime.now())))
    conn_trackDB.commit()

    return Response('uid: '+uid+'\nhtml string: \n'+html_string, mimetype='text')



@app.route('/track/<uid>',methods=['GET'])
def track(uid):
    data=conn_trackDB.execute('SELECT * FROM track_table WHERE uid = "'+uid+'" ORDER BY id DESC').fetchall()
    returnData=[]
    for i in data:
        returnData.append('Last opened from user:  '+i[2]+'   at: '+i[4]+'   by: '+i[3])
    return jsonify({'data':returnData})



if __name__ == '__main__':
    app.run(debug=True,port=5000)
    #serve(app, host='0.0.0.0', port=5000, threads=6) #WAITRESS!
