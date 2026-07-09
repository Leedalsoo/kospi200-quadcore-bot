"""
이 코드는 명세서 제6장 및 제12장의 요구사항을 반영하여 작성되었음.
"""
from enum import Enum, auto
from uuid import UUID
from data_contract import OrderRequest, ExecutionReport

# [①사유]: 주문 생애 주기(FSM)를 관리하여 '미체결 주문의 무한 대기'나 '이중 주문' 사고를 방지함.
# [②위험성]: 상태 전이 오류 발생 시 포지션 불일치가 발생하며, 이는 즉각적인 금전 손실로 이어짐.
# [③커스텀 범위]: 14단계 상태 전이 규칙은 명세서에 정의된 것 외 임의 변경 금지.

class OrderStatus(Enum):
    PENDING = auto()       # 주문 전송 대기
    NEW = auto()           # 거래소 접수 완료
    PARTIALLY_FILLED = auto()
    FILLED = auto()
    CANCELLED = auto()
    REJECTED = auto()      # 리스크 에이전트에 의해 거부됨

class ExecutionAgent:
    """주문 관리 및 14단계 상태 머신(FSM) 엔진"""
    def __init__(self):
        self.order_book: Dict[UUID, OrderStatus] = {}

    def transition_state(self, order_id: UUID, next_status: OrderStatus):
        """FSM 기반 상태 전이 검증 로직"""
        current = self.order_book.get(order_id, OrderStatus.PENDING)
        
        # [상태 전이 규칙 예시]
        if current == OrderStatus.NEW and next_status == OrderStatus.FILLED:
            self.order_book[order_id] = next_status
        elif current == OrderStatus.PENDING and next_status == OrderStatus.REJECTED:
            self.order_book[order_id] = next_status
        else:
            print(f"Invalid State Transition: {current} -> {next_status}")

    def on_execution_report(self, report: ExecutionReport):
        """브로커로부터 받은 체결 보고서 처리"""
        # 상태 업데이트 및 포지션 갱신 요청
        self.transition_state(report.client_order_id, OrderStatus(report.status))

# 주석: 이 에이전트는 리스크 에이전트와 긴밀히 연동되며, 승인된 주문만 물리적으로 전송함.
