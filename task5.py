import asyncio
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import random

class Response(Enum):
    Success = 1
    RetryAfter = 2
    Failure = 3
    
@dataclass
class ApplicationResponse:
    identifier: str
    status: Response
    description: str
    last_request_time: datetime
    retriesCount: int

async def get_application_status1(identifier: str) -> Response:
    # Здесь должен быть код для получения статуса заявки от сервиса 1
    await asyncio.sleep(random.uniform(0.5, 2))  # Пример задержки
    return random.choice([Response.Success, Response.RetryAfter, Response.Failure])

async def get_application_status2(identifier: str) -> Response:
    # Здесь должен быть код для получения статуса заявки от сервиса 2
    await asyncio.sleep(random.uniform(0.5, 2))  # Пример задержки
    return random.choice([Response.Success, Response.RetryAfter, Response.Failure])

async def perform_operation(identifier: str) -> ApplicationResponse:
    TIMEOUT = 5
    DELAY_BEFORE_NEXT_TRIAL = 3
    
    start_time = datetime.now()

    with ThreadPoolExecutor() as pool:
        response1_task = await asyncio.get_event_loop().run_in_executor(pool, get_application_status1, identifier)
        response2_task = await asyncio.get_event_loop().run_in_executor(pool, get_application_status2, identifier)

        responses = await asyncio.gather(response1_task, response2_task)

    end_time = datetime.now()
    elapsed_time = (end_time - start_time).total_seconds()

    if elapsed_time > TIMEOUT:
        return ApplicationResponse(identifier, Response.Failure, "Timeout exceeded", end_time, None)

    if Response.Success in responses:
        return ApplicationResponse(identifier, Response.Success, "Operation successful", end_time, None)
    elif Response.RetryAfter in responses:
        await asyncio.sleep(DELAY_BEFORE_NEXT_TRIAL)
        return ApplicationResponse(identifier, Response.RetryAfter, "Retry after delay", end_time, None)
    else:
        return ApplicationResponse(identifier, Response.Failure, "Operation failed", end_time, None)

async def main():
    identifier = str(random.randint(1, 1_000_000))
    result = await perform_operation(identifier)
    print(result)

asyncio.run(main())
