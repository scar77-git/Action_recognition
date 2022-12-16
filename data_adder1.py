import mysql.connector
from datetime import datetime, timedelta
import pandas as pd
import cv2
mydb = mysql.connector.connect(
  user='root', password='', host='127.0.0.1', database='capstone_proj'
)

mycursor = mydb.cursor()
rows=1
import datetime;
ct = datetime.datetime.now()
sql = "INSERT INTO cycle_info (SNO,Cycle_no,task_id,Time,video_src,video_id,status,Time_stamp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
sample_rate=2
video_src='/content/drive/MyDrive/action_clips_resized/output/outputnewupdate3.mp4'
label_src='/content/drive/MyDrive/action_clips_resized/output/labels.txt'
vid = cv2.VideoCapture(video_src)
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
if int(major_ver)  < 3 :
        fps = vid.get(cv2.cv.CV_CAP_PROP_FPS)
else :
        fps = vid.get(cv2.CAP_PROP_FPS)
df = pd.read_csv(label_src)
df1=pd.DataFrame(df)
dlist=df1.values.tolist()
l=[]
for i in dlist:
  l.extend(i)
print(l)
dict1={'grown_check':[],'lcd':[],'Light_guide':[],'Metal_stacker':[],'Adhesive_tape_check':[],'diffuser':[]}
i=0
while i < len(l):
  x=l[i]
  x1=i+1
  c=0
  l1=[]
  l1.append(x)
  while x1<len(l) and x==l[x1]:
    l1.append(l[x1])
    x1=x1+1
  i=x1
  val=(len(l1)*sample_rate)/fps
  dict1[x].append(val)
print(dict1)
#dict1={'grown_check': [2.1, 2.1, 4.2, 2.1, 2.1, 4.2, 2.1, 2.1, 2.0, 0.1, 6.3, 4.2, 0.1, 2.0, 2.1, 2.1, 4.2, 4.2, 2.1, 2.1, 4.2, 4.2, 2.1, 2.1, 4.2, 2.1, 2.1, 0.1, 0.1, 1.9], 'lcd': [4.2, 6.3, 4.2, 4.2, 10.5, 2.1, 2.1, 4.2, 2.1, 2.1, 2.1, 0.1, 2.0, 2.1, 2.1, 8.4, 2.1, 2.1, 0.1, 0.2, 0.1, 1.7, 2.1, 2.1, 2.1, 6.3, 0.1, 2.0, 2.1, 2.1, 4.2, 0.1, 0.2, 1.8, 8.4, 6.0, 0.1, 0.1, 0.1, 2.1, 4.2, 4.2, 2.1, 1.9, 0.1, 0.1, 0.1, 4.1, 0.1, 0.1, 4.0, 2.1, 0.1, 0.2, 0.1, 0.1, 0.1, 0.1, 1.4, 2.1, 8.4, 8.4, 4.2, 2.1, 2.1, 1.8, 0.1, 0.1, 0.1, 2.1, 2.1, 2.1, 2.1, 6.3, 6.3, 4.2, 0.1, 2.0, 2.1, 2.1, 4.2, 2.0, 0.1, 2.1, 4.2, 2.1, 2.0, 0.1, 2.1, 2.1], 'Light_guide': [2.0, 4.1, 0.1, 4.2, 6.3, 2.1, 2.1, 0.1, 0.1, 1.9, 4.2, 2.1, 4.2, 4.2, 2.1, 2.1, 0.1, 4.1, 0.2, 0.1, 0.2, 3.7, 2.1, 2.1, 0.1, 0.1, 1.9, 2.1, 2.1, 4.2, 2.1, 2.1, 3.9, 0.1, 0.1, 0.1, 2.1, 0.1, 0.2, 0.1, 5.9, 2.1, 6.3, 2.1, 7.9, 0.1, 0.1, 0.1, 0.1, 0.1, 2.1, 2.1, 0.1, 0.1, 0.1, 0.1, 1.7, 2.1, 0.1, 2.0, 2.1, 2.1, 2.1, 2.1], 'Metal_stacker': [2.1, 2.1, 2.1, 4.2, 6.3, 4.2, 1.9, 0.1, 0.1, 2.0, 0.1, 2.1, 1.8, 0.1, 0.1, 0.1, 2.1, 2.1, 2.1, 4.2, 1.8, 0.1, 0.1, 0.1, 2.0, 0.1, 4.2, 2.1, 2.1, 4.2, 2.1, 4.2, 2.1, 2.1, 4.2, 4.2, 2.1, 4.2, 2.1, 4.2, 2.1, 4.2, 2.0, 0.1, 2.1, 2.1, 2.1, 2.1, 2.1, 2.1, 4.2, 2.1, 3.9, 0.2, 0.1], 'Adhesive_tape_check': [4.2, 10.5, 10.5, 0.1, 0.1, 14.5, 10.5, 8.4, 2.1, 2.1, 18.6, 0.1, 0.1, 0.1, 6.3, 2.1, 2.1, 4.1, 0.1, 0.1, 0.1, 0.2, 3.8, 8.4, 6.3, 8.4, 16.6, 0.1, 0.1, 10.5, 4.1, 0.1, 0.1, 0.1, 7.8, 0.1, 0.3, 5.7, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 23.1, 0.1, 6.2, 2.1, 2.1, 8.4, 0.1, 0.1, 0.1, 3.9, 0.1, 8.3, 12.6, 12.6, 12.6, 12.6, 21.0, 4.2, 6.3, 1.7, 0.1, 0.1, 0.1, 0.1, 21.0, 2.1, 18.9, 6.3, 0.1, 20.9, 4.2], 'diffuser': [2.1, 0.1, 6.2, 2.1, 6.3, 2.1, 8.1, 0.2, 0.1, 2.1, 4.2, 2.1, 2.1, 6.3, 6.3, 2.1, 4.2, 4.2, 4.2, 6.3, 6.3, 4.2, 0.1, 0.1, 0.1, 1.8, 4.2, 4.2, 4.0, 0.1, 0.1, 4.2, 4.1, 0.1, 2.1, 4.1, 0.1, 6.3, 4.2, 6.3, 4.2, 2.1, 2.1, 4.2, 0.1, 0.2, 0.1, 0.1, 0.1, 5.7, 2.1, 4.2, 2.1, 4.2, 2.1, 4.2, 10.5, 4.2]}
video_src="https://tinyurl.com/2c8hy5xm"
status="NIL"
xl=[]
l1=['Light_guide','diffuser','Adhesive_tape_check','lcd','Metal_stacker','grown_check']
for a in l1:
  print(len(dict1[a]))
  xl.append(len(dict1[a]))
xl.sort()
m=xl[-1]
video_id=0
lx=['Light_guide','diffuser','Adhesive_tape_check','lcd','Metal_stacker','grown_check']
for x in lx:
  list1=dict1[x]
  for jk in range(len(list1),m):
    list1.append(0)
  dict1[x]=list1

for i in range(m):
    l3=[]
    cycle=i+1
    k=0
    """
    while k<len(l1):
      #print(k)
      #print(l1[k])
      list1=dict1[l1[k]]
      if i<len(list1):
        l3.append(k)
      k=k+1
    
    for j in l3:
       list1=dict1[l1[j]]
       task_no=j+1
       time=list1[i]
       if time==0:
           print("red")
       if time>0:
        print("green")
      """
    ct=ct + timedelta(minutes=2)
    ts = ct.timestamp()
    for j in range(len(l1)):
        list1=dict1[l1[j]]
        task_no=j+1
        time=list1[i]
        val=(rows,cycle,task_no,time,video_src,video_id,status,ts)
        mycursor.execute(sql, val)
        mydb.commit()
        rows=rows+1
        print(mycursor.rowcount, "record inserted.")
print("successfully added")

    
        # a=jsonify(greeting=["hello", "world"],b=[1,2])
        