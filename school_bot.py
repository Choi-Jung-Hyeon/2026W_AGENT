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

# 2. 도구(Tool) 정의: 성균관대 공지사항 크롤러 (보완 버전)
@tool
def fetch_skku_notices(keyword: str) -> str:
    """
    성균관대학교 학부 공지사항 사이트에서 실시간으로 키워드를 검색합니다.
    '장학', '채용', '행사' 등 학교 소식을 찾을 때 사용하세요.
    """
    # [핵심] 브라우저처럼 보이기 위한 헤더 설정
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    }
    
    # 검색 파라미터를 포함한 URL
    url = f"https://www.skku.edu/skku/campus/skk_comm/notice01.do?mode=list&srSearchVal={keyword}"
    
    try:
        # 헤더를 포함하여 요청 보내기
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 공지사항 목록 추출 (성균관대 사이트의 테이블 구조 타겟팅)
        notice_list = soup.select(".board-list-wrap table tbody tr")
        
        # '데이터가 없습니다' 메시지가 있는지 확인
        if not notice_list or "데이터가 없습니다" in soup.get_text():
            return f"현재 '{keyword}'에 대한 검색 결과가 없습니다. '장학'이나 '취업'처럼 짧은 단어로 검색해 보세요."
        
        results = []
        for item in notice_list[:8]:  # 최신 8개만 추출
            title_tag = item.select_one(".td-subject a")
            date_tag = item.select_one(".td-date")
            
            if title_tag:
                title = title_tag.get_text(strip=True)
                # 상대 경로를 절대 경로로 변환
                link = "https://www.skku.edu/skku/campus/skk_comm/notice01.do" + title_tag['href']
                date = date_tag.get_text(strip=True) if date_tag else "날짜 불명"
                results.append(f"📌 제목: {title}\n📅 날짜: {date}\n🔗 링크: {link}")
        
        return "\n\n".join(results)
    
    except Exception as e:
        return f"공지사항을 가져오는 중 기술적 오류가 발생했습니다: {str(e)}"

# 3. Agent 설정
# [참고] 사용자님의 환경에 맞는 모델명을 사용합니다.
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

# 대화 내용 출력
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력 처리
if prompt := st.chat_input("키워드를 입력하세요..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 에이전트 시스템 프롬프트 구성
    prompt_template = f"""
    당신은 성균관대학교 학생을 돕는 'SKKU 공지 비서'입니다.
    
    [학생 정보]
    {user_info}
    
    [임무]
    1. 사용자가 묻는 키워드로 'fetch_skku_notices' 도구를 사용해 공지를 검색하세요.
    2. 검색된 공지의 제목을 보고 [학생 정보]와 관련이 있는지(전공, 학년 등) 판단하세요.
    3. 만약 '장학' 관련 검색이라면, 학생의 성적(3.8)이나 학과에 맞는 공지를 우선적으로 추천하세요.
    4. 친절하게 학교 선배처럼 말투를 사용하고, 상세 내용을 보려면 링크를 클릭하라고 안내하세요.
    """

    # 에이전트 생성
    agent = create_react_agent(model=llm, tools=tools, prompt=prompt_template)

    with st.chat_message("assistant"):
        with st.spinner("학교 홈페이지를 꼼꼼히 뒤져보는 중..."):
            # 에이전트 실행
            response = agent.invoke({"messages": [HumanMessage(content=prompt)]})
            final_answer = response["messages"][-1].content
            st.markdown(final_answer)

    # 대화 기록 저장
    st.session_state.messages.append({"role": "assistant", "content": final_answer})