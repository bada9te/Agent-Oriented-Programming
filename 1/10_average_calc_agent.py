import random
import asyncio
from spade.behaviour import CyclicBehaviour
from spade.agent import Agent
from spade.message import Message


# Агент для обміну числовими даними та обчислення середнього значення
class AverageCalculatorAgent(Agent):
    class AverageBehaviour(CyclicBehaviour):
        numbers = []  # Список для зберігання отриманих чисел

        async def run(self):
            msg = await self.receive(timeout=10)  # Чекаємо повідомлення з числовими даними
            if msg:
                self.numbers.append(int(msg.body))

                avg = sum(self.numbers) / len(self.numbers)
                print(f"{self.agent.name} updated average: {avg}")

                with open("average_log.txt", "a") as file:
                    file.write(f"Received number: {msg.body}, Average: {avg}\n")

    async def setup(self):
        self.add_behaviour(self.AverageBehaviour()) 

# Агент-запитувач, який надсилає числові дані
class NumberSenderAgent(Agent):
    class NumberSenderBehaviour(CyclicBehaviour):
        async def run(self):
            numbers_to_send = [random.randint(1, 100) for _ in range(5)] 
            for num in numbers_to_send:
                msg = Message(to="studtelepov811@xmpp.jp")
                msg.body = str(num)
                await self.send(msg)
                print(f"{self.agent.name} sent number: {num}")
            
            self.kill()

    async def setup(self):
        self.add_behaviour(self.NumberSenderBehaviour()) 


async def main():
    average_calculator = AverageCalculatorAgent("studtelepov811@xmpp.jp", "04082004")
    number_sender = NumberSenderAgent("studtelepov811_r@xmpp.jp", "04082004")

    # Запуск агентів
    await average_calculator.start()
    await number_sender.start()

    await asyncio.sleep(20)  # Час роботи симуляції
    await average_calculator.stop()
    await number_sender.stop()
    print("Agents stopped.")

if __name__ == "__main__":
    asyncio.run(main())
