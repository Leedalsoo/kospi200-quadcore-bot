"""
이 코드는 명세서 제5장 및 제12장의 요구사항을 반영하여 작성되었음.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any

# [①사유]: 전략별 로직을 시스템 코어와 분리하여 런타임에 동적으로 로딩 및 교체하기 위함.
# [②위험성]: 전략 코드의 의존성 충돌은 시스템 전체 정지(Fatal Error)를 초래함.
# [③커스텀 범위]: 전략 플러그인은 반드시 명시된 Interface를 상속받아야 함.

class StrategyInterface(ABC):
    """전략 플러그인 표준 인터페이스"""
    @abstractmethod
    def on_tick(self, tick: Any): pass
    
    @abstractmethod
    def generate_signal(self) -> Dict[str, Any]: pass

class StrategyAgent:
    """전략 통합 관리 및 플러그인 로더"""
    def __init__(self):
        self.active_strategies: Dict[str, StrategyInterface] = {}

    def load_plugin(self, strategy_name: str, strategy_instance: StrategyInterface):
        """동적 플러그인 로딩 및 버전 검증"""
        # 전략 버전 관리 및 서명 검증 로직 구현 예정
        self.active_strategies[strategy_name] = strategy_instance
        print(f"Plugin Loaded: {strategy_name}")

    def execute_tick_cycle(self, tick: Any):
        """활성화된 모든 전략에 틱 데이터 배포"""
        for strategy in self.active_strategies.values():
            strategy.on_tick(tick)

# 주석: 전략 플러그인은 절대 코어 시스템의 내부 상태를 직접 변경할 수 없으며, 
# 반드시 이벤트 버스를 통해서만 통신함.
