import sys
import os
import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import pytz
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
import concurrent.futures
from Controller.ytbViewer import ytbViewer

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(int(1202 * 2/3), int(770 * 2/3))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setObjectName("frame")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName("gridLayout")

        self.groupBox = QtWidgets.QGroupBox(self.frame)
        self.groupBox.setObjectName("groupBox")

        self.groupBoxLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.groupBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.groupBoxLayout.setSpacing(0) 

        self.scrollArea = QtWidgets.QScrollArea(self.groupBox)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.groupBoxLayout.addWidget(self.scrollArea)

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")

        self.tableWidget = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(7)
        self._set_table_headers()

        self.verticalLayout.addWidget(self.tableWidget)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 2)

        self.label = QtWidgets.QLabel(self.frame)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit = QtWidgets.QLineEdit(self.frame)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.spinBox = QtWidgets.QSpinBox(self.frame)
        self.spinBox.setObjectName("spinBox")
        self.gridLayout.addWidget(self.spinBox, 2, 1, 1, 1)

        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.spinBox_2 = QtWidgets.QSpinBox(self.frame)
        self.spinBox_2.setObjectName("spinBox_2")
        self.gridLayout.addWidget(self.spinBox_2, 3, 1, 1, 1)

        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 4, 0, 1, 1)

        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 4, 1, 1, 1)

        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 5, 0, 1, 2)

        MainWindow.setCentralWidget(self.frame)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton.clicked.connect(self.stop_button_clicked)
        self.pushButton_2.clicked.connect(self.start_button_clicked)
        self.pushButton_3.clicked.connect(self.pause_button_clicked)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._update_table)

    def stop_button_clicked(self):
        print("Nút Stop được nhấn")
        self.timer.stop()
        self.executor.shutdown(wait=True)

    def start_button_clicked(self):
        search_query = self.lineEdit.text()
        num_threads = self.spinBox.value()
        self.time_interval = self.spinBox_2.value()

        if num_threads <= 0:
            print("Số lượng luồng phải lớn hơn 0.")
            return

        self._initialize_table(num_threads)

        self.start_time = datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
        self.timer.start(1000)

        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=num_threads)
        self.futures = [self.executor.submit(self.run_task, search_query, i) for i in range(num_threads)]

    def run_task(self, search_query, index):
        auto = ytbViewer()
        auto.OpenYtb(search_query)

        start_time = self.start_time + datetime.timedelta(seconds=index * self.time_interval)
        time_run = 60  
        end_time = start_time + datetime.timedelta(seconds=time_run)

        def get_vietnam_time():
            vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
            return datetime.datetime.now(vietnam_tz)
        
        while datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh')) < end_time:
            current_time = get_vietnam_time()
            elapsed_time = (current_time - start_time).total_seconds()
            progress = (elapsed_time / time_run) * 100  
            self.update_progress(index, progress)
            if progress >= 100:
                break
            time.sleep(0.1)  
  
    def pause_button_clicked(self):
        print("Nút Pause được nhấn")
        self.timer.stop()
        self.executor.shutdown(wait=True)

    def _set_table_headers(self):
        _translate = QtCore.QCoreApplication.translate
        self.tableWidget.setHorizontalHeaderLabels([
            _translate("MainWindow", "Thời gian bắt đầu"),
            _translate("MainWindow", "Thời gian chạy "),
            _translate("MainWindow", "Thời gian kết thúc"),
            _translate("MainWindow", "Tiến độ"),
            _translate("MainWindow", "Lượt xem hiện tại")
        ])
        for i in range(7):
            item = QtWidgets.QTableWidgetItem()
            item.setText(_translate("MainWindow", f"Người dùng {i + 1}"))
            self.tableWidget.setVerticalHeaderItem(i, item)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Nhóm"))
        self.label.setText(_translate("MainWindow", "Tên video:"))
        self.label_2.setText(_translate("MainWindow", "Số lượt xem:"))
        self.label_3.setText(_translate("MainWindow", "Khoảng thời gian chạy (giây)"))
        self.pushButton.setText(_translate("MainWindow", "Dừng"))
        self.pushButton_2.setText(_translate("MainWindow", "Bắt đầu"))
        self.pushButton_3.setText(_translate("MainWindow", "Tạm dừng"))

    def _initialize_table(self, num_rows):
        self.tableWidget.setRowCount(num_rows)
        for i in range(num_rows):
            self.tableWidget.setVerticalHeaderItem(i, QtWidgets.QTableWidgetItem(f"Người dùng {i + 1}"))

    def _update_table(self):
        current_time = datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
        time_run = 60 
        for row in range(self.tableWidget.rowCount()):
            start_time = self.start_time + datetime.timedelta(seconds=row * self.time_interval)
            end_time = start_time + datetime.timedelta(seconds=time_run)
            time_start_str = start_time.strftime("%H:%M:%S")
            time_end_str = end_time.strftime("%H:%M:%S")    
            elapsed_time = 60
            process_percentage = (elapsed_time / time_run) * 100
            data = [
                time_start_str,
                str(datetime.timedelta(seconds=min(elapsed_time, time_run))),
                time_end_str,
                f"{min(process_percentage, 100):.2f} %",
                "0"
            ]
            for column, cellData in enumerate(data):
                item = QtWidgets.QTableWidgetItem(cellData)
                self.tableWidget.setItem(row, column, item)

    def update_progress(self, index, progress):
        item = self.tableWidget.item(index, 3)  
        if item:
            item.setText(f"{progress:.2f} %")
        else:
            self.tableWidget.setItem(index, 3, QtWidgets.QTableWidgetItem(f"{progress:.2f} %"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
