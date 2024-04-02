import asyncio
import copy
import functools
import inspect
import json
import logging
import re
import warnings
from collections import defaultdict
from functools import partial
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, Type, TypeVar, Union

from .agent import Agent, LLMAgent


__all__ = ("ConversableAgent",)

F = TypeVar("F", bound=Callable[..., Any])


class ConversableAgent(LLMAgent):
    """(In preview) A class for generic conversable agents which can be configured as assistant or user proxy.
    主要有两类 agent 一类为 assistant 或者 user prooxy
    只要消息不是终止消息(termination msg)agent 通常需要对发送方给予回复
    接下来定义的 AssistantAgent 和 UserProxyAgent 都是这个类的子类，只是默认配置不同而已
    可以通过设置 `human_input_mode` 为 "NEVER" 或者 "ALWAYS" 来关闭或者开启用户的响应
    如果需要人参与进来就需要复写 `get_human_input` 方法，要执行多个代码块或单个代码块，就需要分别重写 `execute_code_blocks` `run_code` 和 `execute_function` 方法
    """

    DEFAULT_CONFIG = False
    MAX_CONSECUTIVE_AUTO_REPLY = 100
    DEFAULT_SUMMARY_PROMPT = "Summarize the takeaway from the conversation. Do not add any introductory phrases."
    DEFAULT_SUMMARY_METHOD = "last_msg"
    llm_config: Union[Dict, Literal[False]]

    def __init__(
        self,
        name:str,
        system_message: Optional[Union[str,List]] = "You are a helpful AI Assistant.",
        is_termination_msg: Optional[Callable[[Dict], bool]] = None,
        max_consecutive_auto_reply: Optional[int] = None,
        human_input_mode: Literal["ALWAYS", "NEVER", "TERMINATE"] = "TERMINATE",
        function_map: Optional[Dict[str, Callable]] = None,
        code_execution_config: Union[Dict, Literal[False]] = False,
        llm_config: Optional[Union[Dict, Literal[False]]] = None,
        default_auto_reply: Union[str, Dict] = "",
        description: Optional[str] = None,
    ):
