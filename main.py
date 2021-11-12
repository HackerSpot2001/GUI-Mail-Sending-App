#!/usr/bin/python3
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QLineEdit,QMainWindow, QMessageBox, QPushButton, QTextEdit
from PyQt5.uic import loadUi
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from smtplib import SMTP, SMTPAuthenticationError
import sys


class UIWindow(QMainWindow):
    def __init__(self):
        super(UIWindow,self).__init__()
        loadUi("main.ui",self)
        self.setMaximumSize(800,729)
        self.setMinimumSize(800,729)

        self.email = self.findChild(QLineEdit,"lineEdit")
        self.password = self.findChild(QLineEdit,"lineEdit_2")
        self.smtpServer = self.findChild(QLineEdit,"lineEdit_3")
        self.port = self.findChild(QLineEdit,"lineEdit_4")
        self.loginBtn = self.findChild(QPushButton,"pushButton")
        self.loginBtn.clicked.connect(self.loginTOMail)

        self.to = self.findChild(QLineEdit,"lineEdit_5")
        self.subject = self.findChild(QLineEdit,"lineEdit_6")
        self.mailText = self.findChild(QTextEdit,"textEdit")
        self.attachment = self.findChild(QPushButton,"pushButton_2")
        self.attachment.clicked.connect(self.addAttachment)
        self.attachName = self.findChild(QLabel,"label")
        self.attachName.setText("Attachment:")
        self.sendBtn = self.findChild(QPushButton,"pushButton_3")
        self.sendBtn.clicked.connect(self.sendMail)
    
    def loginTOMail(self):
        try:
            if (str(self.email.text()) is not None) or (str(self.password.text()) is not None)  or (str(self.smtpServer.text()) is not None) or (str(self.port.text()) is not None):
                self.server = SMTP(str(self.smtpServer.text()),int(self.port.text()))
                self.server.ehlo()
                self.server.starttls()
                self.server.ehlo()
                self.server.login(str(self.email.text()),str(self.password.text()))
                self.email.setEnabled(False)
                self.password.setEnabled(False)
                self.smtpServer.setEnabled(False)
                self.port.setEnabled(False)
                self.loginBtn.setEnabled(False)
                self.to.setEnabled(True)
                self.subject.setEnabled(True)
                self.mailText.setEnabled(True)
                self.attachment.setEnabled(True)
                self.sendBtn.setEnabled(True)
                self.message_box = QMessageBox()
                self.message_box.setText("Login Success.")
                self.message_box.exec_()

                self.msg = MIMEMultipart()


        except SMTPAuthenticationError:
            self.message_box = QMessageBox()
            self.message_box.setText("Invaild Login Credentials.")
            self.message_box.exec_()

        except:
            self.message_box = QMessageBox()
            self.message_box.setText("Login Failed.")
            self.message_box.exec_()
            

    def addAttachment(self):
        options = QFileDialog.Options()
        fileNames, _ = QFileDialog.getOpenFileNames(self,"Open File","","All Files(*.*)",options=options)
        if fileNames != []:
            for fileName in fileNames:
                attachment = open(fileName,"rb")
                fileName = fileName[fileName.rfind("/") + 1:]
                p = MIMEBase("application","octet-stream")
                p.set_payload(attachment.read())
                encoders.encode_base64(p)
                p.add_header("Content-Disposition",f"attachment: filename={fileName}")
                self.msg.attach(p)
                self.attachName.setText(self.attachName.text()+"  "+fileName)
                 

    def sendMail(self):
        if (str(self.to.text()) is  None) or (str(self.mailText.toPlainText()) is  None) or (str(self.subject.text()) is  None):
            QMessageBox(self,"Warning..","Please Fill all fields.").exec()
        
        else:
            dialog = QMessageBox()
            dialog.setText("Do you want to send Mail?")
            dialog.addButton(QPushButton("Yes"),QMessageBox.YesRole)
            dialog.addButton(QPushButton("No"),QMessageBox.NoRole)

            if dialog.exec_() == 0:
                try:
                    self.msg['From'] = "Abhishek Sagar"
                    self.msg["To"] = self.to.text()
                    self.msg['Subject'] = self.subject.text()
                    self.msg.attach(MIMEText(self.mailText.toPlainText(),"plain"))
                    text = self.msg.as_string()
                    self.server.sendmail(self.email.text(),self.to.text(),text)
                    self.message_box = QMessageBox()
                    self.message_box.setText("Mail Send Successfully.")
                    self.message_box.exec_()

                except:
                    self.message_box = QMessageBox()
                    self.message_box.setText("Mail Sending Failed!")
                    self.message_box.exec_()

                self.to.setText("")
                self.subject.setText("")
                self.mailText.setText("")
                self.attachName.setText("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UIWindow()
    window.show()
    sys.exit(app.exec_())