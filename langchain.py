from langchain_openai import ChatOpenAI

llm=ChatOpenAI(model_name="gpt-4.1-mini", temperature=0)

#llm 단독호출
response = llm.invoke("what is langchain?")
print(response.content)