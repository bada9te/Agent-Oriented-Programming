import asyncio
from spade.behaviour import CyclicBehaviour, OneShotBehaviour
from spade.agent import Agent
from spade.message import Message


# 7 ️. Реалізувати агента, який аналізує текст повідомлення і відповідає залежно від змісту (чат-бот).
class ChatBotAgent(Agent):
    class ChatBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                response = "I don't understand."
                if "hello" in msg.body.lower():
                    response = "Hi! How can I help you?"
                elif "bye" in msg.body.lower():
                    response = "Goodbye!"
                reply = msg.make_reply()
                reply.body = response
                await self.send(reply)

    async def setup(self):
        self.add_behaviour(self.ChatBehaviour())


# Агент-запитувач
class QueryAgent(Agent):
    class QueryBehaviour(OneShotBehaviour):
        async def run(self):
            recipients = ["studtelepov811_r@xmpp.jp"] 
            for recipient in recipients:
                msg = Message(to=recipient)
                msg.body = "hello"
                await self.send(msg)

                asyncio.sleep(3);
                msg.body = "bye"
                await self.send(msg)


            responses = []
            for _ in recipients:
                reply = await self.receive(timeout=10)
                if reply:
                    responses.append(reply.body)
            print(f"{self.agent.name} received responses: {responses}")

    async def setup(self):
        print(f"{self.name} started")
        self.add_behaviour(self.QueryBehaviour()) 



async def main():
    query_agent = QueryAgent("studtelepov811@xmpp.jp", "04082004")
    topic_agent = ChatBotAgent("studtelepov811_r@xmpp.jp", "04082004")

    # Запуск агентів
    await topic_agent.start()
    await query_agent.start()

    await asyncio.sleep(20)  # Час роботи симуляції
    await query_agent.stop()
    await topic_agent.stop()
    print("Agents stopped.")

if __name__ == "__main__":
    asyncio.run(main())