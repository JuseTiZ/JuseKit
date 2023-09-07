# Main window of JuseKit (part 1) #
# Author: Juse
# Version: 0.8
# 该部分包括的功能：
# 组装序列提取：提取最长转录本、处理组装id、根据id提取序列
# 系统发育分析：序列串联、序列格式转换、PEP转CDS、序列过滤
# 绘图专区：火山(volcano)图
# 由于内容过多，之后更新将在 ui_2.py 进行#

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDialog, QApplication, QMainWindow, QLabel, QMenuBar
from PyQt5.QtCore import QUrl, QEvent, QTimer
from PyQt5.QtGui import QDesktopServices, QIcon
import sys
from Juse_toolkit import Ui_MainWindow
import os
from wz_ui import Wzapp
from fasta import readfa, id_modify, peptocds
from filter import fa_filter
from format_convert import *
from Study_record import LearningTimerWindow
import logging
from plot import plot_volcano

class TimedDialog(QDialog):
    def __init__(self, text, time):
        super().__init__()

        self.label = QLabel(text, self)
        self.label.adjustSize()
        self.label.move(30, 30)

        # 设置 QTimer
        self.timer = QTimer()
        self.timer.timeout.connect(self.close)
        self.timer.setSingleShot(True)
        self.timer.start(time) # 5 秒 (5000 毫秒)


class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        # 菜单栏
        self.menu_bar = self.menuBar()

        self.menu_bar.setStyleSheet("""
            QMenuBar {
                border-top: 1px ridge grey;
                border-bottom: 1px ridge grey;
                background: white;
            }
        """)

        self.file_menu = self.menu_bar.addMenu("实用小工具")


        self.wz_modify = QtWidgets.QAction(self)
        self.wz_modify.setIconText("批量改文件尾缀")
        self.wz_modify.triggered.connect(self.wz_modi)
        self.file_menu.addAction(self.wz_modify)

        self.study_rc = QtWidgets.QAction(self)
        self.study_rc.setIconText("学习计时小工具")
        self.study_rc.triggered.connect(self.open_learning_timer)
        self.file_menu.addAction(self.study_rc)

        self.file_menu.addSeparator()

        self.au_pf = QtWidgets.QAction(self)
        self.au_pf.setIconText("关于作者那些事")
        self.au_pf.triggered.connect(lambda: self.blog("https://jusetiz.github.io/myself/"))
        self.file_menu.addAction(self.au_pf)

        self.au_ms = QtWidgets.QAction(self)
        self.au_ms.setIconText("想跟作者留些言")
        self.au_ms.triggered.connect(lambda: self.blog("https://jusetiz.github.io/messageboard/"))
        self.file_menu.addAction(self.au_ms)


        self.gene_symbol_en.stateChanged.connect(self.on_checkbox_state_changed)
        self.inputfa.clicked.connect(lambda: self.on_button_open_file_clicked(self.selected_fa))
        self.le_running.clicked.connect(self.longest_exatract)
        self.clearinput.clicked.connect(self.resetle)
        self.clearinput_2.clicked.connect(self.resetle_2)
        self.prefixbutton.toggled.connect(self.update_group_box)
        self.simplybutton.toggled.connect(self.update_group_box)
        self.suffixbutton.toggled.connect(self.update_group_box)
        self.spenabutton.toggled.connect(self.update_group_box)
        self.multipc_bok.stateChanged.connect(self.on_checkbox_state_changed_2)
        self.idpc_running.clicked.connect(self.id_change)
        self.inputfa_2.clicked.connect(lambda: self.on_button_open_file_clicked(self.selected_fa_2))
        self.multipc_button.clicked.connect(lambda: self.browse_folder(self.mpc_path))
        self.sel_ali_bro_2.clicked.connect(lambda: self.browse_folder_2(label1=self.sel_ali_path, label2=self.sel_ali))
        self.sel_ali_bro.clicked.connect(lambda: self.select_mtfiles(label1=self.sel_ali_path, label2=self.sel_ali))
        self.rm_file.clicked.connect(self.clear_files)
        self.sel_ali.installEventFilter(self)
        self.modi_dir.stateChanged.connect(self.on_checkbox_state_changed_3)
        self.spe_able.stateChanged.connect(self.on_checkbox_state_changed_4)
        self.start_con.clicked.connect(self.seq_con)
        self.con_res_sel.clicked.connect(lambda: self.browse_folder(self.con_res_dir))
        self.fa_file_upload.clicked.connect(lambda: self.on_button_open_file_clicked(self.fa_file))
        self.id_file_ul.clicked.connect(lambda: self.on_button_open_file_clicked(self.id_file))
        self.clear_fl.clicked.connect(self.resetle_3)
        self.start_ex.clicked.connect(self.extract_id)
        self.cv_od_bu.clicked.connect(lambda: self.browse_folder(self.cv_out_dir))
        self.clear_cvfile.clicked.connect(self.resetle_4)
        self.sel_ali_2.installEventFilter(self)
        self.sel_ali_bro_4.clicked.connect(lambda: self.browse_folder_2(label1=self.sel_ali_path_2, label2=self.sel_ali_2))
        self.sel_ali_bro_3.clicked.connect(lambda: self.select_mtfiles(label1=self.sel_ali_path_2, label2=self.sel_ali_2))
        self.cv_running.clicked.connect(self.seq_fc)
        self.pep_input.clicked.connect(lambda: self.browse_folder(self.pep_input_text))
        self.cds_input.clicked.connect(lambda: self.on_button_open_file_clicked(self.cds_input_text))
        self.pep_op_dir_set.clicked.connect(lambda: self.browse_folder(self.pep_op_dir))
        self.ptc_running.clicked.connect(self.peptocds_button)
        self.cds_input_text.installEventFilter(self)
        self.sel_ali_bro_5.clicked.connect(lambda: self.select_mtfiles(label1=None, label2=self.sel_ali_3))
        self.filter_bu.clicked.connect(lambda: self.browse_folder(self.filter_opdir))
        self.ptc_running_2.clicked.connect(self.fafilter)
        self.sel_ali_3.installEventFilter(self)
        self.vol_file.installEventFilter(self)
        self.plot_bu_1.clicked.connect(self.vol_plot)
        self.sel_vol_file.clicked.connect(lambda: self.on_button_open_file_clicked(self.vol_file))
        logging.basicConfig(filename='error.log', level=logging.ERROR, filemode='w',
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def open_learning_timer(self):
        self.learning_timer_window = LearningTimerWindow()
        self.learning_timer_window.show()


    #拖拽文件并读取
    def eventFilter(self, source, event):

        if source in [self.sel_ali, self.sel_ali_2, self.sel_ali_3]:
            if event.type() == QEvent.DragEnter:
                if event.mimeData().hasUrls():
                    event.acceptProposedAction()
                return True

            elif event.type() == QEvent.Drop:
                urls = event.mimeData().urls()
                files = []
                for url in urls:
                    files.append(url.toLocalFile())
                    file_path = ', '.join(files)
                source.setText(file_path)
                return True

        elif source in [self.cds_input_text, self.vol_file, self.enrich_file, self.qc_file]:
            if event.type() == QEvent.DragEnter:
                if event.mimeData().hasUrls():
                    event.acceptProposedAction()
                return True

            elif event.type() == QEvent.Drop:
                urls = event.mimeData().urls()
                files = []
                for url in urls:
                    files.append(url.toLocalFile())
                if len(files) > 1:
                    self.show_message_dialog("你给的文件太多，我只能接受一个QVQ")
                    return True
                source.setText(files[0])
                return True

        return super().eventFilter(source, event)


    def clear_files(self):
        self.sel_ali_path.setText("未选择文件夹")
        self.sel_ali.setText('')
    def select_mtfiles(self, label1, label2):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        files, _ = QFileDialog.getOpenFileNames(self, "Open Files", "", "Fasta files (*.fasta *.fa *.fas);;All Files "
                                                                        "(*)", options=options)
        if files:
            label2.setText(', '.join(files))
            if label1:
                label1.setText("未选择文件夹")
        else:
            return
    def wz_modi(self):
        dialog = Wzapp(self)
        dialog.show()
    def update_group_box(self):
        if self.prefixbutton.isChecked() or self.suffixbutton.isChecked():
            self.option_add.setEnabled(True)
            self.fix_add.setEnabled(True)
            self.spenam_box.setEnabled(False)
        elif self.simplybutton.isChecked():
            self.option_add.setEnabled(False)
            self.spenam_box.setEnabled(False)
        elif self.spenabutton.isChecked():
            self.option_add.setEnabled(False)
            self.spenam_box.setEnabled(True)

    def blog(self, text):
        url = QUrl(text)
        QDesktopServices.openUrl(url)

    def resetle(self):
        self.selected_fa.setText("未选择文件")

    def resetle_2(self):
        self.selected_fa_2.setText("未选择文件")
        self.mpc_path.setText("未选择文件夹")

    def resetle_3(self):
        self.fa_file.setText("未选择文件")
        self.id_file.setText("未选择文件")

    def resetle_4(self):
        self.sel_ali_path_2.setText("未选择文件夹")

    def show_message_dialog(self, text):
        message_box = QMessageBox()
        message_box.setWindowTitle("这是一个弹窗")
        message_box.setText(text)
        message_box.setIcon(QMessageBox.Information)
        message_box.setWindowIcon(QIcon('jusekit.ico'))
        message_box.exec_()

    def on_button_open_file_clicked(self, label):
        file_name, _ = QFileDialog.getOpenFileName(None, "请选择你的文件:)", "", "All Files (*)")
        if file_name:
            # 在这里处理选定的文件，例如打印文件名
            label.setText(file_name)

    def on_checkbox_state_changed(self, state):
        if state == QtCore.Qt.Checked:
            self.gene_symbol.setEnabled(True)
        else:
            self.gene_symbol.setEnabled(False)
            self.gene_symbol.setPlainText("_i")

    def on_checkbox_state_changed_2(self, state):
        if state == QtCore.Qt.Checked:
            self.multipc_button.setEnabled(True)
            self.fire_end.setEnabled(True)
            self.inputfa_txt_2.setEnabled(False)
            self.inputfa_2.setEnabled(False)
        else:
            self.multipc_button.setEnabled(False)
            self.fire_end.setEnabled(False)
            self.inputfa_txt_2.setEnabled(True)
            self.inputfa_2.setEnabled(True)

    def on_checkbox_state_changed_3(self, state):
        if state == QtCore.Qt.Checked:
            self.con_res_dir.setEnabled(True)
            self.con_res_sel.setEnabled(True)
        else:
            self.con_res_dir.setEnabled(False)
            self.con_res_sel.setEnabled(False)

    def on_checkbox_state_changed_4(self, state):
        if state == QtCore.Qt.Checked:
            self.spe_sym.setEnabled(True)
        else:
            self.spe_sym.setEnabled(False)

    def browse_folder(self, label):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", "", options=options)
        if folder_path:
          label.setText(folder_path)

    def browse_folder_2(self, label1, label2):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", "", options=options)
        if folder_path:
            if label1:
                label1.setText(folder_path)
            text = ', '.join(os.listdir(folder_path))
            label2.setText(text)



    def longest_exatract(self):

        type_txt = True
        input_fa = self.inputfa_txt.toPlainText()
        output_name = self.opfa_name.toPlainText()
        symbol = self.gene_symbol.toPlainText()
        output_dir = './'
        if self.selected_fa.text() != '未选择文件':
            type_txt = False
            input_fa = self.selected_fa.text()
            output_dir = os.path.dirname(input_fa)
        if input_fa == '':
            self.show_message_dialog("Juse提醒您要输入fa哦")
            return
        if output_name == '':
            self.show_message_dialog("Juse提醒您没设置输出哦")
            return

        output_fa = f'{output_dir}/{output_name}'
        try:
            _, _, lc = readfa(input_fa, symbol, txt = type_txt, longest = True)
            with open(output_fa, 'w') as output:
                for gene in lc.keys():
                    output.write(">" + gene + '\n')
                    output.write(lc[gene])
            self.show_message_dialog("文件已生成")
        except Exception as e:
            self.show_message_dialog("请检查您的文件或基因标识是否有误")
            logging.error("发生错误: \n%s", str(e))
            return


    def extract_id(self):

        if self.id_file.text() != '未选择文件':
            ids = self.id_file.text()
        elif self.id_frame.toPlainText() != '':
            with open("tmp_id.txt", 'w') as txt:
                txt.write(self.id_frame.toPlainText())
            ids = "tmp_id.txt"
        else:
            self.show_message_dialog("你的id文件我没有啊:<")
            return

        if self.fa_file.text() != '未选择文件':
            fasta = self.fa_file.text()
            outputdir = os.path.dirname(fasta)
        elif self.fasta_frame.toPlainText() != '':
            with open("tmp_fasta.txt", 'w') as txt:
                txt.write(self.fasta_frame.toPlainText())
            fasta = "tmp_fasta.txt"
            outputdir = '.'
        else:
            self.show_message_dialog("id的fasta文件我没有啊:<")
            return

        filename = self.id_out_fl.toPlainText()
        if filename == '':
            self.show_message_dialog("妹有名字你让我怎么输出。")
            return

        id_seq, _, _ = readfa(file=fasta,symbol=' ')

        with open(ids, 'r') as idss:
            id_num = sum(1 for line in idss)
        id_com = 0

        try:
            with open(f'{outputdir}/{filename}', 'w') as op:
                with open(ids, 'r') as idss:
                    for line in idss:
                        id = line.strip()
                        seq = id_seq[id]
                        op.write(f'>{id}\n{seq}')
                        id_com += 1
                        self.id_progress.setValue(int(id_com/id_num*100))
        except Exception as e:
            self.show_message_dialog("id和fasta里必有一个出问题。")
            logging.error("发生错误: \n%s", str(e))
            return
        self.show_message_dialog("提取完成。")
        self.id_progress.setValue(0)

    def seq_con(self):

        align_files = self.sel_ali.toPlainText().split(', ')
        if self.sel_ali_path.text() != '未选择文件夹':
            folder_path = self.sel_ali_path.text()
            align_files = []
            for file_name in os.listdir(folder_path):
                file_path = f'{folder_path}/{file_name}'
                if os.path.isfile(file_path):
                    align_files.append(file_path)
        if align_files == ['']:
            self.show_message_dialog("你是不是尝试过所有按钮的无文件运行？")
            return
        if self.pf_able.isChecked():
            pf_able = True
        else:
            pf_able = False
        if self.log_able.isChecked():
            log_able = True
        else:
            log_able = False
        if self.modi_dir.isChecked():
            opdir = self.con_res_dir.toPlainText()
        else:
            opdir = './'
        if self.spe_able.isChecked():
            sb = self.spe_sym.toPlainText()
        else:
            sb = ' '
        try:
            self.sequence_con(aligns=align_files, symbol=sb, outputdir=opdir, pf=pf_able, log=log_able)
        except Exception as e:
            self.show_message_dialog("您的序列或标识可能有点把子问题，要不检查一下？")
            logging.error("发生错误: \n%s", str(e))
            return
        if self.open_dir.isChecked():
            QDesktopServices.openUrl(QUrl.fromLocalFile(opdir))

    def id_change(self):

        if self.prefixbutton.isChecked():
            symbol = self.fix_add.toPlainText()
            mod_used = 'pre'
        elif self.suffixbutton.isChecked():
            symbol = self.fix_add.toPlainText()
            mod_used = 'suf'
        elif self.simplybutton.isChecked():
            symbol = ''
            mod_used = 'sim'
        elif self.spenabutton.isChecked():
            symbol = self.spe_symbol.toPlainText()
            mod_used = 'spe'
        else:
            self.show_message_dialog("貌似你妹让我干任何事的想法，hum？")
            return

        if self.multipc_bok.isChecked() == False:
            input_fa = self.inputfa_txt_2.toPlainText()
            txt = True
            if self.selected_fa_2.text() != '未选择文件':
                input_fa = self.selected_fa_2.text()
                txt = False
            if input_fa == '':
                self.show_message_dialog("Juse提醒您要输入fa哦")
                return
            if symbol == '' and mod_used != 'sim':
                self.show_message_dialog("请检查你的前后缀或标识~")
                return

            if txt:
                with open('Jusekit.fa', 'w') as tmp:
                    tmp.write(input_fa)
                input_fa = 'Jusekit.fa'
            try:
                if symbol:
                    id_modify(inputfile = input_fa, string = symbol, mod = mod_used)
                else:
                    id_modify(inputfile = input_fa,  mod = mod_used)
                if self.delete_check.isChecked():
                    os.remove(input_fa)
            except Exception as e:
                self.show_message_dialog("请检查序列文件是否出错")
                logging.error("发生错误: \n%s", str(e))
                return

            self.show_message_dialog("文件已生成")

        else:

            if self.mpc_path.text() == '未选择文件夹':
                self.show_message_dialog("不选文件夹，Running要凉凉")
                return
            mp_dir = self.mpc_path.text()
            mp_files = os.listdir(mp_dir)
            if self.fire_end.toPlainText() != '':
                wz = self.fire_end.toPlainText()
                mp_files = [filename for filename in mp_files if filename.endswith(wz)]
            if mp_files == []:
                self.show_message_dialog("要么是文件夹有问题，要么是你有问题")
                return
            total_num = len(mp_files)
            compl_num = 0
            for file in mp_files:
                try:
                    if symbol:
                        id_modify(inputfile=f'{mp_dir}/{file}', string=symbol, mod=mod_used)
                    else:
                        id_modify(inputfile=f'{mp_dir}/{file}', mod=mod_used)
                    if self.delete_check.isChecked():
                        os.remove(f'{mp_dir}/{file}')
                    compl_num += 1
                    self.progressBar.setValue(int(compl_num/total_num*100))
                except Exception as e:
                    self.show_message_dialog("请检查序列文件是否出错")
                    logging.error("发生错误: \n%s", str(e))
                    return
            self.show_message_dialog("文件已生成")
            self.progressBar.setValue(0)

    def sequence_con(self, aligns, symbol, outputdir, pf=True, log=True):

        IQpartition = '#nexus\nbegin sets;\n'
        total_length = 0
        total_spe_seq = {}
        gene_spe_dic = {}
        partition_name = {}

        total_num = len(aligns)
        compl_num = 0

        aligns.sort()

        # 对当前文件夹里所有文件逐个读取
        for align in aligns:

            with open(align, 'r') as ali:

                # 初始化当前文件信息
                gene_name = os.path.basename(align)
                gene_spe = []
                tmp_len = 0
                tmp_species = []
                for line in ali:
                    if line.startswith('>') and line.strip() != '>':
                        spe_name = line.split(symbol)[0].strip()
                        gene_spe.append(spe_name[1:])
                        tmp_species.append(spe_name)

                        # 到当前比对才出现的物种之前的序列都以gap表示
                        if spe_name not in total_spe_seq.keys():
                            total_spe_seq[spe_name] = '-' * total_length

                    # 跳过空序列
                    elif line.strip() == '>' or line.strip() == '':
                        continue

                    # 将第一个序列的长度读取以作为该多序列比对的长度
                    else:
                        if len(tmp_species) == 1:
                            tmp_len += len(line.strip())

                        total_spe_seq[spe_name] += line.strip('>').strip()

                # 对不在该文件出现但在之前出现过的物种以gap作为其序列进行补充
                for spe in total_spe_seq.keys():
                    if spe not in tmp_species:
                        total_spe_seq[spe] += '-' * tmp_len
                # 记录物种信息
                gene_spe_dic[gene_name] = gene_spe
                # 添加分区信息
                charsetid = align.split('.')[0].split('/')[-1]
                if charsetid not in partition_name.keys():
                    partition_name[charsetid] = 1
                    IQpartition += f"\tcharset {charsetid}={total_length + 1}-{total_length + tmp_len};\n"
                else:
                    partition_name[charsetid] += 1
                    IQpartition += f"\tcharset {charsetid}_{partition_name[charsetid]}={total_length + 1}-" \
                                   f"{total_length + tmp_len};\n"

                total_length += tmp_len
            compl_num += 1
            self.con_progress.setValue(int(compl_num/total_num*100))
            if compl_num % 1000 == 0:
                dialog = TimedDialog(time=5000,text=f"您的序列过多，目前已处理{compl_num}条，"
                                                    f"包括{len(total_spe_seq.keys())}个物种，"
                                                    f"下一次处理将于5秒后开始...")
                dialog.exec_()

        length_set = []
        for spe in total_spe_seq.keys():
            length_set.append(len(total_spe_seq[spe]))
        if len(set(length_set)) != 1:
            message_box = QMessageBox()
            message_box.setIcon(QMessageBox.Warning)
            message_box.setText("你的序列看上去长度并不一致，至少某个出现了问题。")
            message_box.setWindowTitle("Juse Warning")
            continue_button = message_box.addButton("生成文件", QMessageBox.AcceptRole)
            cancel_button = message_box.addButton("取消退出", QMessageBox.RejectRole)
            message_box.exec_()
            if message_box.clickedButton() == continue_button:
                # 继续执行功能
                pass
            elif message_box.clickedButton() == cancel_button:
                # 退出功能
                self.con_progress.setValue(0)
                return

        total_spe_seq = dict(sorted(total_spe_seq.items()))

        if log:
            # 生成物种log
            with open(f"{outputdir}/sequence_con.log", 'w') as log:

                log.write("Species\tLength\tGap\n")
                for spe in total_spe_seq.keys():
                    gap_num = total_spe_seq[spe].count('-')
                    gap_per = round(gap_num/len(total_spe_seq[spe])*100, 1)
                    if len(total_spe_seq[spe]) == total_length:
                        log.write(f"{spe[1:]}\t{len(total_spe_seq[spe])}\t{gap_per}%\t+\n")
                    else:
                        log.write(f"{spe[1:]}\t{len(total_spe_seq[spe])}\t{gap_per}%\t-\n")

            # 生成基因log
            all_spe = set()
            for values in gene_spe_dic.values():
                all_spe.update(values)

            all_spe = sorted(all_spe)
            gene_matrix = [['Gene'] + all_spe + ['Percentage(present)']]
            spe_counts = {spe: 0 for spe in all_spe}

            for key, values in gene_spe_dic.items():
                row = [key]
                spe_checked = 0
                for spe in all_spe:
                    if spe in values:
                        row.append('')
                        spe_checked += 1
                        spe_counts[spe] += 1
                    else:
                        row.append('-')
                percentage = f"{spe_checked / len(all_spe) * 100:.2f}%"
                row.append(percentage)
                gene_matrix.append(row)

            final_row = ['Percentage']
            total_keys = len(gene_spe_dic)
            for spe in all_spe:
                percentage = f"{spe_counts[spe] / total_keys * 100:.2f}%"
                final_row.append(percentage)
            final_row.append('')
            gene_matrix.append(final_row)

            with open(f"{outputdir}/gene.log", 'w') as log:
                for row in gene_matrix:
                    log.write('\t'.join(row) + '\n')


        # 生成串联文件
        with open(f"{outputdir}/concatenation_ortho.fasta", 'w') as f:

            for spe in total_spe_seq:
                f.write(spe + '\n' + total_spe_seq[spe] + '\n')

        if pf:
        # 生成分区文件
            with open(f"{outputdir}/IQ_partition.txt", 'w') as f:

                f.write(IQpartition)
                f.write("end;")

        self.show_message_dialog("串联完成！")
        self.con_progress.setValue(0)


    def seq_fc(self):

        align_files = self.sel_ali_2.toPlainText().split(', ')
        if self.sel_ali_path_2.text() != '未选择文件夹':
            folder_path = self.sel_ali_path_2.text()
            align_files = []
            for file_name in os.listdir(folder_path):
                file_path = f'{folder_path}/{file_name}'
                if os.path.isfile(file_path):
                    align_files.append(file_path)
        if align_files == ['']:
            self.show_message_dialog("我有理由怀疑你在这里试图凑齐空运行bug。")
            return
        op_dir = self.cv_out_dir.toPlainText()
        if op_dir == '':
            self.show_message_dialog("这下不得不设置输出路径啦！")
            return

        total_num = len(align_files)
        compu_num = 0
        try:
            for af in align_files:
                id_seq_for, _, _ = readfa(af, symbol=' ',stripornot=True)

                if self.paml_box.isChecked():
                    basename = os.path.basename(af)
                    op_file = f'{op_dir}/{basename.split(".")[0]}.PML'
                    write_paml(op_file, id_seq_for)
                if self.axt_box.isChecked():
                    basename = os.path.basename(af)
                    op_file = f'{op_dir}/{basename.split(".")[0]}.axt'
                    write_axt(op_file, id_seq_for)
                if self.nex_box.isChecked():
                    basename = os.path.basename(af)
                    op_file = f'{op_dir}/{basename.split(".")[0]}.nex'
                    seqtype = check_sequence_type(id_seq_for)
                    write_nexus(op_file, id_seq_for, seqtype)
                if self.nex_int_box.isChecked():
                    basename = os.path.basename(af)
                    op_file = f'{op_dir}/{basename.split(".")[0]}.interleaved.nex'
                    seqtype = check_sequence_type(id_seq_for)
                    write_nexus_interleaved(op_file, id_seq_for, seqtype)
                if self.phy_box.isChecked():
                    basename = os.path.basename(af)
                    op_file = f'{op_dir}/{basename.split(".")[0]}.phy'
                    write_phylip(op_file, id_seq_for)
                compu_num += 1
                self.convert_progress.setValue(int(compu_num/total_num*100))
        except Exception as e:
            self.show_message_dialog("输入的文件里有不对劲的东西！")
            self.convert_progress.setValue(0)
            logging.error("发生错误: \n%s", str(e))
            return

        self.show_message_dialog("格式转换完成咯啊哈哈哈")
        self.convert_progress.setValue(0)

    def peptocds_button(self):

        cdsfile = self.cds_input_text.toPlainText()
        pepfile_dir = self.pep_input_text.toPlainText()
        output_dir = self.pep_op_dir.toPlainText()

        if cdsfile == '' or pepfile_dir == '':
            self.show_message_dialog("快给我文件，我已经迫不及待了！")
            return
        if output_dir == '':
            self.show_message_dialog("我要在哪里发泄我的输出？")
            return

        pepfiles = os.listdir(pepfile_dir)
        total_num = len(pepfiles)
        compu_num = 0
        try:
            id_seq, _, _ = readfa(file=cdsfile,symbol=' ')
            for pep in pepfiles:
                pep_path = f'{pepfile_dir}/{pep}'
                peptocds(id_seq, pep_path, output_dir)
                compu_num += 1
                self.pep_to_cds.setValue(int(compu_num/total_num*100))
            self.show_message_dialog(f"完成了，输出在{output_dir}里。")
            self.pep_to_cds.setValue(0)
        except Exception as e:
            self.show_message_dialog("是哪里出了问题呢？是哪里呢...")
            self.pep_to_cds.setValue(0)
            logging.error("发生错误: \n%s", str(e))
            return

    def fafilter(self):

        align_files = self.sel_ali_3.toPlainText().split(', ')
        output_dir = self.filter_opdir.toPlainText()
        mls = self.min_len_seq.value()
        mla = self.min_len_ali.value()
        msn = self.min_spe_num.value()
        gn = self.gap_name.toPlainText()
        ss = self.spe_sym_2.toPlainText()
        if align_files == ['']:
            self.show_message_dialog("此地无银三百两。")
            return
        if output_dir == '':
            self.show_message_dialog("我望眼欲穿，看我看不到的输出文件夹。")
            return
        if ss == '':
            ss = ' '
        if gn == '':
            gn = '-'
        total_num = len(align_files)
        compu_num = 0
        try:
            for af in align_files:
                fa_filter(af, output_dir, spesym=ss, gap=gn, min_ali_len=mla, min_seq_len=mls, min_spe_num=msn)
                compu_num += 1
                self.filter_progress.setValue(int(compu_num/total_num*100))
        except Exception as e:
            self.show_message_dialog('遇到问题序列，程序中断。')
            self.filter_progress.setValue(0)
            logging.error("发生错误: \n%s", str(e))
            return
        self.show_message_dialog("任务已完成，运行 log 可见 filter.log")
        self.filter_progress.setValue(0)

    def vol_plot(self):

        file = self.vol_file.toPlainText()
        log2fc = self.log2fc.value()
        self.vp_pro.setValue(20)
        adjp = self.adjp.value()
        upcol = self.up_color.currentText()
        downcol = self.down_color.currentText()
        self.vp_pro.setValue(50)
        labelsize = self.labelsize.value()
        axissize = self.axissize.value()
        dotsize = self.dotsize.value()
        titlesize = self.titlesize.value()
        numsize = self.numsize.value()
        self.vp_pro.setValue(100)

        try:
            plot_volcano(file, logfc_threshold=log2fc, adjp_threshold=adjp,
                         up_color=upcol, down_color=downcol,point_size=dotsize,
                         tick_size=numsize, title_size=titlesize, axis_size=axissize,
                         label_size=labelsize)
            self.vp_pro.setValue(0)
        except Exception as e:
            self.show_message_dialog(f"发生错误：{e}\n请检查文件")
            self.vp_pro.setValue(0)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MyApp()
    main_window.setWindowIcon(QIcon('jusekit.ico'))
    main_window.show()
    sys.exit(app.exec_())