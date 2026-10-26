from enum import Enum

from typing_extensions import Literal
from langgraph.types import Command
from utils.agent_logger import get_logger
from langchain_core.runnables import RunnableConfig
from graphs.sagt_graph.sagt_state import SagtState, SagtStateField
from models.sagt_models import Intent, NodeResult
from llm.llm_intent_detect import llm_intent_detect

logger = get_logger("sagt_node")

# 节点名称
class NodeName(str, Enum):
    # 主图节点
    CLEANUP_STATE       = "cleanup_state"
    WELCOME_MESSAGE     = "sagt_welcome_message"
    INTENT_DETECTION    = "intent_detection"
    TASK_RESULT_CONFIRM = "task_result_confirm"

    # 子图节点（意图识别后，根据意图调用对应的子图）
    CHAT_SUGGESTION     = "chat_suggestion" ## 生成客户聊天建议
    KF_CHAT_SUGGESTION  = "kf_chat_suggestion" ## 生成客服聊天建议
    TAG_SUGGESTION      = "tag_suggestion" ## 生成客户标签
    PROFILE_SUGGESTION  = "profile_suggestion" ## 生成客户画像
    SCHEDULE_SUGGESTION = "schedule_suggestion" ## 生成客户日程
    NO_CLEAR_INTENTION  = "no_clear_intention" ## 未明确意图

# 意图列表（意图识别后，根据意图调用对应的子图）
class IntentDetection(str, Enum):
    CHAT_SUGGESTION     = NodeName.CHAT_SUGGESTION.value
    KF_CHAT_SUGGESTION  = NodeName.KF_CHAT_SUGGESTION.value
    TAG_SUGGESTION      = NodeName.TAG_SUGGESTION.value
    PROFILE_SUGGESTION  = NodeName.PROFILE_SUGGESTION.value
    SCHEDULE_SUGGESTION = NodeName.SCHEDULE_SUGGESTION.value
    NO_CLEAR_INTENTION  = NodeName.NO_CLEAR_INTENTION.value

def cleanup_state_node(state: SagtState, config: RunnableConfig):
    """清理状态节点"""
    logger.info("=== 清理状态 ===")
    return {
        ## 执行结果
        SagtStateField.NODE_RESULT: None,
        SagtStateField.TASK_RESULT: None,
        ## 信息Load
        SagtStateField.EMPLOYEE_INFO: None,
        SagtStateField.CHAT_HISTORY: None,
        SagtStateField.KF_CHAT_HISTORY: None,
        SagtStateField.ORDER_HISTORY: None,
        SagtStateField.TAG_SETTING: None,
        SagtStateField.CUSTOMER_INFO: None,
        SagtStateField.CUSTOMER_TAGS: None,
        SagtStateField.CUSTOMER_PROFILE: None,
        ## Intermediate Output 中间输出
        SagtStateField.SUGGESTION_PROFILE: None,
        SagtStateField.SUGGESTION_TAG: None,
        SagtStateField.SUGGESTION_CHAT: None,
        SagtStateField.SUGGESTION_KF: None,
        SagtStateField.SUGGESTION_SCHEDULE: None,
        SagtStateField.NOTIFY_CONTENT: None,
    }

def welcome_message(state: SagtState, config: RunnableConfig):
    """欢迎消息节点"""
    
    logger.info("=== 欢迎消息 ===")
    
    return {
        SagtStateField.NODE_RESULT: [NodeResult(
            execute_node_name=NodeName.WELCOME_MESSAGE.value,
            execute_result_code=0,
            execute_result_msg="您好，我是Sagt，很高兴为您服务",
            execute_exceptions=[]
        )]
    }

def intent_detection(state: SagtState, config: RunnableConfig) -> Command[Literal[*[intent.value for intent in IntentDetection]]]:
    """意图检测节点"""
    
    logger.info("=== 意图检测 ===")
    
    intents=[
        Intent(intent_id=IntentDetection.CHAT_SUGGESTION.value, intent_description="我是销售人员，正在和客户沟通，我需要知道如何回复比较合适"),
        Intent(intent_id=IntentDetection.KF_CHAT_SUGGESTION.value, intent_description="我是企业客服，在帮助客户解决问题，请帮助我生成客服回复建议"),
        Intent(intent_id=IntentDetection.TAG_SUGGESTION.value, intent_description="我的客户情况有更新，我需要更客户标签"),
        Intent(intent_id=IntentDetection.PROFILE_SUGGESTION.value, intent_description="我的客户情况有更新，我需要更新客户画像"),
        Intent(intent_id=IntentDetection.SCHEDULE_SUGGESTION.value, intent_description="我和客户沟通过程中，我需要创建日程，方便提醒我跟进事项"),
        Intent(intent_id=IntentDetection.NO_CLEAR_INTENTION.value, intent_description="我想咨询一些问题，或者没有明确的意图，仅仅是聊聊天")
    ]

    task_input = state.get(SagtStateField.TASK_INPUT, "")

    # 任务值直接表明意图，则直接跳转到对应的意图节点
    if task_input in [intent.value for intent in IntentDetection]:
        return Command(goto=task_input)

    ## 暂时不做意图检测，直接返回未明确意图，如果不在意图列表中，则默认设置为未明确意图
    ##intent = llm_intent_detect(task_input, intents)

    ## 非任务值，直接返回未明确意图
    intent_id = IntentDetection.NO_CLEAR_INTENTION.value
    
    # 如果意图不在意图列表中，则默认设置为未明确意图    
    if not intent_id in [intent.value for intent in IntentDetection]:
        intent_id = IntentDetection.NO_CLEAR_INTENTION.value 
    
    return Command(goto = intent_id)
    

# 任务结果确认
def task_result_confirm(state: SagtState, config: RunnableConfig):
    """任务结果确认节点"""
    
    logger.info("=== 任务结果确认 ===")

    return {
        SagtStateField.NODE_RESULT: [NodeResult(
            execute_node_name=NodeName.TASK_RESULT_CONFIRM.value,
            execute_result_code=0,
            execute_result_msg="任务已完成，希望您能满意",
            execute_exceptions=[]
        )]
    }