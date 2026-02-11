from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv("key.env")

llm=ChatOpenAI(model_name="gpt-4.1-mini", temperature=0)
prompt=ChatPromptTemplate.from_messages([
    ("system", "당신은 친절한 선생님입니다. 초등학생도 이해할 수 있게 설명해주세요."),
    ("user", "{question}"),
])

#prompt와 llm을 파이프로 연결
chain = prompt | llm

#llm 단독호출
response = chain.invoke("양자역학이 뭐야?")
print(response.content)