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
df.columns= ["编码","一级","三级","项目定义","国家导向","年度","业内平均水平","满分标准","统计单位"]
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

# 表格数据处理,空缺数据剔除

json_string = edited_df.to_json(orient="split", force_ascii= False)
json_data = json.loads(json_string)

txt = st.text_area('提示词调试(主题参数/关键数据参数)', 
'''你是综合性三甲医院的资深管理者,拥有十年的行业经验,每一年的医院行政报告都是由你负责制作。
行政报告是用于在年度总结大会上对整个医院领导和全体医务人员作出发展和业绩汇报。
这里会提供段落主题和医院的统计数据,你的任务是利用数据撰写医院年度行政报告的一个段落。
要解决此问题,请执行以下操作：
-首先,将提供的数据进行整理,整理为Markdown格式的数据。
-然后,参考示例的词频,尽量用提供的词频构建内容。
-最后,忽略数据中的"满分数据",将整理过的数据扩写成一个段落,字数控制在400字以内。
在你自己参考示例段落和词频、整理好数据之前,不要开始扩写段落。

使用以下格式完成任务：
报告段落标题:
```
报告段落标题在这里
```
原始数据:
```
原始数据在这里
```
整理过的数据:
```
整理过的数据在这里
```
扩写段落：
```
扩写段落在这里
-首先统一说明数据的年份；
-然后将数据依次罗列；
-忽略"满分"项目,也不要试图编造数据；
-在扩写段落时,尽量使用我提供给你的一批高频词汇组织内容,具体词汇如下:
('医院', 165), ('工作', 117), ('建设', 103), ('管理', 94), ('医疗', 73), ('临床', 66), ('推进', 64), ('服务', 64), ('进一步', 60), ('学科', 57), ('发展', 56), ('中心', 54), ('患者', 49), ('提升', 46), ('2018', 43), ('重点', 42), ('质量', 42), ('手术', 42), ('特色', 37), ('项目', 37), ('完善', 36), ('文化', 34), ('病种', 33), ('创新', 32), ('诊疗', 32), ('落实', 32), ('技术', 30), ('评审', 30), ('上海市', 29), ('品牌', 28), ('人才', 28), ('建立', 28), ('全国', 28), ('宣传', 28), ('一是', 28), ('文明', 28), ('上海', 27), ('系统', 27), ('公济', 27), ('二是', 27), ('2019', 26), ('持续', 26), ('平台', 26), ('流程', 26), ('三是', 26), ('媒体', 26), ('优化', 25), ('创建', 24), ('年度', 23), ('中国', 22), ('研究', 22), ('制度', 22), ('核心', 21), ('传播', 21), ('精神', 20), ('精准', 20), ('体系', 20), ('国家', 19), ('提高', 19), ('团队', 19), ('实施', 19), ('模式', 19)；
```

报告段落标题:
```
{}
```
原始数据:
```
{}
```
整理过的数据：
''',
    height=300,
    help="调整提示词构建,不断地逼近预期输出效果"
    )



prompt = txt.format(title,json_data)

with st.expander("查看提示词:"):
    st.write(prompt)



temp = st.slider('发散思维', 0.0, 1.0, step=0.1)

if st.button('生成'):
    response = get_completion(prompt,temp)
    st.write(response)
    st.download_button('Download text', prompt + "*"*10 + "temp:"+ str(temp) +"*"*10 + response)
else:
    st.write('等待生成ing')


