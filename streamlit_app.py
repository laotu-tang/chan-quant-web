# streamlit_app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

st.set_page_config(layout="wide")
st.title("缠论自动买点识别平台")

# 1. 上传CSV文件
uploaded_file = st.file_uploader("上传K线数据（CSV）", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['trade_date'] = pd.to_datetime(df['trade_date'])
    df.sort_values('trade_date', inplace=True)
    df.reset_index(drop=True, inplace=True)

    # 2. 绘制基础K线图 + 中枢 + 笔（此处仅示意）
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df['trade_date'], df['close'], label='Close')

    # 示例中枢区（用实际中枢识别逻辑替代）
    mid_idx = len(df) // 2
    center_start = df['trade_date'].iloc[mid_idx - 5]
    center_end = df['trade_date'].iloc[mid_idx + 5]
    low = df['low'].iloc[mid_idx-5:mid_idx+5].min()
    high = df['high'].iloc[mid_idx-5:mid_idx+5].max()
    ax.axvspan(center_start, center_end, ymin=0.02, ymax=0.98, color='orange', alpha=0.3, label='中枢')

    # 3. 示例买点识别（简单模拟，真实使用替换为缠论笔/段分析结果）
    buy_points = []
    for i in range(10, len(df)-10):
        # 简化的一买识别：前5天下跌，后5天上涨
        if df['low'].iloc[i] < df['low'].iloc[i-5:i].min() and df['low'].iloc[i] < df['low'].iloc[i+1:i+6].min():
            buy_points.append((df['trade_date'].iloc[i], df['close'].iloc[i], "买点一"))

        # 简化的二买识别：前期出现低点，后续未破且出现上涨
        if len(buy_points) >= 1:
            last_buy_date = buy_points[-1][0]
            if df['trade_date'].iloc[i] > last_buy_date and                df['low'].iloc[i] > min(df['low'].iloc[i-5:i]) and                df['close'].iloc[i] > df['close'].iloc[i-1]:
                buy_points.append((df['trade_date'].iloc[i], df['close'].iloc[i], "买点二"))

    # 4. 图表标注买点
    for date, price, btype in buy_points:
        ax.text(date, price, '★', fontsize=16, color='gold', ha='center', va='bottom')

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.legend()
    plt.xticks(rotation=45)

    # 显示图表和表格
    col1, col2 = st.columns([2, 1])
    with col1:
        st.pyplot(fig)
    with col2:
        if buy_points:
            df_buy = pd.DataFrame(buy_points, columns=['日期', '价格', '买点类型'])
            st.dataframe(df_buy)
        else:
            st.info("当前数据未识别出买点")
