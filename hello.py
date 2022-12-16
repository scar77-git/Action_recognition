import pymysql
from flask import *
import json
app = Flask(__name__)
#database connection
connection = pymysql.connect(
  user='root', password='', host='127.0.0.1', database='capstone_proj'
)
cursor = connection.cursor()
#inserting data to db
cycle={ 'cycles': [  ] } 
cycle_Data={ 'cycle_no': 0, 'video': { 'video_id':0 ,'video_src': " ",}, 'tasks':[ { 'task_name':" ", 'task_id':0 ,'time:0, status':" " } ]}
@app.route('/get_data',methods=["POST", "GET"])
def get_data():
    if request.method == "POST":
        print("hello")
        hello = request.json
        print("#################################33")
          
    a1 = hello["a"]  
    a2=hello["b"]
    print(a1)
    print(a2)
    query = ("SELECT cycle_info.SNO,cycle_info.Cycle_no,labels.label_name,cycle_info.Time,cycle_info.task_id,cycle_info.Time_stamp FROM cycle_info JOIN labels ON cycle_info.task_id = labels.label_id where cycle_info.Time_stamp BETWEEN %s AND %s")
    values = (a1,a2)
    cursor.execute(query,values)
    connection.commit()
    a=cursor.fetchall()
    a = sorted(a,key=lambda x: x[1])
    o={"cycles":[]}
    key_name={'Light_guide':0,'diffuser':1,'Adhesive_tape_check':2,'lcd':3,'Metal_stacker':4,'grown_check':5}

    for i in range(0,len(a),6):
     ct=0
     t={}
     while ct<6 and (i+ct)<len(a):
        j=i+ct
        t[a[j][2]]=a[j][3]
        ct+=1
     cycle = {"cycle_id":(a[i][1]),"cycle_name":" ", "task":t}
     o["cycles"].append(cycle)
    o = json.dumps(o['cycles'], indent = 4)
    print(o)
    return "ok"
  
@app.route('/get_data1',methods=["POST", "GET"])
def get_data1():
  if request.method == "POST":
        print("hello")
        hello = request.json
        print("#################################33")
          
  a1 = hello["a"]  
  query = ("SELECT cycle_info.SNO,cycle_info.Cycle_no,labels.label_name,cycle_info.Time,cycle_info.video_src,cycle_info.video_id,cycle_info.status,cycle_info.task_id FROM cycle_info JOIN labels ON cycle_info.task_id = labels.label_id where cycle_info.Cycle_no<=%s")
  values = (a1)
  cursor.execute(query,values)
  connection.commit()
  a=cursor.fetchall()
  #print(a)
  a = sorted(a,key=lambda x: x[1])
  o={"cycles":[]}
  key_name={'Light_guide':0,'diffuser':1,'Adhesive_tape_check':2,'lcd':3,'Metal_stacker':4,'grown_check':5}

  for i in range(0,len(a),6):
     task={"tasks":[]}
     ct=0
     while ct<6 and (i+ct)<len(a):
        j=i+ct
        t_no = key_name[a[j][2]]
        t={"task_no":t_no, "task_name":a[j][2],"time_taken":a[j][3]}
        task["tasks"].append(t)
        ct+=1
     cycle = {"cycle_no":(i//6+1),"video":{"video_no":12345,"video_src":"https://tinyurl.com/2c8hy5xm"}, "tasks":task}
     o["cycles"].append(cycle)
  o = json.dumps(o, indent = 4)
  print(o)
  return "ok"
  


if __name__=="__main__":
	app.run(port=8081,debug=True)    
    

# API requests:    
#requests.post('http://localhost:8081/get_data',json={"a":1671030051.331564,"b":1671030531.331564},proxies={"http":"","https":""})    
#requests.post('http://localhost:8081/get_data1',json={"a":10},proxies={"http":"","https":""})