import streamlit as st
import openai
import json
import os
import pandas as pd



from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_key = os.getenv("OPENAI_API_KEY")

# print(openai.api_base)
# print(openai.api_key)

def get_completion(prompt='hi', temp=0, model="gpt-3.5-turbo-16k"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temp, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


# 导入测试数据
with open('data.json','r',encoding='utf8')as fp:
    json_data = json.load(fp)

st.title("行政报告提示词自助调试")
st.caption("基于ChatGPT接口能力 %s" % openai.api_key)

option = st.selectbox(
    '选择模板',
    ('医疗质量', '创新技术'))

temp_list = [x for x in json_data["template"] if x["tag"] == option]
key_data_list = [x for x in json_data["standard"] if x["tag"] == option]

title = st.text_input('参考标题', temp_list[0]["name"])
st.write('段落标题为:', title)

df = pd.DataFrame(key_data_list)
df.columns= ["编码","一级","三级","年度","业内平均水平","满分","统计单位"]
# dataframe操作
if option=='医疗质量':
    df["我的数据"] = json_data["add_data"]

# if st.button('填充数据'):
#     df["我的数据"] = json_data["add_data"]
#     st.write("已添加")
# else:
#     st.write('等待生成中……')

edited_df = st.data_editor(
    df,
    # column_config={
    #     "id":"指标编码",
    #     "tag": "一级指标",
    #     "name":"三级指标",
    #     "year": "年度",
    #     "IQR": "参考中位数",
    #     "full_mark": "满分",
    #     "unit":"单位",
    #     "Key Data":"我的数据",
    # },
    hide_index=True,
    num_rows="dynamic"
    )
st.write("请提交关键数据, 特殊自定义数据项目可在表格末尾添加并填报")

# 表格数据处理，空缺数据剔除

json_string = edited_df.to_json(orient="split", force_ascii= False)
json_data = json.loads(json_string)

txt = st.text_area('提示词调试(主题参数/关键数据参数)', 
'''你是中国三甲公立医院院长办公室的主任，正在撰写医院年度行政报告，
你撰写的报告充分贯彻党的十九大精神，
以习近平新时代中国特色社会主义思想为指引，
深入学习贯彻习近平总书记关于推动长三角更高质量一体化发展重要指示精神。
你的文笔缜密、数据详实。
文字风格上，尽量以第三方角度组织语言，不要总是提到'我们'。
接下来需要你撰写一份医院行政工作报告，主题如下：{}。 
请根据该主题撰写出一个或多个段落,最后我会把所有段落整合在一起。
在这个主题中，我会提供给你一些参考数据，其中"我的数据"是重点参考的字段，请你将这些数据都整合在段落中：
***{}***
你撰写的段落：
''',
    height=300,
    help="调整提示词构建，不断地逼近预期输出效果"
    )



prompt = txt.format(title,json_data)

with st.expander("查看提示词:"):
    st.write(prompt)



temp = st.slider('发散思维', 0.0, 1.0, step=0.1)

if st.button('生成'):
    response = get_completion(prompt,temp)
    st.write(response)
    st.download_button('Download text', prompt + "*"*10 + response)
else:
    st.write('等待生成ing')


