"""
이 코드는 명세서 제2장의 요구사항을 반영하여 작성되었음.
"""
from dataclasses import dataclass, field
from decimal import Decimal
from datetime import datetime
from typing import List, Optional
from uuid import UUID

# [①사유]: 시스템 전반에서 사용되는 데이터의 무결성과 타입 안전성을 보장하기 위함.
# [②위험성]: 잘못된 데이터 구조체 정의는 OMS(주문관리시스템) 전체의 논리적 붕괴를 초래함.
# [③커스텀 범위]: 각 데이터 구조의 필드는 명세서 제2장에 정의된 것 외에 임의 추가 금지.

@dataclass(slots=True)
class MarketTick:
    instrument_code: str = field(metadata={"description": "종목코드"})
    timestamp: datetime = field(metadata={"description": "거래소 시각(KST)"})
    last_price: float = field(metadata={"description": "최종 체결가(float64)"})
    volume: int = field(metadata={"description": "체결량"})
    bid_prices: List[float] = field(metadata={"description": "매수호가 리스트"})
    ask_prices: List[float] = field(metadata={"description": "매도호가 리스트"})
    bid_qtys: List[int] = field(metadata={"description": "매수잔량 리스트"})
    ask_qtys: List[int] = field(metadata={"description": "매도잔량 리스트"})

@dataclass(slots=True)
class InstrumentProfile:
    instrument_code: str = field(metadata={"description": "종목코드"})
    strike_price: float = field(metadata={"description": "행사가"})
    tick_size_rule: float = field(metadata={"description": "호가단위 규칙"})
    multiplier: int = field(metadata={"description": "승수(KOSPI200: 250,000)"})
    expiry_date: datetime = field(metadata={"description": "만기일"})
    is_underlying: bool = field(metadata={"description": "기초자산 여부"})

@dataclass(slots=True)
class OrderRequest:
    decision_id: UUID = field(metadata={"description": "결정 ID"})
    client_order_id: UUID = field(metadata={"description": "고유 주문 ID"})
    instrument_code: str = field(metadata={"description": "종목코드"})
    order_type: str = field(metadata={"description": "주문유형(LIMIT 고정)"})
    side: str = field(metadata={"description": "BUY/SELL"})
    price: Decimal = field(metadata={"description": "주문가격(Decimal)"})
    qty: int = field(metadata={"description": "주문수량"})

@dataclass(slots=True)
class ExecutionReport:
    client_order_id: UUID = field(metadata={"description": "주문 ID"})
    broker_order_id: str = field(metadata={"description": "브로커 주문 ID"})
    status: str = field(metadata={"description": "OMS 14단계 상태"})
    filled_qty: int = field(metadata={"description": "체결량"})
    filled_price: Decimal = field(metadata={"description": "체결가격(Decimal)"})
    timestamp: datetime = field(metadata={"description": "체결시각"})

@dataclass(slots=True)
class Position:
    instrument_code: str = field(metadata={"description": "종목코드"})
    role: str = field(metadata={"description": "포지션 역할(MAIN, WING 등)"})
    avg_price: Decimal = field(metadata={"description": "평균 단가(Decimal)"})
    qty: int = field(metadata={"description": "포지션 수량"})
    realized_pnl: Decimal = field(metadata={"description": "실현 손익"})
    unrealized_pnl: Decimal = field(metadata={"description": "미실현 손익"})

@dataclass(slots=True)
class DecisionLog:
    decision_id: UUID = field(metadata={"description": "결정 ID"})
    trigger_type: str = field(metadata={"description": "트리거 유형"})
    regime_state: str = field(metadata={"description": "시장 국면"})
    composite_risk_score: float = field(metadata={"description": "통합 리스크 점수"})
    reason: str = field(metadata={"description": "결정 사유"})

@dataclass(slots=True)
class HardLimitsConfig:
    mdd_shutdown_pct: float = field(metadata={"description": "글로벌 MDD 한도"})
    max_kelly_fraction: float = field(metadata={"description": "최대 켈리 비율"})
    fat_finger_theo_dev_pct: float = field(metadata={"description": "이론가 이탈 허용률"})
    fat_finger_ltp_dev_pct: float = field(metadata={"description": "LTP 이탈 허용률"})
    max_order_qty_per_trade: int = field(metadata={"description": "1회 최대 주문량"})
    max_daily_loss_amount: Decimal = field(metadata={"description": "일일 최대 손실액"})
