import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
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

def plot_GOem_classify(file_path, num = 5, xlab = 'GeneRatio', ylab = 'Description'):

    data = pd.read_csv(file_path)

    if xlab == 'GeneRatio':
        data['GeneRatio'] = data['GeneRatio'].apply(lambda x: float(x.split('/')[0]) / float(x.split('/')[1]))

    data = data.dropna(subset=['Ontology'])

    # 对每个 Ontology 获取 p 值最小的 num 个
    data_top5_per_ontology = data.groupby('Ontology').apply(lambda x: x.nsmallest(num, 'qvalue')).reset_index(drop=True)
    data_top5_per_ontology = data_top5_per_ontology.sort_values(by=['Ontology', 'Count'], ascending=[True, False])

    ontologies = data_top5_per_ontology['Ontology'].unique()

    plt.figure(figsize=(10, 10))

    cmap = mcolors.LinearSegmentedColormap.from_list("", ["red", "blue"])

    plot = sns.scatterplot(x=xlab, y=ylab, size='Count', hue='qvalue',
                           palette=cmap, sizes=(50, 300), data=data_top5_per_ontology)

    plt.axhline(y=num-0.5, color='black')
    plt.axhline(y=num*2-0.5, color='black')
    plt.text(1.05, 1 / 6, ontologies[2].replace("_", " ").title(), rotation='vertical', verticalalignment='center',
             transform=plt.gca().transAxes)
    plt.text(1.05, 0.5, ontologies[1].replace("_", " ").title(), rotation='vertical', verticalalignment='center',
             transform=plt.gca().transAxes)
    plt.text(1.05, 2 / 3 + 1 / 6, ontologies[0].replace("_", " ").title(), rotation='vertical', verticalalignment='center',
             transform=plt.gca().transAxes)

    legend = plot.legend(title='Legend', bbox_to_anchor=(1.2, 1), loc=2)
    frame = legend.get_frame()
    frame.set_width(200)
    frame.set_height(500)

    for text in legend.texts[1:-1]:
        text_content = text.get_text()
        if text_content == 'Count':
            break
        value = float(text_content)
        text.set_text(format(value, ".1e"))

    plt.title('GO Enrichment Plot')
    plt.xlabel('GeneRatio', fontsize=12)
    plt.ylabel('GO Description', fontsize=12)

    plt.tight_layout()
    plt.show()

def plot_GOem(file_path, num = 20, xlab = 'GeneRatio', ylab = 'Description'):

    data = pd.read_csv(file_path)
    data = data.dropna(subset=['Description'])

    if xlab == 'GeneRatio':
        data['GeneRatio'] = data['GeneRatio'].apply(lambda x: float(x.split('/')[0]) / float(x.split('/')[1]))

    data = data.nsmallest(num, 'qvalue')
    data = data.sort_values(by='Count', ascending=False)

    plt.figure(figsize=(10, 10))

    cmap = mcolors.LinearSegmentedColormap.from_list("", ["red", "blue"])

    plot = sns.scatterplot(x=xlab, y=ylab, size='Count', hue='qvalue',
                           palette=cmap, sizes=(50, 300), data=data)

    legend = plot.legend(title='Legend', bbox_to_anchor=(1.05, 1), loc=2)
    frame = legend.get_frame()
    frame.set_width(200)
    frame.set_height(500)

    for text in legend.texts[1:-1]:
        text_content = text.get_text()
        if text_content == 'Count':
            break
        value = float(text_content)
        text.set_text(format(value, ".1e"))

    plt.title('GO Enrichment Plot')
    plt.xlabel('GeneRatio', fontsize=12)
    plt.ylabel('GO Description', fontsize=12)

    plt.tight_layout()
    plt.show()


def read_golist(filepath):

    golist = {}
    with open(filepath, 'r') as f:

        for line in f:
            if line.startswith('id:'):
                GOid = line.lstrip('id:').strip()
                golist[GOid] = {}
            if line.startswith('name:'):
                GOname = line.lstrip('name:').strip()
                golist[GOid]['description'] = GOname
            if line.startswith('namespace:'):
                GOonto = line.lstrip('namespace:').strip()
                golist[GOid]['ontology'] = GOonto

    return golist


def assign_go(file_path, golist):

    data = pd.read_csv(file_path)
    data['Description'] = data['ID'].apply(lambda x: golist.get(x, {}).get('description', 'NA(Obsolete)'))
    data['Ontology'] = data['ID'].apply(lambda x: golist.get(x, {}).get('ontology', 'NA(Obsolete)'))
    dirpath = os.path.dirname(file_path)
    data.to_csv(f'{dirpath}/GOanno.csv', index=False)