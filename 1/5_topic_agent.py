import asyncio
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.agent import Agent
from spade.message import Message

# Агент, який реагує лише на повідомлення з темою "ALERT"
class TopicAgent(Agent):
    class TopicBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg and "ALERT" in msg.body: 
                print(f"{self.agent.name} received an alert: {msg.body}")

    async def setup(self):
        print(f"{self.name} started")
        self.add_behaviour(self.TopicBehaviour())

# Агент-запитувач
class QueryAgent(Agent):
    class QueryBehaviour(OneShotBehaviour):
        async def run(self):
            recipients = ["studtelepov811_r@xmpp.jp"] 
            for recipient in recipients:
                msg = Message(to=recipient)
                msg.body = "ALERT: System failure detected"
                await self.send(msg)

    async def setup(self):
        print(f"{self.name} started")
        self.add_behaviour(self.QueryBehaviour()) 


async def main():
    query_agent = QueryAgent("studtelepov811@xmpp.jp", "04082004")
    topic_agent = TopicAgent("studtelepov811_r@xmpp.jp", "04082004")

    # Запуск агентів
    await topic_agent.start()
    await query_agent.start()

    await asyncio.sleep(20)  # Час роботи симуляції
    await query_agent.stop()
    await topic_agent.stop()
    print("Agents stopped.")

if __name__ == "__main__":
    asyncio.run(main())
