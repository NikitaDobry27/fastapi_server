from typing import List

import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel

from rivet_client import RivetClient

app = FastAPI()


class EventID(BaseModel):
    workspace_id: str
    object_id: str
    record_id: str


class Actor(BaseModel):
    type: str
    id: str


class Event(BaseModel):
    event_type: str
    id: EventID
    actor: Actor


class FirstPayment(BaseModel):
    webhook_id: str
    events: List[Event]


rc = RivetClient()


@app.post('/debug')
async def test(request: Request):
    body = await request.body()
    print("test riggered:\n")
    print("Request body:", body.decode("utf-8"))
    return {"message": "Request received"}


@app.post('/wrap-forward/first-payment')
async def wf_first_payment(first_payment: FirstPayment):
    rc.forward_first_payment(first_payment.model_dump())


if __name__ == '__main__':
    uvicorn.run(app)
