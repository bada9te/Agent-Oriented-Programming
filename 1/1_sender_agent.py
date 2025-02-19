import random
import asyncio
from spade.behaviour import CyclicBehaviour
from spade.agent import Agent
from spade.message import Message

# Агент-відправник
class SenderAgent(Agent):
    class SendMessageBehaviour(CyclicBehaviour):
        async def run(self):
            msg = Message(to="studtelepov811@xmpp.jp")  # JID одержувача
            msg.body = str(random.randint(1, 100))
            await self.send(msg)
            print(f"{self.agent.name} sent: {msg.body}")
            await asyncio.sleep(5)  # Відправляємо кожні 5 секунд

    async def setup(self):
        print(f"{self.name} started")
        self.add_behaviour(self.SendMessageBehaviour())

# Агент-одержувач
class ReceiverAgent(Agent):
    class ReceiveMessageBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)  # Очікуємо повідомлення
            if msg:
                print(f"{self.agent.name} received: {msg.body}")

    async def setup(self):
        print(f"{self.name} started")
        self.add_behaviour(self.ReceiveMessageBehaviour())

async def main():
    sender = SenderAgent("studtelepov811@xmpp.jp", "04082004")
    receiver = ReceiverAgent("studtelepov811@xmpp.jp", "04082004")
    
    await sender.start()
    await receiver.start()
    
    await asyncio.sleep(30)  # Час роботи симуляції
    await sender.stop()
    await receiver.stop()
    print("Agents stopped.")

if __name__ == "__main__":
    asyncio.run(main())