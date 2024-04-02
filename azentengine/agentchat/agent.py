from typing import Any, Dict, List, Optional, Protocol, Union, runtime_checkable

@runtime_checkable
class Agent(Protocol):
    """
    Agent 是可以和其他 Agent 进行沟通，并且也可以执行操作(Action)
    不同类型的 Agent 在 receive 方法里会采取不同动作(Action)
    """

    @property
    def name(self) -> str:
        """ agent 名称"""


    @property
    def description(self) -> str:
        """关于 agent 基本信息主要用于 group chat 设置来描述该 Agent"""

    def send(
        self,
        message: Union[Dict[str, Any], str],
        recipient: "Agent",
        request_reply: Optional[bool] = None,
    ) -> None:
        """给其他 agent 发送消息.

        Args:
            message (dict or str): 要发送的消息，如果是 dict 类型，应该是可以 JSON 序列化的，而且需要遵循 OpenAI's ChatCompletion schema.
            recipient (Agent): 指定接受消息的 Agent.
            request_reply (bool): 是否需要接收方给予回复.
        """
        ...
    async def a_send(
        self,
        message: Union[Dict[str, Any], str],
        recipient: "Agent",
        request_reply: Optional[bool] = None,
    ) -> None:
        """(异步)发送消息给其他 agent"""
        ...

    def receive(
        self,
        message: Union[Dict[str, Any], str],
        sender: "Agent",
        request_reply: Optional[bool] = None,
    ) -> None:
        """从其他用 agent 接受消息"""
        ...
            
    async def a_receive(
        self,
        message: Union[Dict[str, Any], str],
        sender: "Agent",
        request_reply: Optional[bool] = None,
    ) -> None:
        """(Async) Receive a message from another agent."""

        ...

    def generate_reply(
        self,
        messages: Optional[List[Dict[str, Any]]] = None,
        sender: Optional["Agent"] = None,
        **kwargs: Any,
    ) -> Union[str, Dict[str, Any], None]:
        """根据收到的信息生成回复
        
        """
        ...

    async def a_generate_reply(
        self,
        messages: Optional[List[Dict[str, Any]]] = None,
        sender: Optional["Agent"] = None,
        **kwargs: Any,
    ) -> Union[str, Dict[str, Any], None]:
        ...

@runtime_checkable
class LLMAgent(Agent, Protocol):
    """(In preview)  LLM agent 接口"""

    @property
    def system_message(self) -> str:
        """The system message of this agent."""

    def update_system_message(self, system_message: str) -> None:
        """更新 agent's system message.

        Args:
            system_message (str): system message for inference.
        """