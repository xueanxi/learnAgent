from autogen import AssistantAgent,Agent
import re
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generator,
    Iterable,
    Literal,
    Optional,
    TypeVar,
    Union,
)

class FilteredUserProxyAgent(AssistantAgent):
    '''
    去掉模型思维链的Agent
    '''
    def receive(self,
            message: Union[dict[str, Any], str],
            sender: Agent,
            request_reply: Optional[bool] = None,
            silent: Optional[bool] = False,):
        
        # 这里可以处理，从发送者接受到的信息
        super().receive(message, sender,request_reply,silent)
    
    def send(self,message: Union[dict[str, Any], str],
            recipient: Agent,
            request_reply: Optional[bool] = None,
            silent: Optional[bool] = False,):

        # 发送出去的内容，需要去掉思维链部分的内容
        result = re.sub(r"<think>.*?</think>\s*", "", message, flags=re.DOTALL)
        super().send(result,recipient,request_reply,silent)