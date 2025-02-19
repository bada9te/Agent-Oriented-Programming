import asyncio
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.agent import Agent
from spade.message import Message

# Агент-монітор, який веде лог усіх отриманих повідомлень
class MonitorAgent(Agent):
    class MonitorBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                print(f"Monitor received from {msg.sender}: {msg.body}")
                
                with open("monitor_log.txt", "a") as file:
                    file.write(f"Received from {msg.sender}: {msg.body}\n")
                print(f"Monitor logged message from {msg.sender}")

    async def setup(self):
        print(f"{self.name} started")
        self.add_behaviour(self.MonitorBehaviour()) 

# Агент-запитувач
class QueryAgent(Agent):
    class QueryBehaviour(OneShotBehaviour):
        async def run(self):
            recipients = ["studtelepov811@xmpp.jp"]
            for recipient in recipients:
                msg = Message(to=recipient)
                msg.body = "Hello from QueryAgent"
                await self.send(msg)
            print(f"{self.agent.name} sent a message.")

    async def setup(self):
        print(f"{self.name} started")
        self.add_behaviour(self.QueryBehaviour())  


async def main():
    monitor_agent = MonitorAgent("studtelepov811@xmpp.jp", "04082004")
    query_agent = QueryAgent("studtelepov811_r@xmpp.jp", "04082004")

    # Запуск агентів
    await monitor_agent.start()
    await query_agent.start()

    await asyncio.sleep(20)  # Час роботи симуляції
    await monitor_agent.stop()
    await query_agent.stop()
    print("Agents stopped.")

if __name__ == "__main__":
    asyncio.run(main())
