"""
이 코드는 명세서 제7장 및 제15장의 요구사항을 반영하여 작성되었음.
"""
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from datetime import datetime
from typing import Any, Dict
from uuid import UUID

# [①사유]: 매매 이벤트를 안전하게 디스크에 기록하여 시스템 장애 시 복구(Replay)를 가능하게 함.
# [②위험성]: 파일 I/O가 메인 루프를 블로킹할 경우 슬리피지(Slippage) 발생 및 체결 실패 위험.
# [③커스텀 범위]: JSONL 로그 회전(Rotation) 정책은 향후 별도 설정 가능.

class TradingJSONEncoder(json.JSONEncoder):
    """Decimal, UUID, datetime 타입을 JSON으로 직렬화하기 위한 커스텀 인코더"""
    def default(self, obj: Any) -> Any:
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

class EventStoreAgent:
    """이벤트 영속화 및 상태 스냅샷 저장 엔진"""
    def __init__(self, log_path: str = "logs/event_store.jsonl"):
        self.log_path = log_path
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._lock = threading.Lock()

    def append_event(self, event_type: str, payload: Dict[str, Any]) -> None:
        """비동기적으로 이벤트를 JSONL 형식으로 디스크에 기록"""
        event_data = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "payload": payload
        }
        self._executor.submit(self._write_to_disk, event_data)

    def _write_to_disk(self, event_data: Dict[str, Any]) -> None:
        """디스크 쓰기 작업(싱글 스레드 보장)"""
        with self._lock:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(event_data, cls=TradingJSONEncoder) + "\n")

    def trigger_snapshot(self) -> None:
        """상태 스냅샷 백업 로직 뼈대"""
        # 향후 스냅샷 생성 로직 구현 예정
        pass

    def graceful_shutdown(self) -> None:
        """시스템 종료 시 이벤트 큐 정리 및 풀 닫기"""
        self._executor.shutdown(wait=True)
