from typing import List
import uvicorn
import base64
import json
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from pydantic import BaseModel
from rivet_client import RivetClient

app = FastAPI()

MAX_REQUEST_SIZE = 1_000_000  # 1 MB

@app.middleware("http")
async def limit_request_size(request: Request, call_next):
    request_body = await request.body()
    if len(request_body) > MAX_REQUEST_SIZE:
        raise HTTPException(status_code=413, detail="Request body too large")
    return await call_next(request)

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

def process_slashid_attio_user(decoded_body: dict):
    """Function to process the webhook in background."""
    try:
        rc.slashid_to_attio_user_creation(decoded_body)
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")

def process_chargebee_attio(body_json:dict):
    try:
        rc.chargebee_to_attio(body_json)
    except Exception as e: 
        print(f"Error processing webhook: {str(e)}")

def process_orb_attio(body_json:dict):
    try:
        rc.orb_to_attio(body_json)
    except Exception as e: 
        print(f"Error processing webhook: {str(e)}")

def process_intercom_dashboard(body_json:dict):
    try:
        rc.intercom_dashboard(body_json)
    except Exception as e: 
        print(f"Error processing webhook: {str(e)}")

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
async def wf_slashid_attio_user(request: Request, background_tasks: BackgroundTasks):
    try:
        body = await request.body()
        jwt_token = body.decode("utf-8")
        decoded_body = decode_jwt(jwt_token)
        print("Decoded JWT:", json.dumps(decoded_body))
        
        # Add the processing task to the background
        background_tasks.add_task(process_slashid_attio_user, decoded_body)
        
        # Immediately return a 200 response
        return {"message": "Request received"}

    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error processing webhook: {str(e)}")

@app.post('/wrap-forward/chargebee-attio')
async def chargebee_attio_sync(request: Request, background_tasks: BackgroundTasks):
    try:
        body = await request.body()
        body_str = body.decode('utf-8')
        body_json = json.loads(body_str)
        print("Request body JSON:", json.dumps(body_json))
        background_tasks.add_task(process_chargebee_attio, body_json)
    except json.JSONDecodeError as json_error:
        print(f"JSON decode error: {json_error}")
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"message": "Request received"}

@app.post('/wrap-forward/orb-attio')
async def orb_attio_sync(request: Request, background_tasks: BackgroundTasks):
    try:
        body = await request.body()
        body_str = body.decode('utf-8')
        body_json = json.loads(body_str)
        print("Request body JSON:", json.dumps(body_json))
        background_tasks.add_task(process_orb_attio, body_json)
    except json.JSONDecodeError as json_error:
        print(f"JSON decode error: {json_error}")
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"message": "Request received"}

@app.post('/wrap-forward/intercom-dashboard')
async def intercom_dashboard_sync(request: Request, background_tasks: BackgroundTasks):
    try:
        body = await request.body()
        body_str = body.decode('utf-8')
        body_json = json.loads(body_str)
        print("Request body JSON:", json.dumps(body_json))
        background_tasks.add_task(process_intercom_dashboard, body_json)
    except json.JSONDecodeError as json_error:
        print(f"JSON decode error: {json_error}")
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return {"message": "Request received"}

if __name__ == '__main__':
    uvicorn.run(app)
