from models.sagt_models import ReplySuggestion, ChatHistory, CustomerInfo, EmployeeInfo
from datetime import datetime
from llm.llm_setting import chat_model as llm
from langchain_core.messages import AIMessage
from utils.agent_logger import get_logger

logger = get_logger("llm_suggest_chat")

def llm_chat_suggest(customer_info: CustomerInfo, employee_info: EmployeeInfo, chat_history: ChatHistory, current_time = None) -> ReplySuggestion:
    prompt = _chat_suggest_instructions.format(
        customer_info = customer_info.model_dump_json(),
        employee_info = employee_info.model_dump_json(),
        chat_history = chat_history.model_dump_json(),
        current_time = current_time or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        schema_json = ReplySuggestion.get_schema_json(),
        example_json = ReplySuggestion.get_example_json(),
    )
    logger.debug(f"prompt: {prompt}")
    # 生成回复建议
    generated_result: AIMessage = llm.invoke(prompt)
    logger.debug(f"generated_result: {generated_result}")

    if generated_result and generated_result.content:
        generated_reply_suggestion_json = generated_result.content
    else:
        generated_reply_suggestion_json = "{}"

    try:
        generated_reply_suggestion = ReplySuggestion.model_validate_json(generated_reply_suggestion_json)
        logger.info(f"generated_reply_suggestion: {generated_reply_suggestion.model_dump_json()}")
        return generated_reply_suggestion
    except Exception as e:
        logger.error(f"生成回复建议失败: {e}")
        return ReplySuggestion()


_chat_suggest_instructions = """
你是出色的酒类销售助理，擅长与客户进行聊天互动。除了销售产品，还特别擅长维护客户关系。

下面是近期与客户的聊天记录，请根据聊天记录，提供合适的回复建议 ReplySuggestion 。


这里是回复建议 ReplySuggestion 的数据结构定义：
-------------------
{schema_json}
-------------------

JSON对象示例：
-------------------
{example_json}
-------------------



【注意】要根据消息中的发送者sender和接收者receiver，分清楚消息是客户发送的还是销售人员发送的。
【注意】要根据消息中的发送时间msg_time，理解所讨论内容的时间背景。



请根据下面的客户信息，生成ReplySuggestion，具体要求：

1、【重要】您必须回复一个有效JSON对象
2、请不要在JSON对象前后包含任何文本。也不要包含“```json”或者“```”这样的文本。
3、json对象结构必须符合ReplySuggestion的定义。
4、请不要在json对象中包含任何未定义的字段。
5、请根据客户信息和聊天记录，生成回复建议。



这里是客户基础信息：
-------------------
{customer_info}
-------------------


这里是销售人员的基本信息：
-------------------
{employee_info}
-------------------


这里是客户和销售人员近期的对话记录：
-------------------
{chat_history}
-------------------




这是当前真实世界的时间，供你参考：
-------------------
{current_time}
-------------------

"""