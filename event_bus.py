"""
이 코드는 명세서 제8장 및 제12장의 요구사항을 반영하여 작성되었음.
"""
import asyncio
from typing import Callable, Dict, List, Any

# [①사유]: 에이전트 간의 통신을 중앙 집중화하고 비동기 이벤트 발행/구독(Pub/Sub) 구조를 구축함.
# [②위험성]: 이벤트 버스 지연은 전체 시스템 레이턴시와 직결되며, 이벤트 손실 시 정합성 붕괴.
# [③커스텀 범위]: 내부 버스는 asyncio.PriorityQueue를 사용하여 Execution/Risk 이벤트를 최우선 처리함.

class EventBus:
    """우선순위 기반 내부 이벤트 메시지 버스"""
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._queue = asyncio.PriorityQueue()

    def subscribe(self, event_type: str, callback: Callable):
        """특정 이벤트 유형에 대한 구독 등록"""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    async def publish(self, event_type: str, data: Any, priority: int = 1):
        """이벤트 발행 (priority: 낮은 숫자가 높은 우선순위)"""
        await self._queue.put((priority, event_type, data))

    async def start_bus(self):
        """메시지 루프 실행 (이벤트 배포)"""
        while True:
            priority, event_type, data = await self._queue.get()
            if event_type in self._subscribers:
                for callback in self._subscribers[event_type]:
                    await callback(data)
            self._queue.task_done()

# 주석: 본 이벤트 버스는 시스템의 신경망으로, 전략→리스크→주문→로그 순의 엄격한 우선순위를 가짐.
