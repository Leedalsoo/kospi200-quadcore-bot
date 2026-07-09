"""
이 코드는 명세서 제12장 및 제15장의 요구사항을 반영하여 작성되었음.
"""
from typing import List, Dict
from collections import deque
from data_contract import MarketTick

# [①사유]: 수신된 Raw 틱 데이터를 시스템 규격에 맞춰 정규화하고, LOB를 재구축하여 시세 왜곡 방지.
# [②위험성]: 데이터 수신 지연(Latency)이 발생하면 전략 에이전트의 판단 오류를 초래함.
# [③커스텀 범위]: 호가창 재구축 로직은 1~10호가로 고정함.

class MarketDataAgent:
    """틱 데이터 정규화 및 주문책 관리 엔진"""
    def __init__(self):
        self.orderbook: Dict[str, List] = {"bid": [], "ask": []}
        self.tick_buffer = deque(maxlen=1000) # 백프레셔 제어를 위한 링 버퍼

    def normalize_tick(self, raw_data: Dict) -> MarketTick:
        """Raw 데이터를 MarketTick 데이터 컨트랙트 규격으로 변환"""
        # 데이터 정규화 로직 구현
        return MarketTick(
            instrument_code=raw_data["code"],
            timestamp=raw_data["time"],
            last_price=float(raw_data["price"]),
            volume=int(raw_data["vol"]),
            bid_prices=raw_data["bids"],
            ask_prices=raw_data["asks"],
            bid_qtys=raw_data["b_qtys"],
            ask_qtys=raw_data["a_qtys"]
        )

    def apply_backpressure(self):
        """데이터 큐 포화 감지 시 오래된 데이터 즉시 폐기"""
        if len(self.tick_buffer) >= 1000:
            self.tick_buffer.popleft()

    def rebuild_orderbook(self, tick: MarketTick):
        """1~10호가 뎁스 재구축"""
        self.orderbook["bid"] = list(zip(tick.bid_prices, tick.bid_qtys))
        self.orderbook["ask"] = list(zip(tick.ask_prices, tick.ask_qtys))

# 주석: 본 모듈은 명세서 제15장 4조(고속 틱 처리)를 준수하며 비동기 락을 사용하지 않음.
