## JuseKit

**JU**st a **SE**quence tool**KI**t for **T**ranscriptomics

![](https://jusetiz.github.io/pic2/jusekit.png)

该软件的目标：以最接地气的方式帮助进行生信分析。

该软件基于 `Python v3.10` 和 `PyQt5` 开发，支持在 Windows 操作系统运行，请在右侧 Release 下载。

其中 `JuseKit.zip` 解压后使用文件夹中的 `Jusekit.exe` 打开。`JuseKit.exe` 可以直接打开，无需其他操作，但运行速度和性能等可能不如前者。

该软件也可在 Linux 系统下运行，请 `git clone` 后运行 `python main.py`。

运行要求：可进行图形交互（因此在服务器上可能行不通，实在不行可以扒源码自己弄个脚本）。

功能教程可见：[Juse's blog](https://jusetiz.github.io/)

若存在任何报错 Bug 可以联系 Juse 进行修复。

## 目前的功能进度

- 提取最长转录本。*（已实现）*
- 根据 id 提取序列。*（已实现）*
- 对序列的 id 进行各种处理。*（已实现）*
- 串联序列并得到分区信息。*（已实现）*
- 批量改后缀。*（已实现）*
- 批量进行序列格式转换。*（已实现）*
- 批量提取 Orthofinder 的 orthogroup 对应的 CDS 序列。*（已实现）*
- 批量进行序列的物种数和长度过滤。*（已实现）*
