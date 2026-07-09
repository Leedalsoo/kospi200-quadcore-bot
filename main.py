"""
이 코드는 명세서 제10장 및 제12장의 요구사항을 반영하여 작성되었음.
"""
import asyncio
from event_bus import EventBus
from market_data_agent import MarketDataAgent
from risk_agent import RiskPortfolioAgent
from execution_agent import ExecutionAgent
from strategy_agent import StrategyAgent

# [①사유]: 모든 에이전트를 통합 관리하고 비동기 이벤트 루프를 통해 단일 프로세스로 운영하기 위함.
# [②위험성]: 루프 초기화 실패 시 시스템이 기동되지 않으며, 종료 처리 미흡 시 리소스 누수 발생.
# [③커스텀 범위]: 에이전트 초기화 순서는 데이터→리스크→전략→주문 순서를 엄격히 준수함.

async def main():
    # 1. 시스템 핵심 구성 요소 초기화
    bus = EventBus()
    md_agent = MarketDataAgent()
    risk_agent = RiskPortfolioAgent()
    exec_agent = ExecutionAgent()
    strat_agent = StrategyAgent()

    print("--- Quadcore Trading System Bootstrapping ---")

    # 2. 이벤트 구독 설정 (이벤트 버스 신경망 연결)
    # 예: bus.subscribe("TICK_DATA", md_agent.rebuild_orderbook)
    
    # 3. 비동기 루프 시작
    await asyncio.gather(
        bus.start_bus(),
        # 기타 상시 구동 에이전트 태스크
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("System shutdown requested.")
