from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ..services.ai_gateway import AIGateway, get_ai_gateway

router = APIRouter(prefix="/api", tags=["ai"])


class ConfigRequest(BaseModel):
    requirements: str
    complexity: str = "medium"


class ConfigResponse(BaseModel):
    config: str


@router.post("/generate_config", response_model=ConfigResponse)
async def generate_config(
    request: ConfigRequest,
    gateway: AIGateway = Depends(get_ai_gateway),
):
    """Generate ServiceNow configuration code from natural language requirements."""
    result = gateway.generate_config(request.requirements, request.complexity)
    return {"config": result}
