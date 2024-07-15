# Main window of JuseKit #
# Author: Juse
# Version: 0.8

import sys
from utils.windowAction import *
from utils.windowMore import *
from UIs.JuseKitQtUI import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QAction
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QIcon


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

        # 改尾缀窗口
        self.wz_modify = QtWidgets.QAction(self)
        self.wz_modify.setIconText("批量改文件尾缀")
        self.wz_modify.triggered.connect(lambda: wz_modi(app=self))
        self.file_menu.addAction(self.wz_modify)

        # 学习计时窗口
        self.study_rc = QtWidgets.QAction(self)
        self.study_rc.setIconText("学习计时小工具")
        self.study_rc.triggered.connect(lambda: open_learning_timer(app=self))
        self.file_menu.addAction(self.study_rc)

        self.file_menu.addSeparator()

        # Juse 简介链接
        self.au_pf = QtWidgets.QAction(self)
        self.au_pf.setIconText("关于作者那些事")
        self.au_pf.triggered.connect(lambda: blog("https://jusetiz.github.io/myself/"))
        self.file_menu.addAction(self.au_pf)

        # Blog 留言面板
        self.au_ms = QtWidgets.QAction(self)
        self.au_ms.setIconText("想跟作者留些言")
        self.au_ms.triggered.connect(lambda: blog("https://jusetiz.github.io/messageboard/"))
        self.file_menu.addAction(self.au_ms)

        # 教程页面
        self.file_menu_2 = self.menu_bar.addMenu("教程传送")
        assempr = QMenu("组装序列处理", self)
        phyloge = QMenu("系统发育分析", self)
        plotreg = QMenu("绘图专区", self)

        jc = [assempr, phyloge, plotreg]
        for i in jc:
            self.file_menu_2.addMenu(i)

        as_web = {'提取最长转录本':'https://jusetiz.github.io/2023/04/08/JuseKit（一） —— 提取最长转录本',
                  '处理组装 id':'https://jusetiz.github.io/2023/04/09/JuseKit（二） —— 序列id简化、加前缀尾缀或转变为物种名',
                  '根据 id 提取序列':'https://jusetiz.github.io/2023/04/13/JuseKit（三） —— 串联序列、根据id提取序列、批量修改文件尾缀',
                  '组装指标计算':'https://jusetiz.github.io/2023/09/01/JuseKit（八） —— 计算转录组组装指标'}

        ph_web = {'序列串联':'https://jusetiz.github.io/2023/04/13/JuseKit（三） —— 串联序列、根据id提取序列、批量修改文件尾缀',
                  '序列格式转换':'https://jusetiz.github.io/2023/04/26/JuseKit（四） —— 序列格式转换以及 Orthogroup 的 cds 提取',
                  'PEP 转 CDS':'https://jusetiz.github.io/2023/04/26/JuseKit（四） —— 序列格式转换以及 Orthogroup 的 cds 提取',
                  '序列过滤':'https://jusetiz.github.io/2023/05/14/JuseKit（五） —— 用于系统发育分析的序列过滤'}

        pl_web = {'火山图':'https://jusetiz.github.io/2023/07/04/JuseKit（六） —— 绘制火山图',
                  '富集气泡图':'https://jusetiz.github.io/2023/08/04/JuseKit（七） —— 绘制 GO 富集分析气泡图'}

        all_web = {assempr:as_web,
                   phyloge:ph_web,
                   plotreg:pl_web}

        for w in all_web:
            for option, page in all_web[w].items():
                action = QAction(option, self)
                action.triggered.connect(lambda checked, page=page: blog(page))
                w.addAction(action)

        # 按钮功能
        self.gene_symbol_en.stateChanged.connect(lambda state: on_checkbox_state_changed(self, state))
        self.inputfa.clicked.connect(lambda: on_button_open_file_clicked(self.selected_fa))
        self.le_running.clicked.connect(lambda: longest_exatract(self))
        self.clearinput.clicked.connect(lambda: resetle_1(self))
        self.clearinput_2.clicked.connect(lambda: resetle_2(self))
        self.prefixbutton.toggled.connect(lambda: update_group_box(self))
        self.simplybutton.toggled.connect(lambda: update_group_box(self))
        self.suffixbutton.toggled.connect(lambda: update_group_box(self))
        self.spenabutton.toggled.connect(lambda: update_group_box(self))
        self.multipc_bok.stateChanged.connect(lambda state: on_checkbox_state_changed_2(self, state))
        self.idpc_running.clicked.connect(lambda: id_change(self))
        self.inputfa_2.clicked.connect(lambda: on_button_open_file_clicked(self.selected_fa_2))
        self.multipc_button.clicked.connect(lambda: browse_folder_1(self, self.mpc_path))
        self.sel_ali_bro_2.clicked.connect(lambda: browse_folder_2(self, label1=self.sel_ali_path, label2=self.sel_ali))
        self.sel_ali_bro.clicked.connect(lambda: select_mtfiles(self, label1=self.sel_ali_path, label2=self.sel_ali))
        self.rm_file.clicked.connect(lambda: clear_files(self))
        self.sel_ali.installEventFilter(self)
        self.modi_dir.stateChanged.connect(lambda state: on_checkbox_state_changed_3(self, state))
        self.spe_able.stateChanged.connect(lambda state: on_checkbox_state_changed_4(self, state))
        self.start_con.clicked.connect(lambda: seq_con(self))
        self.con_res_sel.clicked.connect(lambda: browse_folder_1(self, self.con_res_dir))
        self.fa_file_upload.clicked.connect(lambda: on_button_open_file_clicked(self.fa_file))
        self.id_file_ul.clicked.connect(lambda: on_button_open_file_clicked(self.id_file))
        self.clear_fl.clicked.connect(lambda: resetle_3(self))
        self.start_ex.clicked.connect(lambda: extract_id(self))
        self.cv_od_bu.clicked.connect(lambda: browse_folder_1(self, self.cv_out_dir))
        self.clear_cvfile.clicked.connect(lambda: resetle_4(self))
        self.sel_ali_2.installEventFilter(self)
        self.sel_ali_bro_4.clicked.connect(lambda: browse_folder_2(self, label1=self.sel_ali_path_2, label2=self.sel_ali_2))
        self.sel_ali_bro_3.clicked.connect(lambda: select_mtfiles(self, label1=self.sel_ali_path_2, label2=self.sel_ali_2))
        self.cv_running.clicked.connect(lambda: seq_fc(self))
        self.pep_input.clicked.connect(lambda: browse_folder_1(self, self.pep_input_text))
        self.cds_input.clicked.connect(lambda: on_button_open_file_clicked(self.cds_input_text))
        self.pep_op_dir_set.clicked.connect(lambda: browse_folder_1(self, self.pep_op_dir))
        self.ptc_running.clicked.connect(lambda: peptocds_button(self))
        self.cds_input_text.installEventFilter(self)
        self.sel_ali_bro_5.clicked.connect(lambda: select_mtfiles(self, label1=None, label2=self.sel_ali_3))
        self.filter_bu.clicked.connect(lambda: browse_folder_1(self, self.filter_opdir))
        self.ptc_running_2.clicked.connect(lambda: fafilter(self))
        self.sel_ali_3.installEventFilter(self)
        self.vol_file.installEventFilter(self)
        self.plot_bu_1.clicked.connect(lambda: vol_plot(self))
        self.sel_vol_file.clicked.connect(lambda: on_button_open_file_clicked(self.vol_file))

        self.set_enrich_file.clicked.connect(lambda: on_button_open_file_clicked(self.enrich_file))
        self.enrich_file.installEventFilter(self)
        self.gtl_dl.clicked.connect(lambda: gtlfile_dl(self))
        self.plot_bu_2.clicked.connect(lambda: GOem_plot(self))
        self.gef_c.clicked.connect(lambda: GOem_anno(self))
        self.qc_file.installEventFilter(self)

        self.sel_qc_file.clicked.connect(lambda: on_button_open_file_clicked(self.qc_file))
        self.qc_running.clicked.connect(lambda: qc_cal(self))


    # 拖拽文件并读取
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
                    show_message_dialog("你给的文件太多，我只能接受一个QVQ")
                    return True
                source.setText(files[0])
                return True
        return super().eventFilter(source, event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MyApp()
    main_window.setWindowIcon(QIcon('jusekit.ico'))
    main_window.show()
    sys.exit(app.exec_())