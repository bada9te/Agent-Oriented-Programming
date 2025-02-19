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
            msg.body = "This is a key message!" if random.random() > 0.5 else "Just a regular message."
            await self.send(msg)
            print(f"{self.agent.name} sent: {msg.body}")
            await asyncio.sleep(5)

    async def setup(self):
        print(f"{self.name} started")
        self.add_behaviour(self.SendMessageBehaviour())

# Агент-одержувач (з ключовим словом)
class KeywordAgent(Agent):
    class KeywordBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg and "key" in msg.body.lower():
                print(f"{self.agent.name} received a key message: {msg.body}")

    async def setup(self):
        print(f"{self.name} started")
        self.add_behaviour(self.KeywordBehaviour())

async def main():
    sender = SenderAgent("studtelepov811@xmpp.jp", "04082004")
    receiver = KeywordAgent("studtelepov811@xmpp.jp", "04082004")
    
    await sender.start()
    await receiver.start()
    
    await asyncio.sleep(30)  # Час роботи симуляції
    await sender.stop()
    await receiver.stop()
    print("Agents stopped.")

if __name__ == "__main__":
    asyncio.run(main())
