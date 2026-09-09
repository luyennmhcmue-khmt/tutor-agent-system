from typing import Annotated, List, Optional
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class TutorState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    behavior_strikes: int
    is_account_locked: bool
    wrong_attempts: int
    academic_warning: bool
    force_theory_review: bool
    system_notice: Optional[str]
    exercise: Optional[str]