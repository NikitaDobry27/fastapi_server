from typing import List
import uvicorn
import base64
import json
from fastapi import FastAPI, Request, HTTPException
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

def decode_jwt(token: str) -> dict:
    """Decode JWT token without external libraries."""
    try:
        header, payload, signature = token.split('.')
        
        # Decode the payload
        decoded_payload = base64.urlsafe_b64decode(payload + '==')  # Adding padding if necessary
        decoded_json = json.loads(decoded_payload)
        
        return decoded_json
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to decode JWT: {str(e)}")

@app.post('/debug')
async def test(request: Request):
    body = await request.body()
    print("test triggered:\n")
    print("Request body:", body.decode("utf-8"))
    print("Request body raw:", body)
    return {"message": "Request received"}

@app.post('/wrap-forward/first-payment')
async def wf_first_payment(request: Request):
    body = await request.json()
    print("Request body:", body)
    rc.forward_first_payment(body)
    return {"message": "Request received"}

@app.post('/wrap-forward/user-for-won-deals')
async def wf_user_for_won_deals(request: Request):
    body = await request.json()
    print("Request body:", body)
    rc.forward_user_for_won_deals(body)
    return {"message": "Request received"}

@app.post('/wrap-forward/slashid-attio-user')
async def wf_slashid_attio_user(request: Request):
    try:
        body = await request.body()
        jwt_token = body.decode("utf-8")
        decoded_body = decode_jwt(jwt_token)
        print("Decoded JWT:", decoded_body)
        rc.slashid_to_attio_user_creation(decoded_body)
    
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
    return {"message": "Request received"}


if __name__ == '__main__':
    uvicorn.run(app)
