import streamlit as st
import openai
import os

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


st.title("医院行政报告生成器")
st.caption("基于ChatGPT接口能力 %s" % openai.api_key)

"""
创建思路：
1. 展示对应提示词,MindMap、text、prompt
2. 选择温度,发散思维temp
3. 生成报告并改变check状态

仅供内部交流,作者 aorui
"""

MindMap = st.text_area('报告大纲', """# 标题:2019 年度医院行政工作大会上的报告
        ## 第一部分 2018 年度工作回顾
        ### 一、狠抓临床诊疗能力建设，医疗服务水平进一步提升 
        #### （一）着力服务内涵建设，质量效率不断提高
        #### （二）着力临床技术创新，诊疗能级不断提升
        #### （三）着力诊疗模式创新，打造综合诊治中心
        #### （四）着力服务流程创新，提高患者就医体验
        #### （五）着力应急能力建设，提升应急救援水平
        #### （六）着力护理能力建设，优质护理持续完善 
        #### （七）着力药品耗材监管，经济运营平稳过渡 
        ## 第二部分 谋划 2019 年主要工作
    """)

topic = st.text_input('主题',"""（一）着力服务内涵建设，质量效率不断提高""")


text = st.text_area('参考材料',"""1. CMI值:
-2018年医院CMI值为1.11。
-同比上升0.06。

2. 外科系统住院手术率：
-达到84.25%。
-同比上升2.15个百分点。

3. 医院三四级手术率：
-达到89.10%。
-同比上升0.9个百分点。

4. 日间手术人次数：
-2.71万人次。
-同比上升10.97%。
-占总手术人次比重达到29.42%。

5. 平均住院天数：
-6.54天。
-同比下降0.26天。

6. 申康关注的代表性病种：
-2018年申康关注54个代表性病种中,以下病种排名靠前：
-造血干细胞移植：全市排名第一。
-白内障加人工晶体植入术、玻璃体视网膜手术、喉部恶性肿瘤：全市排名第二。
-总计有11个病种位列前三名。

7. 医疗质量与安全监测平台实现医疗质量指标实时监测预警与疾病全诊疗环节质量评价。

8. 围手术期患者安全管理：
-组建围手术期安全管理团队。
-建立脑梗、心梗等高危人群筛查处置流程和VTE标准预防细则。
-完成VTE筛查组套设置,实现与HIS系统无缝衔接。
-编制《VTE防治手册》。
-目前术后高危患者VTE预防率达到90%。

9. 院感监测信息化及微生物室信息系统建设：
-提升指标动态监测功能。
-强化抗菌药物管控,通过临床应用实践MDT讨论会、抗菌药物使用监测网络等措施。
-加强感控培训。
-全年I类手术切口预防使用率28.8%,每百人天住院抗菌药物使用强度43.32,均较去年有明显下降。

10. 强化母婴医疗质量与安全：
-重点聚焦危重孕产妇管理。
-加强围产期监测、筛查与评估。
-建立多学科联动机制，提高危重孕产妇救治水平。
-加强新生儿出生缺陷、死亡管理。
-2018年收治危重孕产妇41例、出生缺陷儿8例,全年未发生危重孕产妇死亡事件。
""")



prompt = """
你是全中国文笔最好的三甲公立医院院长办公室的主任，\
你撰写的报告充分贯彻党的十九大精神，以习近平新时代中国特色社会主义思想为指引，\
深入学习贯彻习近平总书记关于推动长三角更高质量一体化发展重要指示精神。\
你的文笔缜密、数据详实。
文字风格上，尽量以第三方角度组织语言，不要总是提到“我们”。
接下来需要你撰写一份医院行政工作报告，提纲如下：
***{}***
你需要完成提纲中的这个主题：{},请根据该主题撰写出一个或多个段落,最后我会把所有段落整合在一起。
在这个主题中，我会提供给你一些参考数据，请你将这些数据都整合在段落中：
***{}***
你撰写的段落：
""".format(MindMap,topic,text)

with st.expander("查看提示词:"):
    st.write(prompt)

temp = st.slider('发散思维', 0.0, 1.0, step=0.1)

if st.button('生成'):
    response = get_completion(prompt,temp)
    st.write(response)
else:
    st.write('等待生成ing')


