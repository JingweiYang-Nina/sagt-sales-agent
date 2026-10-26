import operator
from typing import TypedDict, Annotated, List
from graphs.sagt_graph.sagt_state import SagtStateField
from models.sagt_models import ChatHistory, KFChatHistory, OrderHistory, CustomerProfile, CustomerTags, TaskResult, NodeResult
from enum import Enum


class SubProfileStateField(str, Enum):
    """子图状态字段名称枚举"""
    
    ## 输入字段
    CHAT_HISTORY = SagtStateField.CHAT_HISTORY.value
    KF_CHAT_HISTORY = SagtStateField.KF_CHAT_HISTORY.value
    ORDER_HISTORY = SagtStateField.ORDER_HISTORY.value
    CUSTOMER_TAGS = SagtStateField.CUSTOMER_TAGS.value
    CUSTOMER_PROFILE = SagtStateField.CUSTOMER_PROFILE.value
    
    ## 中间输出字段
    NOTIFY_CONTENT = SagtStateField.NOTIFY_CONTENT.value
    SUGGESTION_PROFILE = SagtStateField.SUGGESTION_PROFILE.value

    ## 输出字段
    TASK_RESULT = SagtStateField.TASK_RESULT.value
    NODE_RESULT = SagtStateField.NODE_RESULT.value
class SubProfileInputState(TypedDict):
    chat_history:       ChatHistory
    kf_chat_history:    KFChatHistory
    order_history:      OrderHistory
    customer_tags:      CustomerTags
    customer_profile:   CustomerProfile

class SubProfileIntermediateOutputState(TypedDict):
    notify_content:     str
    suggestion_profile: CustomerProfile


class SubProfileOutputState(TypedDict):
    task_result: TaskResult
    node_result: Annotated[List[NodeResult], operator.add]

# 使用多重继承，自动合并所有字段
class SubProfileState(SubProfileInputState, SubProfileIntermediateOutputState, SubProfileOutputState):
    """
    完整的子图状态，包含输入和输出字段
    继承自 SubProfileInputState, SubProfileIntermediateOutputState 和 SubProfileOutputState
    """
    pass