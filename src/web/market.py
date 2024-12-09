from fastapi import APIRouter
from model.market import Market
import service.market as service

router = APIRouter(prefix="/market")

@router.get("/")
def get_all() -> list[Market]:
    return service.get_all()

@router.get("/{market_name}")
def get_market(market_name) -> Market | None:
    return service.get_market(market_name)