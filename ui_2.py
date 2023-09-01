# Main window of JuseKit (part 2) #
# Author: Juse
# Version: 0.7
# 该部分包括的功能：
# 绘图专区：富集气泡图

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDialog, QApplication, QMainWindow, QLabel
from PyQt5.QtCore import QUrl, QEvent, QTimer
from PyQt5.QtGui import QDesktopServices, QIcon
from ui_1 import MyApp
from plot import plot_GOem, plot_GOem_classify, read_golist, assign_go
from fasta import readfa, qc_calcu
import sys
import os
import logging
import urllib.request

class MyApp2(MyApp):

    def __init__(self):
        super().__init__()
        self.set_enrich_file.clicked.connect(lambda: self.on_button_open_file_clicked(self.enrich_file))
        self.enrich_file.installEventFilter(self)
        self.gtl_dl.clicked.connect(self.gtlfile_dl)
        self.plot_bu_2.clicked.connect(self.GOem_plot)
        self.gef_c.clicked.connect(self.GOem_anno)
        self.qc_file.installEventFilter(self)
        self.sel_qc_file.clicked.connect(lambda: self.on_button_open_file_clicked(self.qc_file))
        self.qc_running.clicked.connect(self.qc_cal)



    def gtlfile_dl(self):

        gtl_url = 'http://current.geneontology.org/ontology/go-basic.obo'
        gtl_fn = 'go_term.list'
        if os.path.exists(gtl_fn) or os.path.exists('go-basic.obo'):
            self.show_message_dialog("文件已存在，下载终止")
            return
        try:
            urllib.request.urlretrieve(gtl_url, gtl_fn)
            self.show_message_dialog("GO list file 下载完成")
        except:
            self.show_message_dialog("下载出错，请检查网络是否出错。")

    def GOem_plot(self):

        fp = self.enrich_file.toPlainText()
        if fp == '':
            self.show_message_dialog("请输入文件路径。")
            return

        xlab = self.enrich_xlab.currentText()
        ylab = self.enrich_ylab.currentText()
        if self.enrich_c.isChecked():
            num = int(self.enrich_c_num.value())
            try:
                plot_GOem_classify(file_path=fp, num=num, xlab=xlab, ylab=ylab)
            except Exception as e:
                self.show_message_dialog(f"发生错误：{e}\n请检查文件")
        else:
            num = int(self.enrich_num.value())
            try:
                plot_GOem(file_path=fp, num=num, xlab=xlab, ylab=ylab)
            except Exception as e:
                self.show_message_dialog(f"发生错误：{e}\n请检查文件")

    def GOem_anno(self):

        fp = self.enrich_file.toPlainText()
        if fp == '':
            self.show_message_dialog("请输入文件路径。")
            return

        if os.path.exists('go_term.list'):
            glfile = 'go_term.list'
        elif os.path.exists('go-basic.obo'):
            glfile = 'go-basic.obo'
        else:
            self.show_message_dialog("不存在 GO list 文件，请下载。")
            return

        golist = read_golist(glfile)
        if golist == {}:
            self.show_message_dialog("GO list 文件存在错误，请检查。")
            return

        try:
            assign_go(fp, golist)
        except Exception as e:
            self.show_message_dialog(f"发生错误：{e}\n请检查文件")
            return

        self.show_message_dialog("已完成注释，请见 GOanno.csv。")


    def qc_cal(self):

        fp = self.qc_file.toPlainText()
        op = os.path.dirname(fp)
        gene_symbol = self.gene_symbol_2.toPlainText()

        if fp == '':
            self.show_message_dialog('请输入文件路径。')
            return

        self.qc_progress.setValue(20)

        try:
            if gene_symbol == '':
                id_seq, _, longest_is = readfa(file=fp, symbol=gene_symbol, stripornot=True)
            else:
                id_seq, _, longest_is = readfa(file=fp, symbol=gene_symbol, longest=True, stripornot=True)
        except Exception as e:
            self.show_message_dialog(f'发生错误：{e}')
            logging.error("发生错误: \n%s", str(e))
            self.qc_progress.setValue(0)
            return

        self.qc_progress.setValue(50)

        try:
            all_qc_index = qc_calcu(id_seq)
        except Exception as e:
            self.show_message_dialog(f'发生错误：{e}')
            logging.error("发生错误: \n%s", str(e))
            self.qc_progress.setValue(0)
            return

        self.qc_progress.setValue(80)

        qctext = f'######################\n' \
                 f'### File: {fp}\n' \
                 f'######################\n' \
                 f'\n' \
                 f'\tNum of gene: {all_qc_index["num_gene"]}\n' \
                 f'\tMax length: {all_qc_index["max_leng"]}\n' \
                 f'\tMin length: {all_qc_index["min_leng"]}\n' \
                 f'\tAverage length: {all_qc_index["ave_leng"]}\n' \
                 f'\n' \
                 f'\tN10: {all_qc_index["N10"]}\n' \
                 f'\tN20: {all_qc_index["N20"]}\n' \
                 f'\tN30: {all_qc_index["N30"]}\n' \
                 f'\tN40: {all_qc_index["N40"]}\n' \
                 f'\tN50: {all_qc_index["N50"]}\n' \
                 f'\tGC content: {all_qc_index["GC"]}%\n\n'

        if longest_is == {}:
            with open(f'{op}/assem_qc.txt', 'w') as t:
                t.write(qctext)

            self.qc_progress.setValue(100)
            self.show_message_dialog(f'运算已完成，输出见 {op}/assem_qc.txt。')
            self.qc_progress.setValue(0)
        else:
            all_qc_index = qc_calcu(longest_is)
            self.qc_progress.setValue(90)

            qctext += f'######################\n' \
                 f'### Calculated based on longest contig\n' \
                 f'######################\n' \
                 f'\n' \
                 f'\tNum of gene: {all_qc_index["num_gene"]}\n' \
                 f'\tMax length: {all_qc_index["max_leng"]}\n' \
                 f'\tMin length: {all_qc_index["min_leng"]}\n' \
                 f'\tAverage length: {all_qc_index["ave_leng"]}\n' \
                 f'\n' \
                 f'\tN10: {all_qc_index["N10"]}\n' \
                 f'\tN20: {all_qc_index["N20"]}\n' \
                 f'\tN30: {all_qc_index["N30"]}\n' \
                 f'\tN40: {all_qc_index["N40"]}\n' \
                 f'\tN50: {all_qc_index["N50"]}\n' \
                 f'\tGC content: {all_qc_index["GC"]}%\n'

            with open(f'{op}/assem_qc.txt', 'w') as t:
                t.write(qctext)

            self.qc_progress.setValue(100)
            self.show_message_dialog(f'运算已完成，输出见 {op}/assem_qc.txt。')
            self.qc_progress.setValue(0)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MyApp2()
    main_window.setWindowIcon(QIcon('jusekit.ico'))
    main_window.show()
    sys.exit(app.exec_())
