
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union

import logging
logger = logging.getLogger(__name__)

azentengine_logger = None

def log_new_agent(agent: ConversableAgent, init_args: Dict[str, Any]) -> None:
    if azentengine_logger is None:
        logger.error("[runtime logging] log_new_agent: autogen logger is None")
        return

    autogen_logger.log_new_agent(agent, init_args)