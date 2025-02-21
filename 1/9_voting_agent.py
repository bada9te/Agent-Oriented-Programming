import random
import asyncio
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.agent import Agent
from spade.message import Message

# Агент для голосування, який збирає свої голоси
class VotingAgent(Agent):
    class VotingBehaviour(OneShotBehaviour):
        async def run(self):
            votes = [random.choice(["yes", "no"]) for _ in range(5)]
            print(f"{self.agent.name} collected votes: {votes}")
            result = f"YES: {votes.count('yes')}, NO: {votes.count('no')}"
            print(f"Voting result: {result}")

            msg = Message(to="studtelepov811@xmpp.jp")
            msg.body = result
            await self.send(msg)

    async def setup(self):
        self.add_behaviour(self.VotingBehaviour()) 

# Головний агент, який підраховує результати голосування
class MainAgent(Agent):
    class MainBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                print(f"{self.agent.name} received voting result: {msg.body}")
               
                with open("voting_results.log", "a") as file:
                    file.write(f"Result from {msg.sender}: {msg.body}\n")

    async def setup(self):
        print(f"{self.name} started")
        self.add_behaviour(self.MainBehaviour())

async def main():
    main_agent = MainAgent("studtelepov811@xmpp.jp", "04082004")
    voting_agents = [
        VotingAgent("studtelepov811_r@xmpp.jp", "04082004"),
    ]

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
