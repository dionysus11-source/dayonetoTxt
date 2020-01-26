#!/usr/bin/env python
# coding: utf-8

# In[6]:


from flask import Flask, render_template, request, send_file
from flask import redirect
from werkzeug.utils import secure_filename
import sys
import json
import io
import getMagnet
app = Flask(__name__)


# In[7]:


@app.route('/upload')
def render_file():
    return render_template('upload.html')


# In[ ]:



# In[8]:
def makeFile(openName, calendar):

    if openName.split('.')[1] != 'json':              # not json file
        return 'NoJson'

    with open(openName, encoding='UTF8') as st_json:
        st_python = json.load(st_json)
    if not 'entries' in st_python:
        return 'NoDayto'
    obj = st_python.get('entries')
    obj.reverse()
    # filename = '2020-01'

    #f = open(self._filename + '.txt', 'w')
    # f = io.open(self._filename + '.txt', 'w', newline='')
    f = io.open('Journal-'+ calendar + '.txt', 'w', encoding = 'utf8',newline='')

    for journal in obj:
        Date = str(journal['creationDate'])
        seoulTime = int(str(journal['creationDate'])[11:13]) + 9
        if seoulTime >= 24:
            seoulTime -= 24
            changeDate = int(journal['creationDate'][8:10]) + 1
            if changeDate < 10:
                changeDate = '0' + str(changeDate)
            else:
                changeDate = str(changeDate)
        else:
            changeDate = journal['creationDate'][8:10]
        if seoulTime < 10:
            seoulTime = '0' + str(seoulTime)
        Date = Date[:8] + str(changeDate) + ' ' + str(seoulTime) + Date[13:19]
        Date = '### ' + Date + '\n'
        if calendar == Date[4:11]:
            Text = journal['text']
            removeImage = Text.split('\n\n')
            tt = removeImage[0] + '\n'
            # print(tt)
            latitude = str(journal['location']['latitude'])
            longitude = ',%20' + str(journal['location']['longitude']) + '\n\n'
            googleUrl = 'https://maps.google.com/?q=' + latitude + longitude
            # print(googleUrl)
            Data = Date + tt + googleUrl
            # print(Data)
            f.write(Data)
    f.close()
    return 'success'

@app.route('/fileUpload', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        calendar = request.form['calendar']
        f.save(secure_filename(f.filename))
        ret = makeFile(f.filename, calendar)
        if ret == 'NoJson':
            return 'Failed : Not Json File'
        elif ret == 'NoDayto':
            return 'Failed : Not dayone Json File'
        else:
            return send_file('/Journal-'+ calendar+ '.txt', mimetype=None, attachment_filename=calendar+ '.txt',# 다운받아지는 파일 이름. 
                      as_attachment=True)
            #return 'success'
        
@app.route('/test/<userName>', methods=['GET','POST'])
def test(userName):
    if request.method == 'GET':
        return 'success ' + userName

# In[9]:
@app.route('/torrentSaturday')
def gettorrentSaturday():
    # return 'http://www.naver.com'
    # return redirect("http://www.example.com", code=302)
    return redirect(getMagnet.getSaturdaySong(), code=302)

if __name__ == '__main__':
    app.run(host='192.168.1.81', port='5000', debug = True)
    # app.run()

