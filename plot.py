import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_volcano(file_path, logfc_threshold=1, adjp_threshold=0.05,
                 width=10, height=10, point_size=20,
                 up_color='red', down_color='blue',
                 tick_size=14, title_size=20, label_size=12,
                 axis_size=14):

    # 读取文件
    data = pd.read_csv(file_path)
    title = os.path.basename(file_path).split('.')[0]

    # 允许列名变化（适应 DESeq2 & edgeR）
    logfc_col = 'logFC' if 'logFC' in data.columns else 'log2FoldChange'
    adjp_col = 'FDR' if 'FDR' in data.columns else 'padj'

    data['minus_log10_padj'] = -np.log10(data[adjp_col])

    # 标记差异表达基因
    data['color'] = 'gray'
    data.loc[(data[logfc_col] > logfc_threshold) & (data[adjp_col] < adjp_threshold), 'color'] = up_color
    data.loc[(data[logfc_col] < -logfc_threshold) & (data[adjp_col] < adjp_threshold), 'color'] = down_color

    # 基础框架
    fig, ax = plt.subplots(figsize=(width, height))
    # 绘制点
    ax.scatter(data[logfc_col], data['minus_log10_padj'], c=data['color'], s=point_size)
    # 设置标签和标题
    ax.set_xlabel('Log2FC', fontsize=axis_size, labelpad=6)
    if adjp_col == 'padj':
        ax.set_ylabel('-Log10 Adjusted P-Value', fontsize=axis_size, labelpad=12)
    else:
        ax.set_ylabel('-Log10 FDR', fontsize=axis_size, labelpad=12)
    ax.set_title(title, fontsize=title_size, pad=12)
    # 设置坐标轴取值范围
    ax.set_ylim(-0.4, None)
    xlim = ax.get_xlim()
    max_abs_xlim = max(abs(xlim[0]), abs(xlim[1]))
    symmetric_xlim = (-max_abs_xlim, max_abs_xlim)
    ax.set_xlim(symmetric_xlim)
    # 设置辅助线
    ax.axhline(y=-np.log10(adjp_threshold), color='gray', linestyle='dashed', lw=1.2)
    ax.axvline(x=logfc_threshold, color='gray', linestyle='dashed', lw=1.2)
    ax.axvline(x=-logfc_threshold, color='gray', linestyle='dashed', lw=1.2)
    # 设置刻度字体大小
    ax.tick_params(axis='x', labelsize=tick_size)
    ax.tick_params(axis='y', labelsize=tick_size)
    # 设置标签
    ax.scatter(data.loc[data['color'] == up_color, logfc_col],
               data.loc[data['color'] == up_color, 'minus_log10_padj'], c=up_color, s=point_size,
               label='Up-regulated')
    ax.scatter(data.loc[data['color'] == down_color, logfc_col],
               data.loc[data['color'] == down_color, 'minus_log10_padj'], c=down_color, s=point_size,
               label='Down-regulated')
    ax.legend(loc='upper left', fontsize=label_size, bbox_to_anchor=(1.05, 1),)
    # 设置窗口名称
    fig.canvas.manager.set_window_title('Volcano')
    # 显示图像
    plt.show()

