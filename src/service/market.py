from data import market as data
from model.market import Market

def get_all() -> list[Market]:
    return data.get_all()

def get_market(market_name) -> Market | None:
    return data.get_market(market_name)