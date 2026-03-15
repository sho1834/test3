# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 12:26:34 2026

@author: kk183
"""

import streamlit as st
import pandas as pd

# 1. データの読み込みと準備
@st.cache_data # データをキャッシュして高速化
def load_data():
    # 実際にはアップロード機能にするか、パスを指定
    return pd.read_csv("sales_20260305212949018.csv", encoding='cp932')

try:
    df = load_data()

    # 日付設定 (20260305)
    formated_today = 20260305
    month_s = (formated_today // 100) * 100 + 1
    date_str = f"{str(formated_today)[:4]}年{str(formated_today)[4:6]}月{str(formated_today)[6:]}日"

    # --- ページ設定 ---
    st.set_page_config(page_title="店舗別売上レポート", layout="centered")
    st.title(f"📊 店舗別売上レポート")
    st.subheader(f"対象日: {date_str}")

    # 2. 集計処理
    today_df = df[df["会計日"] == formated_today]
    month_df = df[(df["会計日"] >= month_s) & (df["会計日"] <= formated_today)]

    today_grouped = today_df.groupby("お店名")["金額"].sum()
    month_grouped = month_df.groupby("お店名")["金額"].sum()

    shop_list = df["お店名"].unique()
    
    # 表示用データフレームの作成
    summary_list = []
    for shop in shop_list:
        summary_list.append({
            "お店名": shop,
            "今日の売上": today_grouped.get(shop, 0),
            "今月の累計売上": month_grouped.get(shop, 0)
        })
    
    summary_df = pd.DataFrame(summary_list)

    # 合計の計算
    total_today = today_df["金額"].sum()
    total_month = month_df["金額"].sum()
    
    # 3. GUI (Web画面) の構築
    
    # メトリクス表示（Webならではの見せ方）
    col1, col2 = st.columns(2)
    col1.metric("本日合計", f"{total_today:,}円")
    col2.metric("今月合計累計", f"{total_month:,}円")

    st.divider()

    # データテーブルの表示
    # Pandasのスタイルを使って、Tkinterのような「合計行の強調」を再現
    def highlight_total(s):
        return ['background-color: #1a1a1a; color: #ffca28; font-weight: bold' if s.name == '合計' else '' for _ in s]

    # 合計行を追加
    display_df = summary_df.copy()
    total_row = pd.DataFrame([{"お店名": "--- 合計 ---", "今日の売上": total_today, "今月の累計売上": total_month}])
    display_df = pd.concat([display_df, total_row], ignore_index=True)

    # 数値フォーマットを適用して表示
    st.dataframe(
        display_df.style.format({"今日の売上": "{:,}円", "今月の累計売上": "{:,}円"}),
        use_container_width=True,
        hide_index=True
    )

except FileNotFoundError:
    st.error("CSVファイルが見つかりません。パスを確認してください。")