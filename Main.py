from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import sqlite3
import re
from robobrowser import RoboBrowser


class DecisionThread(QtCore.QThread):
    decisionsignal = QtCore.pyqtSignal(str, str)

    def __init__(self, sitedict):
        super(DecisionThread, self).__init__()
        self.sitedict = sitedict

    def run(self):
        for c, i in enumerate(self.sitedict.values()):
            decision = get_decision(i)
            self.decisionsignal.emit(list(self.sitedict.keys())[c], decision)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(50, 30, 622, 411))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.Login = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Login.sizePolicy().hasHeightForWidth())
        self.Login.setSizePolicy(sizePolicy)
        self.Login.setObjectName("Login")
        self.Login.clicked.connect(lambda: self.LoginCredShow(MainWindow))
        self.gridLayout.addWidget(self.Login, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(238, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.AddUni = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AddUni.sizePolicy().hasHeightForWidth())
        self.AddUni.setSizePolicy(sizePolicy)
        self.AddUni.setObjectName("AddUni")
        self.AddUni.clicked.connect(self.AddUniShow)
        self.gridLayout.addWidget(self.AddUni, 0, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 178, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 188, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 1, 2, 1, 1)
        self.Result = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Result.sizePolicy().hasHeightForWidth())
        self.Result.setSizePolicy(sizePolicy)
        self.Result.setObjectName("Result")
        self.Result.clicked.connect(lambda: self.StatusShow(MainWindow))
        self.gridLayout.addWidget(self.Result, 2, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(238, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 2, 1, 1, 1)
        self.Nothing = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Nothing.sizePolicy().hasHeightForWidth())
        self.Nothing.setSizePolicy(sizePolicy)
        self.Nothing.setObjectName("Nothing")
        self.Nothing.clicked.connect(lambda: self.deleteshow(MainWindow))
        self.gridLayout.addWidget(self.Nothing, 2, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 31))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Login.setText(_translate("MainWindow", "Set Login Credentials"))
        self.AddUni.setText(_translate("MainWindow", "Add Universities"))
        self.Result.setText(_translate("MainWindow", "See Result"))
        self.Nothing.setText(_translate("MainWindow", "DELETE"))

    def AddUniShow(self):
        addunidialog = QtWidgets.QDialog()
        s = AddUni()
        s.setupUi(addunidialog)
        addunidialog.exec_()

    def LoginCredShow(self, MainW):
        ud = userdata()
        if ud == []:
            logincreddialog = QtWidgets.QDialog()
            s = LoginCred()
            s.setupUi(logincreddialog)
            logincreddialog.exec_()

        else:
            email = ud[0][0]
            passw = ud[0][1]
            QtWidgets.QMessageBox.question(MainW, 'ERROR',
                                           "There's already a login credential. The email is `{}` and  the password is `{}`. If this is incorrect, press the delete button from the main window.".format(
                                               email, passw), QtWidgets.QMessageBox.Ok)

    def StatusShow(self, MainW):
        if userdata() == []:
            QtWidgets.QMessageBox.question(MainW, 'ERROR',
                                           "No User Record foud. Add login credential before checking status.",
                                           QtWidgets.QMessageBox.Ok)
        else:
            statusdialog = QtWidgets.QDialog()
            s = Status()
            s.setupUi(statusdialog)
            statusdialog.exec_()

    def deleteshow(self, MainW):
        deleteuser()
        QtWidgets.QMessageBox.question(MainW, 'DONE', 'Previous login credential deleted', QtWidgets.QMessageBox.Ok)


class AddUni(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(514, 411)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(150, 360, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.splitter = QtWidgets.QSplitter(Dialog)
        self.splitter.setGeometry(QtCore.QRect(20, 40, 361, 33))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.Email_label = QtWidgets.QLabel(self.splitter)
        self.Email_label.setObjectName("Email_label")
        self.Email_edit = QtWidgets.QLineEdit(self.splitter)
        self.Email_edit.setObjectName("Email_edit")
        self.splitter_2 = QtWidgets.QSplitter(Dialog)
        self.splitter_2.setGeometry(QtCore.QRect(20, 100, 361, 33))
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.Password_label = QtWidgets.QLabel(self.splitter_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Password_label.sizePolicy().hasHeightForWidth())
        self.Password_label.setSizePolicy(sizePolicy)
        self.Password_label.setObjectName("Password_label")
        self.Password_edit = QtWidgets.QLineEdit(self.splitter_2)
        self.Password_edit.setObjectName("Password_edit")
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(30, 150, 461, 151))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(lambda: self.addsite(Dialog))
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Email_label.setText(_translate("Dialog", "Uni Name"))
        self.Password_label.setText(_translate("Dialog", "Url"))
        self.textBrowser.setHtml(_translate("Dialog",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'Noto Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Please make sure that your URL ends with &quot;/apply/update.&quot; </p>\n"
                                            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">For example, the login page for UChicago is &quot;https://prospects.uchicago.edu/account/login.&quot;</p>\n"
                                            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"> Now, you should replace the &quot;/account/login&quot; part with &quot;/apply/update.&quot; </p>\n"
                                            "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">So, the complete URL is &quot;https://prospects.uchicago.edu/apply/update</p></body></html>"))

    def addsite(self, Dialog):
        if re.match('.+apply/update', self.Password_edit.text()) == None:
            QtWidgets.QMessageBox.question(Dialog, 'ERROR',
                                           "Your URL does not end with '/apply/update'. Please update the url with an '/apply/update' at the last",
                                           QtWidgets.QMessageBox.Ok)
        elif bool(
                self.Password_edit.text().startswith("http") or self.Password_edit.text().startswith("https")) == False:
            QtWidgets.QMessageBox.question(Dialog, 'ERROR',
                                           "Not a valid URL. Make sure your url starts with an 'http://' or 'https://.",
                                           QtWidgets.QMessageBox.Ok)
        else:
            cursor = databse_open()
            cursor.execute("INSERT INTO `LIST` VALUES (?,?) ", (self.Email_edit.text(), self.Password_edit.text()))
            cursor.connection.commit()
            cursor.connection.close()
            Dialog.accept()


class LoginCred(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.splitter = QtWidgets.QSplitter(Dialog)
        self.splitter.setGeometry(QtCore.QRect(20, 40, 361, 33))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.Email_label = QtWidgets.QLabel(self.splitter)
        self.Email_label.setObjectName("Email_label")
        self.Email_edit = QtWidgets.QLineEdit(self.splitter)
        self.Email_edit.setObjectName("Email_edit")
        self.splitter_2 = QtWidgets.QSplitter(Dialog)
        self.splitter_2.setGeometry(QtCore.QRect(10, 140, 361, 33))
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.Password_label = QtWidgets.QLabel(self.splitter_2)
        self.Password_label.setObjectName("Password_label")
        self.Password_edit = QtWidgets.QLineEdit(self.splitter_2)
        self.Password_edit.setEchoMode(QtWidgets.QLineEdit.PasswordEchoOnEdit)
        self.Password_edit.setObjectName("Password_edit")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(lambda: self.addlogin(Dialog))
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.Email_label.setText(_translate("Dialog", "Email"))
        self.Password_label.setText(_translate("Dialog", "Password"))

    def addlogin(self, Dialog):
        c = databse_open()
        c.execute('INSERT INTO `USER` VALUES (?,?)', (self.Email_edit.text(), self.Password_edit.text()))
        c.connection.commit()
        c.connection.close()
        return Dialog.accept()


class Status(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(953, 669)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(570, 580, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.splitter = QtWidgets.QSplitter(Dialog)
        self.splitter.setGeometry(QtCore.QRect(60, 80, 591, 35))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.label = QtWidgets.QLabel(self.splitter)
        self.label.setObjectName("label")
        self.NameCombo = QtWidgets.QComboBox(self.splitter)
        self.NameCombo.setObjectName("NameCombo")
        self.sitedict = sitelistasdict()
        self.sitelist = ['All']
        for i in self.sitedict.keys():
            self.sitelist.append(i)
        print(self.sitelist)
        self.NameCombo.addItems(self.sitelist)
        self.SubmitButton = QtWidgets.QPushButton(self.splitter)
        self.SubmitButton.setObjectName("SubmitButton")
        self.SubmitButton.clicked.connect(lambda: self.showresult(self.NameCombo.currentText()))

        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(50, 140, 701, 421))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Uni Name"))
        self.SubmitButton.setText(_translate("Dialog", "Submit"))

    def showresult(self, collegename):
        if collegename == "All":

            self.thread=DecisionThread(self.sitedict)
            self.thread.decisionsignal.connect(self.changetextview)
            self.thread.start()

        else:
            dec = get_decision(self.sitedict[collegename])
            self.changetextview(collegename, dec)

    def changetextview(self, site, status):
        self.textBrowser.append("College Name: {} \n Status: {} \n".format(site, status))


def initdb():
    conn = sqlite3.connect("Database.db")
    c = conn.cursor()
    c.execute("SELECT name FROM `sqlite_master` WHERE type='table'")
    s = c.fetchall()
    if ('LIST',) not in s:
        c.execute('CREATE TABLE `LIST` ( `Name` TEXT NOT NULL, `Url` TEXT NOT NULL, PRIMARY KEY(`Name`) )')
    if ('USER',) not in s:
        c.execute(
            'CREATE TABLE `USER` ( `email` TEXT NOT NULL, `password` TEXT NOT NULL, PRIMARY KEY(`email`,`password`) )')
    conn.commit()


def databse_open():
    conn = sqlite3.connect("Database.db")
    c = conn.cursor()
    return c


def userdata():
    c = databse_open()
    c.execute('SELECT * FROM `USER`')
    s = c.fetchall()
    return s


def sitelist():
    c = databse_open()
    c.execute('SELECT * FROM `LIST`')
    s = c.fetchall()
    return s


def sitelistasdict():
    list = sitelist()
    dic = {}
    for row in list:
        dic[row[0]] = row[1]
    return dic


def deleteuser():
    c = databse_open()
    c.execute('DELETE FROM `USER`')
    c.connection.commit()


def get_decision(url):
    udata = userdata()[0]
    br = RoboBrowser()
    br.open(url)
    form = br.get_form()
    form['email'] = udata[0]
    form['password'] = udata[1]
    br.submit_form(form)
    classes = []
    for clas in br.find_all('p'):
        classname = clas.get('class')
        if classname == None:
            pass
        else:
            classes.append(classname[0])

    if "error" in classes:
        return "No Update Released"
    elif "update_released" in classes:
        return "Update has been released!!!!"

    else:
        return "Unsure...either your link is incorrect or the portal is different. Please try again."


if __name__ == "__main__":
    initdb()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
