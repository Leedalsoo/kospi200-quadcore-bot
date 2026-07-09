""" 
이 코드는 명세서 제3장 및 제12장 7조의 요구사항을 반영하여 작성되었음.
"""
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Final

# [①사유]: 시장 운영 시간과 시스템 내부 연산의 일관성을 확보하고, 나노초 단위의 지연율 측정을 위함.
# [②위험성]: 시각 오차(Clock Drift)는 주문 체결의 결정론적 순서를 뒤섞을 수 있음.
# [③커스텀 범위]: 타임존 변경은 KST 외 불가.

class WatchdogTimeAgent:
    def __init__(self):
        self.kst_tz: Final = ZoneInfo("Asia/Seoul")

    def get_current_kst(self) -> datetime:
        """KST 타임존이 적용된 현재 시각 반환"""
        return datetime.now(self.kst_tz)

    def get_monotonic_time(self) -> float:
        """시스템 내부 지연율 측정을 위한 단조 증가 시간 반환"""
        return time.monotonic()

    def check_market_open(self) -> bool:
        """KOSPI 200 파생시장 정규장 운영 시간 판정"""
        now = self.get_current_kst()
        if now.weekday() >= 5:  # 주말 여부 판정
            return False
        
        # 장 운영 시간: 08:45 ~ 15:45
        market_start = now.replace(hour=8, minute=45, second=0, microsecond=0)
        market_end = now.replace(hour=15, minute=45, second=0, microsecond=0)
        
        return market_start <= now <= market_end

# 주석: 이 클래스는 명세서 제15장 3조(시계 기준 분리)를 준수하여 설계됨.
