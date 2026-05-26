import json
import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.subplots as sp

def load_data(file_json,category=None):
    with open(file_json,'r',encoding="utf-8") as f:
        data = json.load(f)
    data_list = []
    for key,value in data.items():
        if category:
            value["品类"]=category
        value["价格"]=re.sub(r"元/.*","",value["价格"])       #去除价格单位
        data_list.append(value)
    #print(data_list)
    df = pd.DataFrame(data_list)
    df['价格'] = pd.to_numeric(df['价格'], errors='coerce')         #价格转浮点数
    df['日期'] = pd.to_datetime(df['日期'], errors='coerce')        #日期转为标准格式(datetime64 类型)
    df = df.dropna(subset=['价格', '日期'])  # 删除价格/日期有缺失的行
    return df
df_vegetable=load_data("蔬菜价格.json",category="蔬菜")
#print(df_vegetable)
df_fruit=load_data("水果价格.json",category="水果")
#rint(df_fruit)
df_meat_egg=load_data("禽畜肉蛋.json",category="禽畜肉蛋")
#print(df_meat_egg)
df_grain_oil=load_data("粮油米面.json",category="粮油米面")
#print(df_grain_oil)
#合并食品价格数据
df_all=pd.concat([df_meat_egg,df_grain_oil,df_vegetable,df_fruit],ignore_index=True)
#print(df_all)


plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置黑体支持中文
plt.rcParams['axes.unicode_minus'] = False    # 修复负号显示问题
sns.set(font='SimHei')

# 让Seaborn同步使用中文字体
# 1. 静态：不同品类的均价对比（Matplotlib）
#plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文显示问题
# plt.figure(figsize=(10, 6))
# # 计算各品类均价
# avg_price = df_all.groupby('品类')['价格'].mean().sort_values(ascending=False)
# # 绘制柱状图
# bars = plt.bar(avg_price.index, avg_price.values, color=['#2ca02c', '#ff7f0e', '#1f77b4', '#d62728'])
# #标注均价数值
# for bar in bars:
#     height = bar.get_height()
#     plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
#              f'{height:.2f}', ha='center', va='bottom', fontsize=10)
#
# plt.title('农产品各品类均价对比', fontsize=14)
# plt.xlabel('品类', fontsize=12)
# plt.ylabel('均价（元）', fontsize=12)
# plt.grid(axis='y', alpha=0.3)
# plt.show()


#2. 交互式：同品类（蔬菜）不同商品的价格对比（Plotly，可悬停看详情）
# df_vegetable_top10 = df_vegetable.groupby('商品名称')['价格'].mean().sort_values(ascending=False).head(10).reset_index()
# #print(df_vegetable_top10)
# fig = px.bar(df_vegetable_top10, x='商品名称', y='价格',
#              title='蔬菜品类TOP10商品均价对比',
#              color='价格', color_continuous_scale='blues',
#              labels={'价格':'均价（元）', '商品名称':'商品'},
#              template='plotly_white')
# # 旋转x轴标签，避免重叠
# fig.update_layout(xaxis_tickangle=-45)
# fig.show()  # 本地运行会打开浏览器，支持缩放、悬停看数值



#示例：蔬菜品类TOP5商品的地区价格分布（Seaborn箱线图）
# # ========== 2. 数据处理：筛选蔬菜TOP5商品 ==========
# # 假设df_vegetable是你的蔬菜数据集（包含商品名称、价格、地区等列）
# # 选蔬菜TOP5商品（按商品名称出现频次取前5）
# top5_veg = df_vegetable['商品名称'].value_counts().head(5).index
# df_veg_top5 = df_vegetable[df_vegetable['商品名称'].isin(top5_veg)]     #保留有索引名称的行
# plt.figure(figsize=(12, 7))
# # 移除palette，使用Seaborn默认配色
# sns.boxplot(x='商品名称', y='价格', data=df_veg_top5,hue='商品名称',palette="Set2",legend=False)
# plt.title('蔬菜TOP5商品的地区价格分布', fontsize=14)
# plt.xlabel('商品名称', fontsize=12)
# plt.ylabel('价格（元）', fontsize=12)
# plt.xticks(rotation=30)                 #商品名称顺时针旋转30度
# plt.grid(axis='y', alpha=0.3)           #显示网格线(透明度)
# plt.tight_layout()                      #自动调整图表布局
# plt.show()


# 进阶：地区-商品价格热力图（Seaborn）
# 选前8个地区、前8个蔬菜商品做热力图
# top8_area = df_vegetable['地区'].value_counts().head(8).index
# top8_veg = df_vegetable['商品名称'].value_counts().head(8).index
# df_heat = df_vegetable[(df_vegetable['地区'].isin(top8_area)) & (df_vegetable['商品名称'].isin(top8_veg))]
# #print(df_heat)
# # 透视表：行=地区，列=商品，值=均价
# pivot_heat = df_heat.pivot_table(index='地区', columns='商品名称', values='价格', aggfunc='mean')
# plt.figure(figsize=(16, 9))
# sns.heatmap(pivot_heat, annot=True, cmap='YlGnBu', fmt='.1f', linewidths=0.5)
# plt.title('蔬菜商品-地区价格热力图', fontsize=14)
# plt.xticks(rotation=30)
# plt.show()



# 绘制多品类价格直方图（带核密度曲线）
plt.figure(figsize=(20, 5))
for cate, color in zip(['蔬菜', '水果', '禽畜肉蛋', '粮油米面'], ['green', 'orange', 'blue', 'red']):
    # 取该品类价格数据
    price_data = df_all[df_all['品类'] == cate]['价格']
    # 直方图
    sns.histplot(price_data, bins=5, alpha=0.3, label=cate, color=color, kde=True)
plt.title('农产品各品类价格分布', fontsize=14)
plt.xlabel('价格（元）', fontsize=12)
plt.ylabel('频次', fontsize=12)
plt.legend()
plt.grid(axis='y', alpha=0.5)
plt.show()


# 创建2行2列的子图
# fig = sp.make_subplots(
#     rows=2, cols=2,
#     subplot_titles=('各品类均价对比', '水果价格趋势', '蔬菜价格分布', '禽畜肉蛋地区价格箱线图'),
#     horizontal_spacing=0.1, vertical_spacing=0.15
# )
#
# # 子图1：各品类均价柱状图
# avg_price = df_all.groupby('品类')['价格'].mean().sort_values(ascending=False)
# bar1 = px.bar(avg_price, x=avg_price.index, y=avg_price.values).data[0]
# fig.add_trace(bar1, row=1, col=1)
#
# # 子图2：水果价格趋势折线图
# df_fruit_trend = df_fruit.groupby('日期')['价格'].mean().reset_index()
# line2 = px.line(df_fruit_trend, x='日期', y='价格').data[0]
# fig.add_trace(line2, row=1, col=2)
#
# # 子图3：蔬菜价格直方图
# hist3 = px.histogram(df_vegetable, x='价格', nbins=20).data[0]
# fig.add_trace(hist3, row=2, col=1)
#
# # 子图4：禽畜肉蛋TOP5地区价格箱线图
# top5_meat_area = df_meat_egg['地区'].value_counts().head(5).index
# df_meat_top5 = df_meat_egg[df_meat_egg['地区'].isin(top5_meat_area)]
# box4 = px.box(df_meat_top5, x='地区', y='价格').data[0]
# fig.add_trace(box4, row=2, col=2)
#
# # 全局样式
# fig.update_layout(height=800, width=1000, title_text='农产品价格综合分析仪表盘', template='plotly_white')
# fig.show()