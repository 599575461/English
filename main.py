# -*- coding: UTF-8 -*-
# @Time : 2023/1/10 16:06
# @Author : installation
# @Email : 599575461@qq.com
# @File : main.py
# @Project : encrypt

import logging
from English import stardict
import requests
from os import (walk, path, mkdir, listdir, unlink, getcwd, system)
import webbrowser as web
from sys import exit, argv
from ast import literal_eval
from concurrent.futures import ThreadPoolExecutor, wait, as_completed, ALL_COMPLETED
from playsound import playsound
from PyQt5.QtCore import (
    Qt,
    QCoreApplication,
    QThread,
    pyqtSignal,
)
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QMessageBox,
    QFrame,
)
from EDN import EDNCrypto
from Mainwindows import Ui_Form
import more_info_
import setting


class English:

    def __init__(self):
        self.csv = None
        self.all_task = list()
        self.len_ = int()

        self.save_path = path.join(path.expanduser('~'), "Desktop") + "\\mp3\\"
        if not path.isdir(self.save_path):
            mkdir(self.save_path)

    def start(self):
        self.csv = stardict.DictCsv("C:\\ecdict\\ecdict.csv")

    def paragraph_info(self, i):
        response = requests.get(
            f"https://tts.youdao.com/fanyivoice?word={i}&le=eng&keyfrom=speaker-target"
        ).content
        with open(self.save_path + i + ".mp3", 'wb') as code:
            code.write(response)

    def main(self, text=None, type_=None, is_words_alpha=False):
        self.len_ = len(text)
        for a in listdir(self.save_path):
            if path.splitext(a)[1] == '.mp3':
                unlink(self.save_path + a)

        if is_words_alpha:
            with open("words_alpha.txt", 'r') as f:
                text = f.read().splitlines()[0:100]

        if type_ == 'list':
            wait([
                ThreadPoolExecutor(max_workers=self.len_).submit(
                    self.paragraph_info, m) for m in text
            ],
                 return_when=ALL_COMPLETED)
        else:
            wait([
                ThreadPoolExecutor(max_workers=self.len_).submit(
                    self.paragraph_info, text)
            ],
                 return_when=ALL_COMPLETED)

    def word_dispose(self, word):
        word = self.csv.query(word)
        if word['exchange'] == '':
            return [
                word['sw'], word['phonetic'], word['definition'],
                word['translation']
            ]
        else:
            return [
                word['sw'], word['phonetic'], word['definition'],
                word['translation'],
                {
                    i[0]: i[1]
                    for i in [
                        i.split(":")
                        for i in [i for i in word['exchange'].split("/")]
                    ]
                }
            ]

    def main_idea(self, words):
        self.len_ = len(words)
        data = list()
        if isinstance(words, str):
            self.all_task = [
                ThreadPoolExecutor(max_workers=self.len_).submit(
                    self.word_dispose, words)
            ]
            self.main(is_words_alpha=False, text=words, type_='str')
        if isinstance(words, list):
            self.all_task = [
                ThreadPoolExecutor(max_workers=self.len_).submit(
                    self.word_dispose, i) for i in words
            ]
            self.main(is_words_alpha=False, text=words)
        wait(self.all_task, return_when=ALL_COMPLETED)
        for future in as_completed(self.all_task):
            data.append(future.result())
        return data


# 选择文件
def file_search(function):

    def search(self):
        filename, filetype = QFileDialog.getOpenFileName(
            self, "选取文件", getcwd(),
            "Text Files(*.txt *.py *.json *.xml);;Image Files(*.png *.jpg *.ico *.icon)"
        )
        function(self, filename, filetype)

    return search


class MoreInfo(QDialog, more_info_.Ui_Dialog):

    def __init__(self):
        super(MoreInfo, self).__init__()
        self.window_point = None
        self.start_point = None
        self.is_moving = None
        self.setupUi(self)

        # 最小按钮
        self.small.clicked.connect(self.showMinimized)
        # 最大化按钮
        self.Max.clicked.connect(self.max_normal)
        # 退出按钮
        self.exit.clicked.connect(self.query_exit)
        # 设置无边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(self.width(), self.height())

    # 弹出警告提示窗口确认是否要关闭
    def query_exit(self):
        self.close()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.is_moving = True
            self.start_point = e.globalPos()
            self.window_point = self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self.is_moving:
            repos = e.globalPos() - self.start_point  # QPoint 类型可以直接相减
            self.move(self.window_point + repos)

    def mouseReleaseEvent(self, e):
        self.is_moving = False

    # 切换最大化与正常大小
    def max_normal(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def start_(self, word):
        self.ing.clear()
        self.est.clear()
        self.er.clear()
        self.es.clear()
        self.s.clear()
        self.ed.clear()
        self.ed_.clear()

        for words in e_.main_idea(word):
            if len(word) > 4:
                for key, var in words[4].items():
                    if key == 's':
                        self.s.setText(var)
                        self.s.setTextInteractionFlags(
                            Qt.TextSelectableByMouse)
                    if key == 'i':
                        self.ing.setText(var)
                        self.ing.setTextInteractionFlags(
                            Qt.TextSelectableByMouse)
                    if key == 'd':
                        self.ed.setText(var)
                        self.ed.setTextInteractionFlags(
                            Qt.TextSelectableByMouse)
                    if key == '3':
                        self.es.setText(var)
                        self.es.setTextInteractionFlags(
                            Qt.TextSelectableByMouse)
                    if key == 'p':
                        self.ed_.setText(var)
                        self.ed_.setTextInteractionFlags(
                            Qt.TextSelectableByMouse)
                    if key == 't':
                        self.er.setText(var)
                        self.er.setTextInteractionFlags(
                            Qt.TextSelectableByMouse)
                    if key == 'r':
                        self.est.setText(var)
                        self.est.setTextInteractionFlags(
                            Qt.TextSelectableByMouse)
            self.textBrowser.setText(words[2])


class Settings(setting.Ui_Dialog, QDialog):

    def __init__(self):
        super(Settings, self).__init__()
        self.window_point, self.start_point, self.is_moving = None, None, None
        self.setupUi(self)
        # 最小按钮
        self.small.clicked.connect(self.showMinimized)
        # 最大化按钮
        self.Max.clicked.connect(self.max_normal)
        # 退出按钮
        self.exit.clicked.connect(self.query_exit)
        # 设置无边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setFixedSize(self.width(), self.height())

    # 弹出警告提示窗口确认是否要关闭
    def query_exit(self):
        print(self.fontComboBox.currentFont())
        self.close()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.is_moving = True
            self.start_point = e.globalPos()
            self.window_point = self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self.is_moving:
            repos = e.globalPos() - self.start_point  # QPoint 类型可以直接相减
            self.move(self.window_point + repos)

    def mouseReleaseEvent(self, e):
        self.is_moving = False

    # 切换最大化与正常大小
    def max_normal(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()


class Mian(QFrame, Ui_Form):

    def __init__(self):
        # 继承并且定义变量
        super(Mian, self).__init__()
        self._word = None
        self.window_point = None
        self.start_point = None
        self.is_moving = False
        self.word__number = 0
        self.word__ = None
        self.music_ = None
        # UI设置
        self.setupUi(self)
        # 最小按钮
        self.small.clicked.connect(self.showMinimized)
        # 最大化按钮
        self.Max.clicked.connect(self.max_normal)
        # 退出按钮
        self.exit.clicked.connect(self.query_exit)
        # 设置无边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 定义信号槽

        # start按钮
        self.start.clicked.connect(self.start_work)
        # 选择文件窗口->加密
        self.file_search_en.clicked.connect(self.file_search_en_)
        # 选择文件窗口->解密
        self.file_search_dn.clicked.connect(self.file_search_dn_)
        # 设置按钮
        self.set.clicked.connect(self.start_set)
        # 详细信息
        self.Details.clicked.connect(self.more_info)
        # 输入
        self.start_Custom.clicked.connect(self.start_com)
        # music
        self.sound.clicked.connect(self.music)
        # next按钮
        self.next.clicked.connect(self.word_)
        self.next_.clicked.connect(self.word_)
        # last按钮
        self.last.clicked.connect(lambda: self.word_(mode=True))
        self.last_.clicked.connect(lambda: self.word_(mode=True))

        self.Details.setVisible(False)
        self.youdao.setVisible(False)
        self.love_english.setVisible(False)

        self.setFixedSize(self.width(), self.height())

    def music(self):
        _path = path.join(path.expanduser('~'),
                          "Desktop") + "\\mp3\\" + self.word__ + '.mp3'

        self.music_ = Music(_path)
        self.music_.start()

    def start_com(self):
        self.word__ = self.Custom_words.text()
        self.word_()

    def more_info(self):
        more_inf.start_(self.word__)
        more_inf.show()

    def word_(self, word___=None, mode=False, first=False):
        if mode:
            self.word__number -= 2
        if first:
            self.word__ = 'object'
            self._word = word___
        else:
            self.word__ = self._word[self.word__number]
        # 有道
        self.youdao.clicked.connect(lambda: web.open(
            f"https://dict.youdao.com/result?word={self.word__}&lang=en"))
        # 爱词霸
        self.love_english.clicked.connect(
            lambda: web.open(f"https://www.iciba.com/word?w={self.word__}"))
        try:
            try:
                self.textBrowser.clear()
                for i in e_.main_idea(self.word__):
                    self.textBrowser.append("<strong>单词:</strong>" + i[0])
                    self.textBrowser.append("<strong>音标:</strong>" + i[1])
                    self.textBrowser.append("<strong>解释:</strong>" + i[3])
                    break
                self.english_words.setText(self.word__)

                self.Details.setVisible(True)
                self.youdao.setVisible(True)
                self.love_english.setVisible(True)

                self.more_info()
                self.word__number += 1
            except TypeError:
                QMessageBox.information(self, '出现错误', f'词库损失:{self.word__}')
                self.word__number += 1
        except AttributeError:
            QMessageBox.information(self, '请稍等', '正在初始化词库')
        except TypeError:
            QMessageBox.information(self, '请稍等', '正在初始化词库')
        except IndexError:
            self.word__number = 0

    @staticmethod
    def start_set():
        setting.show()

    # 开始工作
    def start_work(self):

        dn_text_finish = None
        # 获取要加密的信息
        en_text = self.en_text.text()
        # 获得要解密的信息
        dn_text = self.dn_text.text()

        # 获得是否写入log
        is_log = self.write_log.isChecked()
        # 获得阿会否覆盖文件
        is_over = self.Over_write_file.isChecked()

        # 如果说两个输入框都是空的
        if en_text == "" and dn_text == "":
            QMessageBox.question(self, '没有内容', "您未输入任何字符\n您可以输入 /文件/文本/目录")
        elif en_text != "" and dn_text != "":
            QMessageBox.question(self, '不能同时进行', "不能同时进行加密和解密")
        elif len(en_text) >= 1000 or len(dn_text) >= 1000:
            QMessageBox.question(self, '太长', "文本过于长\n建议写入txt文件")
        else:
            # 实例化密码系统
            e = EDNCrypto()
            # 提示消息
            message = ''
            # 获得的文本信息
            text = ''
            # 如果加密的框不是空的
            if en_text != "":
                # 如果输入的是文件
                if path.isfile(en_text):
                    # 读取文件
                    try:
                        with open(en_text, 'r', encoding='UTF-8') as f:
                            # 将获得信息进行加密
                            text = f.read()
                            en_text_finish = str(e.en(text))
                    except FileNotFoundError:
                        message += '未找到文件\n'
                    else:
                        message += '成功加密\n'
                        # 将浏览文本的窗口设置加密文本
                        self.finish_text.setText(en_text_finish)
                        # 如果要覆盖文件
                        if is_over:
                            # 写的模式打开
                            with open(en_text, 'w', encoding='UTF-8') as f:
                                # 写入加密的文本
                                f.write(en_text_finish)
                            # message添加成功信息
                            message += '成功替换文本\n'
                        # 如果要写log
                        if is_log:
                            # 调用写入log_info的函数
                            self.log(f"用户加密{text},结果为{en_text_finish}")
                            # message添加成功信息
                            message += '成功写入日志\n'
                # 如果输入的是目录
                elif path.isdir(en_text):
                    # 遍历目录下所有文件
                    for filepath, dir_names, filenames in walk(en_text):
                        for filename in filenames:
                            # 拼接文件名和路径
                            _path = path.join(filepath, filename)
                            # 分别打开文件
                            with open(_path, 'w', encoding='UTF-8') as f:
                                # 写入加密信息
                                f.write(e.en(text))
                            # message添加成功信息
                            message += f'已将{_path}加密\n'

                # 如果是纯文本
                else:
                    # 设置已经加密好的信息
                    en_text_finish = str(e.en(en_text))
                    # 将浏览文本的窗口设置加密文本
                    self.finish_text.setText(en_text_finish)
                    # message添加成功信息
                    message += '加密文本成功\n'
                    # 如果要写log
                    if is_log:
                        # 调用写入log_info的函数
                        self.log(f"用户加密{en_text},结果为{en_text_finish}")
                        # message添加成功信息
                        message += '成功写入日志\n'
            # 如果解密的框不是空的
            if dn_text != "":
                # 如果输入的是文件
                if path.isfile(dn_text):
                    try:
                        with open(dn_text, 'r', encoding='UTF-8') as f:
                            # 将获得信息进行解密
                            text = f.read()
                    except ValueError:
                        message += '输入格式不正确\n'
                    # 将浏览文本的窗口设置解密文本
                    else:
                        self.finish_text.setText(dn_text_finish)
                    # 如果要覆盖文件
                    if is_over:
                        # 写的模式打开
                        try:
                            with open(dn_text, 'w', encoding='UTF-8') as f:
                                # 写入解密的文本
                                f.write(dn_text_finish)
                        except ValueError:
                            message += '输入格式不正确\n'
                        # message添加成功信息
                        else:
                            message += '成功替换文本\n'
                    # 如果要写log
                    if is_log:
                        # 调用写入log_info的函数
                        self.log(f"用户解密{text},结果为{dn_text_finish}")
                        # message添加成功信息
                        message += '成功写入日志\n'
                # 如果输入的是目录
                elif path.isdir(dn_text):
                    for filepath, dir_names, filenames in walk(dn_text):
                        for filename in filenames:
                            # 拼接文件名和路径
                            _path = path.join(filepath, filename)
                            # 分别打开文件
                            with open(_path, 'w', encoding='UTF-8') as f:
                                # 写入解密信息
                                f.write(e.dn(literal_eval(text)))
                            # message添加成功信息
                            message += f'已将{_path}解密\n'
                # 如果是纯文本
                else:
                    # 设置已经解密好的信息
                    try:
                        dn_text_finish = str(e.dn(literal_eval(dn_text)))
                    except ValueError:
                        message += '输入格式不正确\n'
                    except TypeError:
                        message += '输入格式不正确\n'
                    else:
                        # 将浏览文本的窗口设置解密文本
                        self.finish_text.setText(dn_text_finish)
                        # message添加成功信息
                        message += '加密文本成功\n'
                    # 如果要写log
                    if is_log:
                        # 调用写入log_info的函数
                        self.log(f"用户解密{dn_text},结果为{dn_text_finish}")
                        # message添加成功信息
                        message += '成功写入日志\n'
            # 弹出窗口提示
            QMessageBox.information(self, '信息', message)

    @staticmethod
    def log(text):
        logging.basicConfig(
            filename='log.log',
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO,
            encoding='UTF-8')
        logging.info(text)

    @file_search
    def file_search_en_(self, filename, filetype):
        self.en_text.setText(filename)
        self.start_work()

    @file_search
    def file_search_dn_(self, filename, filetype):
        self.dn_text.setText(filename)
        self.start_work()

    # 切换最大化与正常大小
    def max_normal(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    # 弹出警告提示窗口确认是否要关闭
    def query_exit(self):
        if QMessageBox.question(self, "退出?", "你确认要退出码?", QMessageBox.Yes
                                | QMessageBox.Cancel) == QMessageBox.Yes:
            QCoreApplication.instance().exit()

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.is_moving = True
            self.start_point = e.globalPos()
            self.window_point = self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        if self.is_moving:
            repos = e.globalPos() - self.start_point  # QPoint 类型可以直接相减
            self.move(self.window_point + repos)

    def mouseReleaseEvent(self, e):
        self.is_moving = False


# class Bar(bar.Ui_Dialog, QDialog):
#     def __init__(self):
#         super(Bar, self).__init__()
#         self.setupUi(self)


def bar__(word):
    QMessageBox.information(None, '成功!', '词典初始化成功')
    print(word)
    Windows.word_(word___=word, first=True)


class BarThread(QThread):
    text = pyqtSignal(list)

    def run(self):
        with open("Oipids/words_alpha.txt", 'r') as w:
            a = w.read()
        if not path.isfile("C:\\ecdict\\ecdict.csv"):
            system("7z.exe x ecdict.7z -p599575461 -oC:/ecdict/ -y")
        e_.start()
        self.text.emit(a.split('\n'))


class Music(QThread):

    def __init__(self, path__):
        QThread.__init__(self)
        self.path = path__

    def run(self):
        playsound(self.path)


if __name__ == '__main__':
    app = QApplication(argv)
    app.processEvents()
    setting = Settings()
    more_inf = MoreInfo()
    # 全局读取CSV
    e_ = English()

    update_thread = BarThread()
    update_thread.start()
    update_thread.text.connect(bar__)

    Windows = Mian()
    Windows.show()

    exit(app.exec_())
