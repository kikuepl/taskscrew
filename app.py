import streamlit as st
import pandas as pd
from collections import defaultdict
import numpy as np

uploaded_file = st.file_uploader("Excelファイルを選択してください", type=["xlsx", "csv"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.sidebar.write("ファイルの内容：")
    st.sidebar.dataframe(df)
    column_names = df.columns.tolist()
    len_column_names = len(column_names)
    pid_dct = defaultdict(int)
    screwname_dct =defaultdict(list)
    dct = {}
    for idx, row in df.iterrows():
        row_dict = row.to_dict()
        pid_dct[row_dict['品番']] = idx
        screwname_dct[row_dict['ネジの呼び']].append(idx)
        dct[idx] = row_dict
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "task_type" not in st.session_state:
        st.session_state["task_type"] = "0"
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    task = {
        "0": "タスクを入力してください",
        "1": "品番と仕様項目から数値を抽出する",
        "2": "ねじの呼び・取り付ける鉄板から品番を抽出する"
    }
    product_num = {
        "1" : "全長",
        "2" : "ネジ長さ",
        "3" : "最大取付物厚",
        "4" : "穿孔径",
        "5" : "アンカー埋込み長さ",
        "6" : "穿孔深さ",
        "7" : "座金付ナット二面幅",
        "8" : "入数 (小箱)",
        "9" : "入数 (大箱)",
        "10" : "入数 (大小)",
        "11" : "標準価格",
    }
    if not st.session_state["messages"]:
        with st.chat_message("assistant"):
            st.markdown(f"タスクのタイプを入力してください。  \n・1 : {task['1']}  \n・2 : {task['2']}")
            with st.expander("1 .詳細を表示"):
                st.markdown("---")
                st.markdown(f"{task['1']}場合は  \n以下の形式で入力してください  \n・品番  \n・仕様項目(対応する数字は以下のとおりです)  \n```python  \n1 : 全長,  \n2 : ネジ長さ,  \n3 : 最大取付物厚,  \n4 : 穿孔径,  \n5 : アンカー埋込み長さ,  \n6 : 穿孔深さ,  \n7 : 座金付ナット二面幅,  \n8 : 入数 (小箱), \n9 : 入数 (大箱),  \n10 : 入数 (大小),  \n11 : 標準価格,  \n```")
            with st.expander("2 .詳細を表示"):
                st.markdown("---")
                st.markdown(f"{task['2']}場合は  \n以下の形式で入力してください  \n・ねじの呼び  \n・取り付ける鉄板の厚さ")
    if user_input := st.chat_input("タスクのタイプを入力してください"):
        L = user_input.split('\n')
        task_type = L[0]
        if task_type == "1":
            with st.chat_message("user"):
                st.session_state.messages.append({"role": "user", "content" : user_input})
                st.markdown(user_input)
            if (len(L) -1 < 2):
                response = "要素数が少ないです。  \n・品番  \n・仕様項目  \nの形式に従って入力してください"
            p_id = L[1]
            p_id_idx = pid_dct[p_id]
            response = ""
            nums = L[2:]
            nums = list(set(nums))
            nums.sort()
            for t in nums:
                if t not in product_num:
                    response += f"{t} に対応する項目は見つかりませんでした"
                    continue
                if t == "10":
                    response += f"入数 (小箱) : {dct[p_id_idx][product_num['8']]}  \n"
                    response += f"入数 (大箱) : {dct[p_id_idx][product_num['9']]}  \n"
                else:
                    response += f"{product_num[t]} : {dct[p_id_idx][product_num[t]]}  \n"
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        elif task_type == "2":
            with st.chat_message("user"):
                st.session_state.messages.append({"role": "user", "content" : user_input})
                st.markdown(user_input)
            L = user_input.split("\n")
            response = ""
            if (len(L)-1 < 2):
                response = "要素数が少ないです。  \n・ねじの呼び  \n・取り付ける鉄板の厚さ  \nの形式に従って入力してください"
            elif (len(L)-1 > 2):
                response = "要素数が多いです。  \n・ねじの呼び  \n・取り付ける鉄板の厚さ  \nの形式に従って入力してください"
            else:
                screwname = L[1]
                num = int(L[2])
                if screwname in screwname_dct:
                    for idx in screwname_dct[screwname]:
                        if dct[idx][product_num["3"]] >= num:
                            response += f"{dct[idx]['品番']}  \n"
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        elif task_type == "3":
            with st.chat_message("user"):
                st.session_state.messages.append({"role": "user", "content" : user_input})
                st.markdown(user_input)
            response = ""
            response = "---  \n"
            response += f"{task['1']}場合は  \n以下の形式で入力してください  \n・品番  \n・仕様項目(対応する数字は以下のとおりです)  \n```python  \n1 : 全長,  \n2 : ネジ長さ,  \n3 : 最大取付物厚,  \n4 : 穿孔径,  \n5 : アンカー埋込み長さ,  \n6 : 穿孔深さ,  \n7 : 座金付ナット二面幅,  \n8 : 入数 (小箱), \n9 : 入数 (大箱),  \n10 : 入数 (大小),  \n11 : 標準価格,  \n```"
            response += "  \n---  \n"
            response += f"{task['2']}場合は  \n以下の形式で入力してください  \n・ねじの呼び  \n・取り付ける鉄板の厚さ"
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            with st.chat_message("user"):
                st.session_state.messages.append({"role": "user", "content" : user_input})
                st.markdown(user_input)
            response = "無効なタスク番号です。ヘルプは3で呼び出せます"
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
