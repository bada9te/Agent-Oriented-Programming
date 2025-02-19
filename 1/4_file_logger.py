import asyncio
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.agent import Agent
from spade.message import Message

# Агент-запитувач
class QueryAgent(Agent):
    class QueryBehaviour(OneShotBehaviour):
        async def run(self):
            recipients = ["studtelepov811_r@xmpp.jp"]
            for recipient in recipients:
                msg = Message(to=recipient)
                msg.body = "Request for data"
                await self.send(msg)
            print(f"{self.agent.name} requested information.")

            responses = []
            for _ in recipients:
                reply = await self.receive(timeout=5)
                if reply:
                    responses.append(reply.body)
            print(f"{self.agent.name} received responses: {responses}")

    async def setup(self):
        print(f"{self.name} started")
        self.add_behaviour(self.QueryBehaviour())

# Агент-відповідач
class ResponseAgent(Agent):
    class ResponseBehaviour(CyclicBehaviour):  # Використовуємо циклічну поведінку
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                print(f"{self.agent.name} received request from {msg.sender}")
                reply = Message(to=str(msg.sender))
                reply.body = f"Response from {self.agent.name}"
                await self.send(reply)

                # Логування отриманого повідомлення у файл
                with open("responses.log", "a") as file:
                    file.write(f"Received from {msg.sender}: {msg.body}\n")
                print(f"{self.agent.name} logged message from {msg.sender}")

    async def setup(self):
        print(f"{self.name} started")
        self.add_behaviour(self.ResponseBehaviour())

async def main():
    query_agent = QueryAgent("studtelepov811@xmpp.jp", "04082004")
    agent1 = ResponseAgent("studtelepov811_r@xmpp.jp", "04082004")

    await agent1.start()
    await query_agent.start()

    await asyncio.sleep(20)  # Час роботи симуляції
    await query_agent.stop()
    await agent1.stop()
    print("Agents stopped.")

if __name__ == "__main__":
    asyncio.run(main())
