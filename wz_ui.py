# wz_ui.py
# Author: Juse
# Description: Used to replace file suffixes in bulk.

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
import sys
from wz_kit import wzkit
import os

class Wzapp(QMainWindow, wzkit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.file_dir.clicked.connect(self.browse_folder)
        self.running.clicked.connect(self.batch_rename_files)

    def browse_folder(self):
        end_if = ['.sim.fa', '.pre.fa', '.spe.fa', '.suf.fa']
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", "", options=options)
        if folder_path:
            self.label.setText(folder_path)
            files = os.listdir(folder_path)
            if any(any(file.endswith(end) for end in end_if) for file in files):
                self.show_message_dialog(text = "检测到有特定尾缀的文件，已为你自动填写。")
                if any(file.endswith('.sim.fa') for file in files):
                    self.now_wz.setText('.sim.fa')
                if any(file.endswith('.pre.fa') for file in files):
                    self.now_wz.setText('.pre.fa')
                if any(file.endswith('.spe.fa') for file in files):
                    self.now_wz.setText('.spe.fa')
                if any(file.endswith('.suf.fa') for file in files):
                    self.now_wz.setText('.suf.fa')
        else:
            return

    def show_message_dialog(self, text):
        message_box = QMessageBox()
        message_box.setWindowTitle("这是一个弹窗")
        message_box.setText(text)
        message_box.setIcon(QMessageBox.Information)
        message_box.exec_()

    def batch_rename_files(self):
        # 遍历文件夹中的所有文件
        folder_path = self.label.text()
        old_suffix = self.now_wz.toPlainText()
        new_suffix = self.to_wz.toPlainText()
        if folder_path == '未选择文件夹':
            self.show_message_dialog(text="你一定要什么时候都尝试一下空Run吗？")
            return
        if old_suffix == '':
            self.show_message_dialog(text="原有尾缀不能填空哦不然会出问题")
            return
        for filename in os.listdir(folder_path):
            # 检查文件是否以旧扩展名结尾
            if filename.endswith(old_suffix):
                # 去掉旧扩展名，添加新扩展名
                new_filename = filename[:-len(old_suffix)] + new_suffix

                # 获取文件的完整路径
                old_file_path = os.path.join(folder_path, filename)
                new_file_path = os.path.join(folder_path, new_filename)

                # 重命名文件
                os.rename(old_file_path, new_file_path)
        self.show_message_dialog(text="批量替换成功")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = Wzapp()
    main_window.show()
    sys.exit(app.exec_())