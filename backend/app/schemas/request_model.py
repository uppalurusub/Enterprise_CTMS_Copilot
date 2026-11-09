from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field


class CTMSRequest(BaseModel):
    """
    Generic request model for Enterprise CTMS Copilot.
    Supports Multi-Agent, RAG, SQL Agent, and conversation context.
    """

    # =========================
    # User Query
    # =========================
    question: str = Field(
        ...,
        description="Natural language question asked by the user."
    )

    # =========================
    # Session Information
    # =========================
    session_id: str = Field(
        default="default-session",
        description="Conversation session identifier."
    )

    user_id: Optional[str] = Field(
        default=None,
        description="Current logged-in user."
    )

    role: Optional[str] = Field(
        default="CRA",
        description="User role (Sponsor, CRA, Investigator, Site Coordinator, etc.)"
    )

    # =========================
    # CTMS Identifiers
    # =========================
    trial_id: Optional[str] = None
    protocol_id: Optional[str] = None
    site_id: Optional[str] = None
    patient_id: Optional[str] = None
    monitoring_visit_id: Optional[str] = None
    budget_id: Optional[str] = None
    invoice_id: Optional[str] = None

    # =========================
    # Agent Selection
    # =========================
    module: Optional[str] = Field(
        default="auto",
        description="""
        auto
        trial_planning
        budget_management
        monitoring
        site_management
        patient_recruitment
        """
    )

    # =========================
    # SQL Agent
    # =========================
    enable_sql_agent: bool = True

    # =========================
    # RAG
    # =========================
    enable_rag: bool = True

    top_k: int = 5

    document_types: List[str] = Field(
        default_factory=list,
        description="Protocol, SOP, Monitoring Report, Budget, etc."
    )

    # =========================
    # Metadata Filters
    # =========================
    filters: Dict[str, Any] = Field(default_factory=dict)

    # Example:
    # {
    #   "country":"India",
    #   "phase":"Phase III",
    #   "status":"Active"
    # }

    # =========================
    # LLM Parameters
    # =========================
    temperature: float = 0.2

    max_tokens: int = 2000

    # =========================
    # Conversation Memory
    # =========================
    chat_history: List[Dict[str, str]] = Field(
        default_factory=list
    )

    # =========================
    # Additional Context
    # =========================
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        json_schema_extra = {
            "example": {
                "question": "Show active monitoring visits for Trial TRL-1001",
                "session_id": "SESSION-001",
                "user_id": "CRA100",
                "role": "CRA",
                "trial_id": "TRL-1001",
                "module": "monitoring",
                "enable_sql_agent": True,
                "enable_rag": True,
                "top_k": 5,
                "document_types": [
                    "Protocol",
                    "Monitoring Report"
                ],
                "filters": {
                    "country": "India",
                    "status": "Active"
                },
                "temperature": 0.2,
                "max_tokens": 1500,
                "chat_history": [],
                "metadata": {
                    "application": "Enterprise CTMS Copilot"
                }
            }
        }