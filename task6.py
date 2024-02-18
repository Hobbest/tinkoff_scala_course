import asyncio
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import List
import random

class Result(Enum):
    Accepted = 1
    Rejected = 2

@dataclass
class Address:
    name: str
    email: str

@dataclass
class Payload:
    content: str
    
@dataclass
class Event:
    recipients: List[Address]
    payload: Payload

# Метод для чтения данных
async def read_data() -> Event:
    # Здесь должен быть код для чтения данных
    await asyncio.sleep(1)
    recipients = [Address("Alice", "alice@example.com"), Address("Bob", "bob@example.com")]
    payload = Payload("Hello, World!")
    return Event(recipients, payload)

# Метод для отправки данных
async def send_data(dest: Address, payload: Payload) -> Result:
    # Здесь должен быть код для отправки данных
    status = random.choice([Result.Accepted, Result.Rejected])
    await asyncio.sleep(1)
    return status

# Метод для выполнения операции
async def perform_operation():
    READ_DELAY = 1
    RETRY_DELAY = 5
    
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
    # await loop.run_in_executor(pool, perform_operation)
        while True:
            coro1 = await loop.run_in_executor(pool, read_data)
            event, *_ = await asyncio.gather(coro1)
            for recipient in event.recipients:
                coro2 = await loop.run_in_executor(pool, send_data, recipient, event.payload)
                result, *_ = await asyncio.gather(coro2)
                if result == Result.Rejected:
                    await asyncio.sleep(RETRY_DELAY)
                    coro3 = await loop.run_in_executor(pool, send_data, recipient, event.payload)
                    result, *_ = await asyncio.gather(coro3)
                    if result == Result.Rejected:
                        print(f"Failed to send data to {recipient.name}")
                    else:
                        print(f"Data have been sended to {recipient.name}")
                else:
                    print(f"Data have been sended to {recipient.name}")
            await asyncio.sleep(READ_DELAY)

asyncio.run(perform_operation())
