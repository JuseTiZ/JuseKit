import os
import logging
import urllib.request
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QDialog, QLabel
from utils.fasta import *
from utils.filter import *
from utils.format_convert import *
from utils.plot import *

#%% 缓冲时间
"""
缓冲时间窗口
"""
class TimedDialog(QDialog):
    def __init__(app, text, time):
        super().__init__()
        app.label = QLabel(text, app)
        app.label.adjustSize()
        app.label.move(30, 30)
        # 设置 QTimer
        app.timer = QTimer()
        app.timer.timeout.connect(app.close)
        app.timer.setSingleShot(True)
        app.timer.start(time) # 5 秒 (5000 毫秒)


#%% 日志记录
"""
日志
"""
logging.basicConfig(filename='error.log', level=logging.ERROR, filemode='w',
                    format='%(asctime)s - %(levelname)s - %(message)s')


#%% 窗口功能
"""
弹出包含特定消息的窗口
"""
def show_message_dialog(text):
    message_box = QMessageBox()
    message_box.setWindowTitle("这是一个弹窗")
    message_box.setText(text)
    message_box.setIcon(QMessageBox.Information)
    message_box.exec_()


#%% 内容操作
"""
修改检查框状态
"""
def on_checkbox_state_changed(app, state):
    if state == QtCore.Qt.Checked:
        app.gene_symbol.setEnabled(True)
    else:
        app.gene_symbol.setEnabled(False)
        app.gene_symbol.setPlainText("_i")

def on_checkbox_state_changed_2(app, state):
    if state == QtCore.Qt.Checked:
        app.multipc_button.setEnabled(True)
        app.fire_end.setEnabled(True)
        app.inputfa_txt_2.setEnabled(False)
        app.inputfa_2.setEnabled(False)
    else:
        app.multipc_button.setEnabled(False)
        app.fire_end.setEnabled(False)
        app.inputfa_txt_2.setEnabled(True)
        app.inputfa_2.setEnabled(True)

def on_checkbox_state_changed_3(app, state):
    if state == QtCore.Qt.Checked:
        app.con_res_dir.setEnabled(True)
        app.con_res_sel.setEnabled(True)
    else:
        app.con_res_dir.setEnabled(False)
        app.con_res_sel.setEnabled(False)

def on_checkbox_state_changed_4(app, state):
    if state == QtCore.Qt.Checked:
        app.spe_sym.setEnabled(True)
    else:
        app.spe_sym.setEnabled(False)


"""
选择文件
"""
def on_button_open_file_clicked(label):
    file_name, _ = QFileDialog.getOpenFileName(None, "请选择你的文件:)", "", "All Files (*)")
    if file_name:
        # 在这里处理选定的文件，例如打印文件名
        label.setText(file_name)


"""
重置文件
"""
def resetle_1(app):
    app.selected_fa.setText("未选择文件")

def resetle_2(app):
    app.selected_fa_2.setText("未选择文件")
    app.mpc_path.setText("未选择文件夹")

def resetle_3(app):
    app.fa_file.setText("未选择文件")
    app.id_file.setText("未选择文件")

def resetle_4(app):
    app.sel_ali_path_2.setText("未选择文件夹")

"""
一键勾选（更新）box
"""
def update_group_box(app):
    if app.prefixbutton.isChecked() or app.suffixbutton.isChecked():
        app.option_add.setEnabled(True)
        app.fix_add.setEnabled(True)
        app.spenam_box.setEnabled(False)
    elif app.simplybutton.isChecked():
        app.option_add.setEnabled(False)
        app.spenam_box.setEnabled(False)
    elif app.spenabutton.isChecked():
        app.option_add.setEnabled(False)
        app.spenam_box.setEnabled(True)

"""
选择文件夹或文件夹里的所有序列
"""
def browse_folder_1(app, label):
    options = QFileDialog.Options()
    options |= QFileDialog.ShowDirsOnly
    folder_path = QFileDialog.getExistingDirectory(app, "Select Folder", "", options=options)
    if folder_path:
        label.setText(folder_path)

def browse_folder_2(app, label1, label2):
    options = QFileDialog.Options()
    options |= QFileDialog.ShowDirsOnly
    folder_path = QFileDialog.getExistingDirectory(app, "Select Folder", "", options=options)
    if folder_path:
        if label1:
            label1.setText(folder_path)
        text = ', '.join(os.listdir(folder_path))
        label2.setText(text)


"""
清除文件夹
"""
def clear_files(app):
    app.sel_ali_path.setText("未选择文件夹")
    app.sel_ali.setText('')


"""
选择多个文件
"""
def select_mtfiles(app, label1, label2):
    options = QFileDialog.Options()
    options |= QFileDialog.ReadOnly
    files, _ = QFileDialog.getOpenFileNames(app, "Open Files", "", "Fasta files (*.fasta *.fa *.fas);;All Files "
                                                                    "(*)", options=options)
    if files:
        label2.setText(', '.join(files))
        if label1:
            label1.setText("未选择文件夹")
    else:
        return
"""
打开博客指定页面
"""
def blog(text):
    url = QUrl(text)
    QDesktopServices.openUrl(url)

#%% 模块功能 (序列处理)
"""
提取最长序列
"""
def longest_exatract(app):

    type_txt = True
    input_fa = app.inputfa_txt.toPlainText()
    output_name = app.opfa_name.toPlainText()
    symbol = app.gene_symbol.toPlainText()
    output_dir = './'
    if app.selected_fa.text() != '未选择文件':
        type_txt = False
        input_fa = app.selected_fa.text()
        output_dir = os.path.dirname(input_fa)
    if input_fa == '':
        show_message_dialog("Juse提醒您要输入fa哦")
        return
    if output_name == '':
        show_message_dialog("Juse提醒您没设置输出哦")
        return

    output_fa = f'{output_dir}/{output_name}'
    try:
        _, _, lc = readfa(input_fa, symbol, txt=type_txt, longest=True)
        with open(output_fa, 'w') as output:
            for gene in lc.keys():
                output.write(">" + gene + '\n')
                output.write(lc[gene])
        show_message_dialog("文件已生成")
    except Exception as e:
        show_message_dialog("请检查您的文件或基因标识是否有误")
        logging.error("发生错误: \n%s", str(e))
        return

"""
ID 修改
"""
def id_change(app):

    if app.prefixbutton.isChecked():
        symbol = app.fix_add.toPlainText()
        mod_used = 'pre'
    elif app.suffixbutton.isChecked():
        symbol = app.fix_add.toPlainText()
        mod_used = 'suf'
    elif app.simplybutton.isChecked():
        symbol = ''
        mod_used = 'sim'
    elif app.spenabutton.isChecked():
        symbol = app.spe_symbol.toPlainText()
        mod_used = 'spe'
    else:
        show_message_dialog("貌似你妹让我干任何事的想法，hum？")
        return

    if app.multipc_bok.isChecked() == False:
        input_fa = app.inputfa_txt_2.toPlainText()
        txt = True
        if app.selected_fa_2.text() != '未选择文件':
            input_fa = app.selected_fa_2.text()
            txt = False
        if input_fa == '':
            show_message_dialog("Juse提醒您要输入fa哦")
            return
        if symbol == '' and mod_used != 'sim':
            show_message_dialog("请检查你的前后缀或标识~")
            return

        if txt:
            with open('Jusekit.fa', 'w') as tmp:
                tmp.write(input_fa)
            input_fa = 'Jusekit.fa'
        try:
            if symbol:
                id_modify(inputfile=input_fa, string=symbol, mod=mod_used)
            else:
                id_modify(inputfile=input_fa,  mod=mod_used)
            if app.delete_check.isChecked():
                os.remove(input_fa)
        except Exception as e:
            show_message_dialog("请检查序列文件是否出错")
            logging.error("发生错误: \n%s", str(e))
            return

        show_message_dialog("文件已生成")

    else:

        if app.mpc_path.text() == '未选择文件夹':
            show_message_dialog("不选文件夹，Running要凉凉")
            return
        mp_dir = app.mpc_path.text()
        mp_files = os.listdir(mp_dir)
        if app.fire_end.toPlainText() != '':
            wz = app.fire_end.toPlainText()
            mp_files = [filename for filename in mp_files if filename.endswith(wz)]
        if mp_files == []:
            show_message_dialog("要么是文件夹有问题，要么是你有问题")
            return
        total_num = len(mp_files)
        compl_num = 0
        for file in mp_files:
            try:
                if symbol:
                    id_modify(inputfile=f'{mp_dir}/{file}', string=symbol, mod=mod_used)
                else:
                    id_modify(inputfile=f'{mp_dir}/{file}', mod=mod_used)
                if app.delete_check.isChecked():
                    os.remove(f'{mp_dir}/{file}')
                compl_num += 1
                app.progressBar.setValue(int(compl_num/total_num*100))
            except Exception as e:
                show_message_dialog("请检查序列文件是否出错")
                logging.error("发生错误: \n%s", str(e))
                return
        show_message_dialog("文件已生成")
        app.progressBar.setValue(0)


def sequence_con(app, aligns, symbol, outputdir, pf=True, log=True):

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
        app.con_progress.setValue(int(compl_num/total_num*100))
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
            app.con_progress.setValue(0)
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

    show_message_dialog("串联完成！")
    app.con_progress.setValue(0)

def seq_con(app):

    align_files = app.sel_ali.toPlainText().split(', ')
    if app.sel_ali_path.text() != '未选择文件夹':
        folder_path = app.sel_ali_path.text()
        align_files = []
        for file_name in os.listdir(folder_path):
            file_path = f'{folder_path}/{file_name}'
            if os.path.isfile(file_path):
                align_files.append(file_path)
    if align_files == ['']:
        show_message_dialog("你是不是尝试过所有按钮的无文件运行？")
        return
    if app.pf_able.isChecked():
        pf_able = True
    else:
        pf_able = False
    if app.log_able.isChecked():
        log_able = True
    else:
        log_able = False
    if app.modi_dir.isChecked():
        opdir = app.con_res_dir.toPlainText()
    else:
        opdir = './'
    if app.spe_able.isChecked():
        sb = app.spe_sym.toPlainText()
    else:
        sb = ' '
    try:
        sequence_con(app, aligns=align_files, symbol=sb, outputdir=opdir, pf=pf_able, log=log_able)
    except Exception as e:
        show_message_dialog("您的序列或标识可能有点把子问题，要不检查一下？")
        logging.error("发生错误: \n%s", str(e))
        return
    if app.open_dir.isChecked():
        QDesktopServices.openUrl(QUrl.fromLocalFile(opdir))

"""
提取 ID
"""
def extract_id(app):

    if app.id_file.text() != '未选择文件':
        ids = app.id_file.text()
    elif app.id_frame.toPlainText() != '':
        with open("tmp_id.txt", 'w') as txt:
            txt.write(app.id_frame.toPlainText())
        ids = "tmp_id.txt"
    else:
        show_message_dialog("你的id文件我没有啊:<")
        return

    if app.fa_file.text() != '未选择文件':
        fasta = app.fa_file.text()
        outputdir = os.path.dirname(fasta)
    elif app.fasta_frame.toPlainText() != '':
        with open("tmp_fasta.txt", 'w') as txt:
            txt.write(app.fasta_frame.toPlainText())
        fasta = "tmp_fasta.txt"
        outputdir = '.'
    else:
        show_message_dialog("id的fasta文件我没有啊:<")
        return

    filename = app.id_out_fl.toPlainText()
    if filename == '':
        show_message_dialog("妹有名字你让我怎么输出。")
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
                    app.id_progress.setValue(int(id_com/id_num*100))
    except Exception as e:
        show_message_dialog("id和fasta里必有一个出问题。")
        logging.error("发生错误: \n%s", str(e))
        return
    show_message_dialog("提取完成。")
    app.id_progress.setValue(0)

"""
序列格式转换
"""
def seq_fc(app):

    align_files = app.sel_ali_2.toPlainText().split(', ')
    if app.sel_ali_path_2.text() != '未选择文件夹':
        folder_path = app.sel_ali_path_2.text()
        align_files = []
        for file_name in os.listdir(folder_path):
            file_path = f'{folder_path}/{file_name}'
            if os.path.isfile(file_path):
                align_files.append(file_path)
    if align_files == ['']:
        show_message_dialog("我有理由怀疑你在这里试图凑齐空运行bug。")
        return
    op_dir = app.cv_out_dir.toPlainText()
    if op_dir == '':
        show_message_dialog("这下不得不设置输出路径啦！")
        return

    total_num = len(align_files)
    compu_num = 0
    try:
        for af in align_files:
            id_seq_for, _, _ = readfa(af, symbol=' ',stripornot=True)

            if app.paml_box.isChecked():
                basename = os.path.basename(af)
                op_file = f'{op_dir}/{basename.split(".")[0]}.PML'
                write_paml(op_file, id_seq_for)
            if app.axt_box.isChecked():
                basename = os.path.basename(af)
                op_file = f'{op_dir}/{basename.split(".")[0]}.axt'
                write_axt(op_file, id_seq_for)
            if app.nex_box.isChecked():
                basename = os.path.basename(af)
                op_file = f'{op_dir}/{basename.split(".")[0]}.nex'
                seqtype = check_sequence_type(id_seq_for)
                write_nexus(op_file, id_seq_for, seqtype)
            if app.nex_int_box.isChecked():
                basename = os.path.basename(af)
                op_file = f'{op_dir}/{basename.split(".")[0]}.interleaved.nex'
                seqtype = check_sequence_type(id_seq_for)
                write_nexus_interleaved(op_file, id_seq_for, seqtype)
            if app.phy_box.isChecked():
                basename = os.path.basename(af)
                op_file = f'{op_dir}/{basename.split(".")[0]}.phy'
                write_phylip(op_file, id_seq_for)
            compu_num += 1
            app.convert_progress.setValue(int(compu_num/total_num*100))
    except Exception as e:
        show_message_dialog("输入的文件里有不对劲的东西！")
        app.convert_progress.setValue(0)
        logging.error("发生错误: \n%s", str(e))
        return

    show_message_dialog("格式转换完成咯啊哈哈哈")
    app.convert_progress.setValue(0)

"""
PEP 和 CDS 序列互相转换
"""
def peptocds_button(app):

    cdsfile = app.cds_input_text.toPlainText()
    pepfile_dir = app.pep_input_text.toPlainText()
    output_dir = app.pep_op_dir.toPlainText()

    if cdsfile == '' or pepfile_dir == '':
        show_message_dialog("快给我文件，我已经迫不及待了！")
        return
    if output_dir == '':
        show_message_dialog("我要在哪里发泄我的输出？")
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
            app.pep_to_cds.setValue(int(compu_num/total_num*100))
        show_message_dialog(f"完成了，输出在{output_dir}里。")
        app.pep_to_cds.setValue(0)
    except Exception as e:
        show_message_dialog("是哪里出了问题呢？是哪里呢...")
        app.pep_to_cds.setValue(0)
        logging.error("发生错误: \n%s", str(e))
        return


"""
根据长度等信息过滤序列
"""
def fafilter(app):

    align_files = app.sel_ali_3.toPlainText().split(', ')
    output_dir = app.filter_opdir.toPlainText()
    mls = app.min_len_seq.value()
    mla = app.min_len_ali.value()
    msn = app.min_spe_num.value()
    gn = app.gap_name.toPlainText()
    ss = app.spe_sym_2.toPlainText()
    if align_files == ['']:
        show_message_dialog("此地无银三百两。")
        return
    if output_dir == '':
        show_message_dialog("我望眼欲穿，看我看不到的输出文件夹。")
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
            app.filter_progress.setValue(int(compu_num/total_num*100))
    except Exception as e:
        show_message_dialog('遇到问题序列，程序中断。')
        app.filter_progress.setValue(0)
        logging.error("发生错误: \n%s", str(e))
        return
    show_message_dialog("任务已完成，运行 log 可见 filter.log")
    app.filter_progress.setValue(0)

"""
组装质检
"""
def qc_cal(app):

    fp = app.qc_file.toPlainText()
    op = os.path.dirname(fp)
    gene_symbol = app.gene_symbol_2.toPlainText()

    if fp == '':
        show_message_dialog('请输入文件路径。')
        return

    app.qc_progress.setValue(20)

    try:
        if gene_symbol == '':
            id_seq, _, longest_is = readfa(file=fp, symbol=gene_symbol, stripornot=True)
        else:
            id_seq, _, longest_is = readfa(file=fp, symbol=gene_symbol, longest=True, stripornot=True)
    except Exception as e:
        show_message_dialog(f'发生错误：{e}')
        logging.error("发生错误: \n%s", str(e))
        app.qc_progress.setValue(0)
        return

    app.qc_progress.setValue(50)

    try:
        all_qc_index = qc_calcu(id_seq)
    except Exception as e:
        show_message_dialog(f'发生错误：{e}')
        logging.error("发生错误: \n%s", str(e))
        app.qc_progress.setValue(0)
        return

    app.qc_progress.setValue(80)

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

        app.qc_progress.setValue(100)
        show_message_dialog(f'运算已完成，输出见 {op}/assem_qc.txt。')
        app.qc_progress.setValue(0)
    else:
        all_qc_index = qc_calcu(longest_is)
        app.qc_progress.setValue(90)

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

        app.qc_progress.setValue(100)
        show_message_dialog(f'运算已完成，输出见 {op}/assem_qc.txt。')
        app.qc_progress.setValue(0)


#%% 模块功能 (绘图)
"""
火山图绘制
"""
def vol_plot(app):

    file = app.vol_file.toPlainText()
    log2fc = app.log2fc.value()
    app.vp_pro.setValue(20)
    adjp = app.adjp.value()
    upcol = app.up_color.currentText()
    downcol = app.down_color.currentText()
    app.vp_pro.setValue(50)
    labelsize = app.labelsize.value()
    axissize = app.axissize.value()
    dotsize = app.dotsize.value()
    titlesize = app.titlesize.value()
    numsize = app.numsize.value()
    app.vp_pro.setValue(100)

    try:
        plot_volcano(file, logfc_threshold=log2fc, adjp_threshold=adjp,
                        up_color=upcol, down_color=downcol,point_size=dotsize,
                        tick_size=numsize, title_size=titlesize, axis_size=axissize,
                        label_size=labelsize)
        app.vp_pro.setValue(0)
    except Exception as e:
        show_message_dialog(f"发生错误：{e}\n请检查文件")
        app.vp_pro.setValue(0)

"""
GO 富集分析
"""
def gtlfile_dl(app):

    gtl_url = 'http://current.geneontology.org/ontology/go-basic.obo'
    gtl_fn = 'go_term.list'
    if os.path.exists(gtl_fn) or os.path.exists('go-basic.obo'):
        show_message_dialog("文件已存在，下载终止")
        return
    try:
        urllib.request.urlretrieve(gtl_url, gtl_fn)
        show_message_dialog("GO list file 下载完成")
    except:
        show_message_dialog("下载出错，请检查网络是否出错。")

def GOem_plot(app):

    fp = app.enrich_file.toPlainText()
    if fp == '':
        show_message_dialog("请输入文件路径。")
        return

    xlab = app.enrich_xlab.currentText()
    ylab = app.enrich_ylab.currentText()
    if app.enrich_c.isChecked():
        num = int(app.enrich_c_num.value())
        try:
            plot_GOem_classify(file_path=fp, num=num, xlab=xlab, ylab=ylab)
        except Exception as e:
            show_message_dialog(f"发生错误：{e}\n请检查文件")
    else:
        num = int(app.enrich_num.value())
        try:
            plot_GOem(file_path=fp, num=num, xlab=xlab, ylab=ylab)
        except Exception as e:
            show_message_dialog(f"发生错误：{e}\n请检查文件")

def GOem_anno(app):

    fp = app.enrich_file.toPlainText()
    if fp == '':
        show_message_dialog("请输入文件路径。")
        return

    if os.path.exists('go_term.list'):
        glfile = 'go_term.list'
    elif os.path.exists('go-basic.obo'):
        glfile = 'go-basic.obo'
    else:
        show_message_dialog("不存在 GO list 文件，请下载。")
        return

    golist = read_golist(glfile)
    if golist == {}:
        show_message_dialog("GO list 文件存在错误，请检查。")
        return

    try:
        assign_go(fp, golist)
    except Exception as e:
        show_message_dialog(f"发生错误：{e}\n请检查文件")
        return

    show_message_dialog("已完成注释，请见 GOanno.csv。")