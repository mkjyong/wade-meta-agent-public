from autogen import AssistantAgent, UserProxyAgent, GroupChatManager, GroupChat
from pydantic import BaseModel

# llm_config 설정
llm_config = {
    "config_list": [
        {
            "model": "gpt-4o-mini",
            "api_key": "api_key",
        }
    ]
}

# 에이전트 역할 정의
prompt_template_creator = """
당신의 역할은 AI agent용 프롬프트 생성 전문가입니다.
사용자로부터 받은 하이레벨 요청을 기반으로, 그 요청을 처리할 수 있는 AI 에이전트의 프롬프트를 작성하세요.
만약 외부 데이터 연결 및 외부 툴 연결이 필요하다면 알려주세요.
대화 응답은 생성하지 마세요.
"""

prompt_template_reviewer = """
당신의 역할은 사용자 관점에서 AI 에이전트 프롬프트를 검토하는 전문가입니다.
프롬프트가 사용자의 요청을 충족시키는지 확인하고, 필요하다면 수정 제안을 포함한 결과를 반환하세요.
"""

prompt_template_ux_expert = """
당신의 역할은 사용자 경험(UX) 전문가입니다.
입력으로는 생성된 프롬프트가 들어올 것입니다.
이 프롬프트가 사용자 친화적인지, 직관적인지 검토하고 개선 사항이 있다면 제안하세요.
그 개선 내용을 실행하기 위해 좋은 프롬포트를 추가해주세요
"""

# Web3 비즈니스 전문가
prompt_template_web3_business_expert = """
당신의 역할은 Web3 비즈니스 전문가입니다.
입력으로는 Web3와 관련된 프롬프트가 들어올 것입니다.
비즈니스 관점에서 이 프롬프트가 적절한지 검토하고, 필요한 경우 Web3 비즈니스 모델 및 전략 관련 제안을 추가하세요.
그 전략 및 제안을 실행하기 위해 좋은 프롬포트를 추가해주세요
"""

# Web3 기술 전문가
prompt_template_web3_technical_expert = """
당신의 역할은 Web3 기술 전문가입니다.
입력으로는 Web3와 관련된 프롬프트가 들어올 것입니다.
기술적 관점에서 이 프롬프트가 적절한지 검토하고, 필요한 경우 스마트 컨트랙트, 블록체인 기술, 토큰 설계 등의 기술적 요소를 추가하세요.
그 필요한 기술적 요소를 실행하기 위해 좋은 프롬포트를 추가해주세요
"""

# AI Agent 비즈니스 전문가
prompt_template_ai_agent_business_expert = """
당신의 역할은 AI 에이전트 비즈니스 전문가입니다.
입력으로는 AI 에이전트와 관련된 프롬프트가 들어올 것입니다.
비즈니스 관점에서 이 프롬프트가 적절한지 검토하고, 필요한 경우 AI 에이전트와 관련된 비즈니스 모델 및 시장 전략을 추가하세요.
그 전략을 실행하기 위해 좋은 프롬포트를 추가해주세요
"""

# AI Agent 기술 전문가
prompt_template_ai_agent_technical_expert = """
당신의 역할은 AI 에이전트 기술 전문가입니다.
입력으로는 AI 에이전트와 관련된 프롬프트가 들어올 것입니다.
기술적 관점에서 이 프롬프트가 적절한지 검토하고, 필요한 경우 기술적 구현에 필요한 세부 사항 및 개선점을 추가하세요.
그 개선점을 실행하기 위해 좋은 프롬포트를 추가해주세요
"""

# 에이전트 생성
creator_agent = AssistantAgent(
    name="PromptCreator",
    system_message=prompt_template_creator,
    llm_config=llm_config,
)

reviewer_agent = AssistantAgent(
    name="PromptReviewer",
    system_message=prompt_template_reviewer,
    llm_config=llm_config,
)

ux_expert_agent = AssistantAgent(
    name="UXExpert",
    system_message=prompt_template_ux_expert,
    llm_config=llm_config,
)

web3_business_expert_agent = AssistantAgent(
    name="Web3BusinessExpert",
    system_message=prompt_template_web3_business_expert,
    llm_config=llm_config,
)

web3_technical_expert_agent = AssistantAgent(
    name="Web3TechnicalExpert",
    system_message=prompt_template_web3_technical_expert,
    llm_config=llm_config,
)

ai_agent_business_expert_agent = AssistantAgent(
    name="AIAgentBusinessExpert",
    system_message=prompt_template_ai_agent_business_expert,
    llm_config=llm_config,
)

ai_agent_technical_expert_agent = AssistantAgent(
    name="AIAgentTechnicalExpert",
    system_message=prompt_template_ai_agent_technical_expert,
    llm_config=llm_config,
)

# 사용자 프록시
user_proxy = UserProxyAgent(
    name="UserProxy",
    code_execution_config=False
)

# 협업을 위한 GroupChat 생성
group_chat = GroupChat(
    agents=[creator_agent, reviewer_agent, web3_business_expert_agent, web3_technical_expert_agent, ai_agent_business_expert_agent, ai_agent_technical_expert_agent, ux_expert_agent],
    messages=[],  # 초기 메시지 없음
    max_round=8  # 최대 대화 라운드
)

# GroupChatManager를 사용해 그룹 대화 관리
manager = GroupChatManager(groupchat=group_chat)


class UserInput(BaseModel):
    user_input: str


def process_input(input_data):
    # 사용자 입력을 그룹 대화에 전달
    user_proxy.initiate_chat(
        manager,
        message=input_data
    )
    # 최종 메시지 반환
    final_message = manager.groupchat.messages[-1]  # 마지막 메시지 가져오기
    return final_message["content"]


if __name__ == "__main__":
    # requirement = """
    # 밈코인 배포해주는 ai agent만들어주세요. sns 기반으로 유저의 요청이 있다면 그 요청을 바탕으로 ERC20 토큰 배포를 위해 심볼과 이름 정보를 추출하거나 만들어내는 에이전트 프롬포트 생성
    # """

    requirement = """
    sns에 피드를 자동으로 생성해주는 ai agent를 만들어주세요. web3 게임 관련된 sns feed를 주제로하고 있어.
    """
    result = process_input(requirement)
