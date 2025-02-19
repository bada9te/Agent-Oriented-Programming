import random
import asyncio
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.agent import Agent
from spade.message import Message

# Агент для голосування, який збирає свої голоси
class VotingAgent(Agent):
    class VotingBehaviour(OneShotBehaviour):
        async def run(self):
            # Створюємо список голосів агентів
            votes = [random.choice(["yes", "no"]) for _ in range(5)]
            print(f"{self.agent.name} collected votes: {votes}")
            result = f"YES: {votes.count('yes')}, NO: {votes.count('no')}"
            print(f"Voting result: {result}")

            # Надсилаємо результат голосування головному агенту
            msg = Message(to="main_agent@xmpp.jp")
            msg.body = result
            await self.send(msg)

    async def setup(self):
        self.add_behaviour(self.VotingBehaviour())  # Додаємо поведінку голосування

# Головний агент, який підраховує результати голосування
class MainAgent(Agent):
    class MainBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                print(f"{self.agent.name} received voting result: {msg.body}")
                # Логування результатів голосування
                with open("voting_results.log", "a") as file:
                    file.write(f"Result from {msg.sender}: {msg.body}\n")

    async def setup(self):
        print(f"{self.name} started")
        self.add_behaviour(self.MainBehaviour())  # Додаємо поведінку підрахунку результатів

# Основна функція для ініціалізації агентів
async def main():
    main_agent = MainAgent("main_agent@xmpp.jp", "password")
    voting_agents = [
        VotingAgent("voting_agent1@xmpp.jp", "password"),
        VotingAgent("voting_agent2@xmpp.jp", "password"),
        VotingAgent("voting_agent3@xmpp.jp", "password"),
    ]

    # Запуск головного агента та агентів голосування
    await main_agent.start()
    for agent in voting_agents:
        await agent.start()

    await asyncio.sleep(20)  # Час роботи симуляції
    await main_agent.stop()
    for agent in voting_agents:
        await agent.stop()
    print("Agents stopped.")

if __name__ == "__main__":
    asyncio.run(main())
