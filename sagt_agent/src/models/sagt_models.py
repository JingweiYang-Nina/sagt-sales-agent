from typing import List, Dict, Any
from pydantic import BaseModel, Field
from typing_extensions import Annotated
from models.sagt_base_model import SagtBaseModel

# 使用 Annotated 类型约束
TimeStr = Annotated[str, Field(pattern=r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')]

#####  员工  #####
class EmployeeInfo(SagtBaseModel):
    ''' 员工信息 '''
    user_id: str = Field(default="", description="用户ID")
    name: str = Field(default="", description="名称")


#####  标签  #####
class TagInfo(SagtBaseModel):
    ''' 标签信息 '''
    tag_id: str = Field(default="", description="标签ID")
    tag_name: str = Field(default="", description="标签名称")
    tag_reason: str = Field(default="", description="标签建议原因")

class TagSetting(SagtBaseModel):
    ''' 全局标签设置 '''
    tag_setting: List[TagInfo] = Field(default=[], description="全局标签列表")

class TagSuggestion(SagtBaseModel):
    ''' 标签建议 '''
    tag_ids_add: List[TagInfo] = Field(default=[], description="建议添加的标签列表")
    tag_ids_remove: List[TagInfo] = Field(default=[], description="建议删除的标签列表")

    @classmethod
    def get_example_instance(cls):
        return cls(
            tag_ids_add=[
                    TagInfo(tag_id="tag_id_1", tag_name="tag_name_1", tag_reason="建议添加该标签的原因"),
                    TagInfo(tag_id="tag_id_2", tag_name="tag_name_2", tag_reason="建议添加该标签的原因")
                ],
            tag_ids_remove=[
                    TagInfo(tag_id="tag_id_3", tag_name="tag_name_3", tag_reason="建议删除该标签的原因"),
                    TagInfo(tag_id="tag_id_4", tag_name="tag_name_4", tag_reason="建议删除该标签的原因")
                ]
        )


#####  profile  #####
class ProfileItem(SagtBaseModel):
    ''' profile子项 '''
    item_name: str = Field(default="", description="profile子项的名称")
    item_value: str = Field(default="", description="profile子项的值")


#####  客户  #####
class CustomerInfo(SagtBaseModel):
    ''' 客户信息 '''
    external_id: str = Field(default="", description="外部用户ID")
    union_id: str = Field(default="", description="union_id")
    follow_user_id: str = Field(default="", description="关注用户ID")
    nick_name: str = Field(default="", description="昵称")

class CustomerTags(SagtBaseModel):
    ''' 客户标签 '''
    customer_tags: List[TagInfo] = Field(default=[], description="客户标签")

class CustomerProfile(SagtBaseModel):
    ''' 客户 profile '''
    profile_items: List[ProfileItem] = Field(default=[], description="profile子项的列表")

    @classmethod
    def get_example_instance(cls):
        return cls(
            profile_items=[
                    ProfileItem(item_name="姓名", item_value="张博士"),
                    ProfileItem(item_name="年龄", item_value="25"),
                    ProfileItem(item_name="性别", item_value="男"),
                    ProfileItem(item_name="婚姻状况", item_value="未婚"),
                    ProfileItem(item_name="兴趣爱好", item_value="运动、音乐"),
                    ProfileItem(item_name="教育程度", item_value="本科"),
                    ProfileItem(item_name="饮酒频率", item_value="每周一次"),
                    ProfileItem(item_name="饮酒场景", item_value="聚会、独自小酌"),
                    ProfileItem(item_name="饮酒金额", item_value="100元"),
                    ProfileItem(item_name="饮酒口感偏好", item_value="醇厚"),
                    ProfileItem(item_name="饮酒购买渠道", item_value="线下实体店、线上电商平台"),
                    ProfileItem(item_name="饮食习惯", item_value="无忌口、偏好的菜系等"),
                    ProfileItem(item_name="出行方式", item_value="自驾、公交、地铁"),
                    ProfileItem(item_name="宠物情况", item_value="是否养宠物及宠物种类"),
                    ProfileItem(item_name="娱乐活动偏好", item_value="看电影、唱K等具体活动"),
                    ProfileItem(item_name="家庭成员", item_value="如配偶、子女等"),
                    ProfileItem(item_name="常喝的酒的种类", item_value="如白酒、红酒、啤酒等"),
                    ProfileItem(item_name="喜欢的酒的品牌", item_value="如茅台、五粮液等"),
                    ProfileItem(item_name="消费频率", item_value="如每周一次、每月几次等"),
                    ProfileItem(item_name="消费场景", item_value="如聚会、独自小酌等"),
                    ProfileItem(item_name="每次消费的大致金额", item_value="如100元"),
                    ProfileItem(item_name="对酒的口感偏好", item_value="如醇厚、清爽等"),
                    ProfileItem(item_name="购买渠道", item_value="如线下实体店、线上电商平台等")
                ]
        )


#####  聊天对话  #####
class ChatMessage(SagtBaseModel):
    ''' 聊天消息 '''
    sender: str = Field(default="", description="发送者")
    receiver: str = Field(default="", description="接收者")
    content: str = Field(default="", description="内容")
    msg_time: TimeStr = Field(default="", description="消息时间")

class ReplySuggestion(SagtBaseModel):
    ''' 回复建议 '''
    reply_content: str = Field(default="", description="回复内容")
    reply_reason: str = Field(default="", description="回复原因")

    @classmethod
    def get_example_instance(cls):
        return cls(
            reply_content="回复内容",
            reply_reason="回复原因"
        )

class ChatHistory(SagtBaseModel):
    ''' 聊天记录 '''
    chat_msgs: List[ChatMessage] = Field(default=[], description="聊天记录")

class KFChatHistory(SagtBaseModel):
    ''' 客服聊天记录 '''
    kf_chat_msgs: List[ChatMessage] = Field(default=[], description="客服聊天记录")

#####  订单  #####
class OrderInfo(SagtBaseModel):
    ''' 订单信息 '''
    order_id: str = Field(default="", description="订单ID")
    order_products: List[str] = Field(default="", description="订单产品")
    order_create_time: TimeStr = Field(default="", description="订单创建时间")

class OrderHistory(SagtBaseModel):
    ''' 订单历史 '''
    orders: List[OrderInfo] = Field(default=[], description="历史订单记录")
    
#####  日程  #####

class ScheduleSuggestion(SagtBaseModel):
    ''' 日程建议 '''
    title: str = Field(default="",title="Title", description="日程标题")
    start_time: TimeStr = Field(default="",title="Start Time", description="开始时间，格式 yyyy-MM-dd HH:mm:ss")
    duration: int = Field(default=30,title="Duration", description="持续时间，单位分钟")
    schedule_reason: str = Field(default="",title="Schedule Reason", description="日程建议原因")

    @classmethod
    def get_example_instance(cls):
        return cls(
            title="日程标题，包含具体事项说明",
            start_time="2025-08-01 10:00:00",
            duration=60,
            schedule_reason="日程建议原因"
        )

#####  讨论  #####

class JustTalkOutput(SagtBaseModel):
    ''' 讨论应答 '''
    just_talk_output: str = Field(default="", description="讨论应答")
    
    @classmethod
    def get_example_instance(cls):
        return cls(
            just_talk_output="输出应答内容"
        )


#####  意图检测  #####
class Intent(SagtBaseModel):
    ''' 意图 '''
    intent_id: str = Field(default="", description="意图ID")
    intent_description: str = Field(default="", description="意图描述")

    @classmethod
    def get_example_instance(cls):
        return cls(
            intent_id="chat_suggestion",
            intent_description="生成聊天建议"
        )


class TaskResult(SagtBaseModel):
    task_result: str = Field(default="", description="任务结果")
    task_result_explain: str = Field(default="", description="任务结果解释")
    task_result_code: int = Field(default=1, description="任务结果代码，0: 结果有效，1: 结果无效")

class NodeResult(SagtBaseModel):
    ''' 节点执行 '''
    execute_node_name: str = Field(default="", description="节点名称")
    execute_result_code: int = Field(default=1, description="节点执行结果代码，0: 成功，1: 失败")
    execute_result_msg: str = Field(default="", description="节点执行结果消息")
    execute_exceptions: List[str] = Field(default=[], description="节点执行异常信息")
    