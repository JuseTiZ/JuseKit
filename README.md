## JuseKit

**JU**st a **SE**quence tool**KI**t for **T**ranscriptomics

![](https://jusetiz.github.io/pic2/jusekit.png)

基于 `Python v3.10` 和 `PyQt5` 开发，软件打包使用 `pyinstaller` 进行，请在右侧 Release 下载。

`JuseKit.zip` 解压后使用文件夹中的 `Jusekit.exe` 打开。

古早版本可以直接下载 `JuseKit.exe` 打开，但运行速度和性能等可能有所下降。

在该 repository 的 `examples` 文件夹下储存着用于运行 JuseKit 的示例数据。

### 另外的运行方式

该软件也可直接使用源码运行，不过需要安装好已使用的包：

```cmd
git clone https://github.com/JuseTiZ/JuseKit.git
cd JuseTiZ
python JuseKit_window.py
```

如果你想自行编译成 `exe` 文件，可以通过 `pyinstaller` 进行：

```cmd
git clone https://github.com/JuseTiZ/JuseKit.git
cd JuseTiZ
pyinstaller --noconsole --name=JuseKit --icon=jusekit.ico JuseKit_window.py --hidden-import=matplotlib.backends.backend_pdf
```

教程可见：[Juse's blog](https://biojuse.com/)

若存在报错 Bug 可以联系 Juse 修复。

### 目前已经实现的功能

- 提取最长转录本。
- 根据 id 提取序列。
- 对序列的 id 进行各种处理。
- 串联序列并得到分区信息。
- 批量进行序列格式转换。
- 批量提取 Orthofinder 的 orthogroup 对应的 CDS 序列。
- 批量进行序列的物种数和长度过滤。
- 火山图绘制。
- 气泡图绘制。
- 组装指标计算。

目前已有的小功能：

- 学习计时器。
- 批量改后缀。
