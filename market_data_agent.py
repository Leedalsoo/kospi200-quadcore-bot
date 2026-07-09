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
"""
이 코드는 명세서 제9장 및 제12장의 요구사항을 반영하여 작성되었음.
"""

# [①사유]: 시장의 매물대와 불균형을 실시간 분석하여 진입 신호의 정밀도를 극대화함.
# [②위험성]: 산출식에 오차 발생 시 휩쏘(휩소) 필터가 무력화되어 고빈도 매매 손실 위험.
# [③커스텀 범위]: 베이시스 및 OBI 계산식은 명세서 표준 공식을 준수함.

    def calculate_microprice_and_obi(self) -> tuple[float, float]:
        """미시 가격(Micro-price) 및 호가 불균형(OBI) 연산"""
        # Micro-price = (Bid * AskQty + Ask * BidQty) / (BidQty + AskQty)
        bid_p, bid_q = self.orderbook["bid"][0]
        ask_p, ask_q = self.orderbook["ask"][0]
        micro_price = (bid_p * ask_q + ask_p * bid_q) / (bid_q + ask_q)
        obi = (bid_q - ask_q) / (bid_q + ask_q)
        return micro_price, obi

    def calc_market_basis(self, spot_price: float, future_price: float) -> float:
        """선-현물 베이시스 격차 추적"""
        return future_price - spot_price

    def calc_volume_profile_poc(self) -> float:
        """거래량 기반 당일 최대 매물대(POC) 연산"""
        # 당일 틱 히스토그램 누적 후 최대 빈도 가격 추출
        # (실제 구현 시 deque와 딕셔너리를 활용한 빈도 분석 로직 삽입)
        return 0.0 # POC 가격 반환

# 주석: 이 메서드들은 명세서 9장의 휩쏘 필터링을 위한 핵심 팩터로 활용됨.

