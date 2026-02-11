import streamlit as st
import requests
from bs4 import BeautifulSoup
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

# 1. 환경 설정
load_dotenv("key.env")

# 2. 도구(Tool) 정의: 성균관대 공지사항 크롤러
@tool
def fetch_skku_notices(keyword: str) -> str:
    """
    성균관대학교 학부 공지사항 사이트에서 키워드로 공지사항을 검색하여 리스트를 반환합니다.
    '장학금', '등록금', '수강신청' 등 학교 소식이 궁금할 때 사용하세요.
    """
    # 성균관대 공지사항 검색 URL (키워드 파라미터 포함)
    url = f"https://www.skku.edu/skku/campus/skk_comm/notice01.do?mode=list&srSearchVal={keyword}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 공지사항 목록 추출 (사이트 구조에 따른 선택자 설정)
        notice_list = soup.select(".board-list-wrap table tbody tr")
        
        if not notice_list:
            return f"'{keyword}'에 대한 검색 결과가 없습니다."
        
        results = []
        for item in notice_list[:10]:  # 최신 10개만 추출
            title_tag = item.select_one(".td-subject a")
            date_tag = item.select_one(".td-date")
            
            if title_tag:
                title = title_tag.get_text(strip=True)
                link = "https://www.skku.edu/skku/campus/skk_comm/notice01.do" + title_tag['href']
                date = date_tag.get_text(strip=True) if date_tag else "날짜 불명"
                results.append(f"📌 제목: {title}\n📅 날짜: {date}\n🔗 링크: {link}")
        
        return "\n\n".join(results)
    
    except Exception as e:
        return f"공지사항을 가져오는 중 오류가 발생했습니다: {str(e)}"

# 3. Agent 설정
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
tools = [fetch_skku_notices]

# 4. Streamlit UI
st.set_page_config(page_title="SKKU 공지 비서", page_icon="🏫")
st.title("🏫 성균관대 실시간 공지사항 비서")

# 사이드바: 내 정보(필터링용)
with st.sidebar:
    st.header("👤 나의 프로필")
    user_info = st.text_area("나의 조건 (학과, 학년, 관심분야)", 
                            value="컴퓨터공학과 3학년, 성적 3.8, 장학금에 관심 많음.")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "어떤 공지사항을 찾아드릴까요? (예: 장학금, 졸업, 인턴)"}]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력 처리
if prompt := st.chat_input("키워드를 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 에이전트 실행
    # 사용자의 프로필 정보를 프롬프트에 주입하여 맞춤형 요약을 유도함
    prompt_template = f"""
    당신은 성균관대학교 학생을 돕는 'SKKU 공지 비서'입니다.
    
    [학생 정보]
    {user_info}
    
    [임무]
    1. 사용자가 묻는 키워드로 'fetch_skku_notices' 도구를 사용해 공지를 검색하세요.
    2. 검색된 공지 내용이 [학생 정보]에 해당되는지 분석하세요.
    3. 지원 가능한 장학금이나 유용한 정보가 있다면 강조해서 설명해주세요.
    4. 친절하게 학교 선배처럼 답변하세요.
    """

    agent = create_react_agent(model=llm, tools=tools, prompt=prompt_template)

    with st.chat_message("assistant"):
        with st.spinner("학교 홈페이지에서 공지를 찾는 중..."):
            response = agent.invoke({"messages": [HumanMessage(content=prompt)]})
            final_answer = response["messages"][-1].content
            st.markdown(final_answer)

    st.session_state.messages.append({"role": "assistant", "content": final_answer})