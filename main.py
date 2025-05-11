import streamlit as st
import pandas as pd
from tabulate import tabulate
from principle import principles
from datetime import datetime

st.title("女主无cp/无男主小说评分")

#sidebar

with st.sidebar:
    st.header("评分规则")
    principle = st.markdown("""
### 1.打分为减分制。
完结小说满分为10分，读者根据阅读后体验和感受，给一个印象得分，\n
然后再根据组规进行减分，\n
即最终得分=印象分-减分项，最终得分<<10分。\n
【谨慎打8分以上，禁止分数膨胀】

### 2.打分规则。
各项基础扣分分值为1'，情节严重的可以增加扣分分值，无上限，\n
必须列出各项减分项存在与否。\n
【❗❗❗注意：没有明确标注/提出的、不完全的、模棱两可的即需要扣分，请各位打分人严格执行！！\n

""")

#ratings

book_name = st.text_input("请输入书名：")
impressed_rate = st.number_input("请输入你的印象分：", max_value=10)
book_author = st.text_input("请输入作者姓名：")
book_plate = st.text_input("请输入作品发布平台：")
ich = st.text_input("评分人：")
now = datetime.now().date()

#count

answers = []
remarks = []
for i, principle in enumerate(principles, 1):
    q = st.radio(f"{i}、{principle}", ["有", "没有"], index=None)
    r = st.text_area(f"备注{i}")
    answers.append(q)
    remarks.append(r)

df = pd.DataFrame({"序号": list(range(1, 26)),
                   "评分准则": principles,
                   "我的评判": answers,
                   "备注": remarks
                   })

y, n = "有", "没有"

r = [0] * 26
for i, answer in enumerate(answers[:22], 1):
    if answer == y:
        r[i] = -1

for i, answer in enumerate(answers[22:], 23):
    if answer == n:
        r[i] = -1

extra_rate = st.number_input("因为其它恶劣请节我还想减分：", max_value=10)
paragraph = st.text_area("备注：")
sum_rate = impressed_rate + sum(r) - extra_rate
st.write(f"最终评分为：{sum_rate}")

comment = st.text_area("爱女姐有话说：")

header = (
    f"书名：{book_name} | 作者：{book_author} | 平台：{book_plate} | 最终评分：{sum_rate} 分 | {ich}印象分：{impressed_rate}| 评分日期:{now}")
footer = (f"爱女姐有话说：{comment}")


# HTML


def generate_html_table(df):
    # 生成HTML表格的各个部分
    cols = len(df.columns)

    # 表头部分，包括标题行
    head = f'''
    <table style="border-collapse: collapse; width: 100%;">
    <thead>
        <tr>
            <td colspan="{cols}" style="padding: 10px; text-align: center; font-weight: bold; background-color: #f7f7f7;">
                {header}
            </td>
        </tr>
        <tr>
    '''

    # 添加列标题
    for col in df.columns:
        head += f'<th style="padding: 10px; text-align: center; border: 1px solid black;">{col}</th>'

    head += '</tr></thead><tbody>'

    # 表格主体
    body = ''
    for _, row in df.iterrows():
        body += '<tr>'
        for item in row:
            body += f'<td style="padding: 10px; text-align: center; border: 1px solid black;">{item if item is not None else ""}</td>'
        body += '</tr>'

    # 表尾部分，包括评论行
    foot = f'''
    </tbody>
    <tfoot>
        <tr>
            <td colspan="{cols}" style="padding: 10px; text-align: left; font-weight: bold; background-color: #f7f7f7;">
                {footer}
            </td>
        </tr>
    </tfoot>
    </table>
    '''

    # 组合完整表格
    table_html = head + body + foot

    return f"<html><body>{table_html}</body></html>"


html_table = generate_html_table(df)

button = st.button("生成HTML表格")
if button:
    st.markdown(html_table, unsafe_allow_html=True)
