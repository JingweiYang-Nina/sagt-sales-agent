import operator
from typing import TypedDict, Annotated, List
from graphs.sagt_graph.sagt_state import SagtStateField
from models.sagt_models import CustomerInfo, ScheduleSuggestion, ChatHistory, TaskResult, NodeResult
from enum import Enum

class SubScheduleStateField(str, Enum):
    """子图状态字段名称枚举，引用主图字段值以保持一致性"""
    # 输入字段 - 引用主图字段
    CUSTOMER_INFO       = SagtStateField.CUSTOMER_INFO.value
    CHAT_HISTORY        = SagtStateField.CHAT_HISTORY.value
    # 中间字段
    SUGGESTION_SCHEDULE = SagtStateField.SUGGESTION_SCHEDULE.value
    # 输出字段 - 引用主图字段
    TASK_RESULT         = SagtStateField.TASK_RESULT.value
    NODE_RESULT         = SagtStateField.NODE_RESULT.value

class SubScheduleInputState(TypedDict):
    customer_info:      CustomerInfo
    chat_history:       ChatHistory

class SubScheduleIntermediateState(TypedDict):
    suggestion_schedule: ScheduleSuggestion

class SubScheduleOutputState(TypedDict):
    task_result: TaskResult
    node_result: Annotated[List[NodeResult], operator.add]

# 使用多重继承，自动合并所有字段
class SubScheduleState(SubScheduleInputState, SubScheduleIntermediateState, SubScheduleOutputState):
    """
    完整的子图状态，包含输入和输出字段
    继承自 SubScheduleInputState, SubScheduleIntermediateState 和 SubScheduleOutputState
    """
    pass