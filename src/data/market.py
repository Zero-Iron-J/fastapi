from model.market import Market

_fake_datas = [
    Market(name="치킨마니아",call_num="088-123-1234",menu={"fried chicken" : 20000}, location="서울"),
    Market(name="피자나라",call_num="033-740-1234",menu={"불고기피자" : 5000, "페퍼로니피자" : 7000}, location="강원도 춘천"),    
]
    
def get_all() -> list[Market]:
    return _fake_datas

def get_market(market_name) -> Market | None:
    for _fake_data in _fake_datas:
        if _fake_data.name == market_name:
            return _fake_data
    return None