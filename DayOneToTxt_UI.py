import sys
import json
import io

from PyQt5.QtWidgets import *

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self._filename = '2020-01'

    def setupUI(self):
        self.setGeometry(800, 200, 400, 200)
        self.setWindowTitle("Covert DTO Json to txt v1.0")
        # 달력 입력 예제
        self.labelmonth = QLabel('바꿀 달력 입력(ex. 2020-01)', self)
        #self.labelmonth.move(20, 20)
        # 유저 달력 입력
        self.lineEdit = QLineEdit("", self)
        #self.lineEdit.move(80, 20)
        self.lineEdit.textChanged.connect(self.lineEditChanged)

        self.pushButton = QPushButton("File Open")
        self.pushButton.clicked.connect(self.pushButtonClicked)
        self.label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.labelmonth)
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.pushButton)
        layout.addWidget(self.label)

        self.setLayout(layout)

    def lineEditChanged(self):
        self._filename = self.lineEdit.text()
    def pushButtonClicked(self):
        fname = QFileDialog.getOpenFileName(self)
        # self.label.setText(fname[0])
        toName = self.makeFile(fname)
        if toName == 'NoJson':
            self.label.setText('Failed : Not Json File')
        elif toName == 'NoDayto':
            self.label.setText('Failed : Not dayone Json File')
        else:
            self.label.setText(fname[0] + ' -> ' +toName )


    def makeFile(self, tofname):
        openName = tofname[0].split('/')[-1]
        print(tofname[0].split('/'[0]))
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
        f = io.open('Journal-'+ self._filename + '.txt', 'w', encoding = 'utf8',newline='')

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
            if self._filename == Date[4:11]:
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
        return 'Journal-' + self._filename + '.txt'


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()