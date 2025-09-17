from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI(title="Marketing Automation API")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

KNOWLEDGE_BASE = "You are a marketing pro. Use best practices for offers, ad copy, images, and autoresponders: focus on benefits, AIDA model, clear CTAs."

class OfferRequest(BaseModel):
    client_details: str

class AdCopyRequest(BaseModel):
    campaign: str

class AdImageRequest(BaseModel):
    ad_concept: str

class AutoresponderRequest(BaseModel):
    client_info: str

@app.post("/generate_offer")
async def generate_offer(request: OfferRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": KNOWLEDGE_BASE},
                {"role": "user", "content": f"Create offer for client: {request.client_details}"}
            ]
        )
        offer = response.choices[0].message.content.strip()
        return {"offer": offer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_ad_copy")
async def generate_ad_copy(request: AdCopyRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": KNOWLEDGE_BASE},
                {"role": "user", "content": f"Write ad copy for {request.campaign}"}
            ]
        )
        # print(response.choices[0].message.content)  # Testing: log raw response
        ad_copy = response.choices[0].message.content.strip()
        return {"ad_copy": ad_copy}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_ad_image")
async def generate_ad_image(request: AdImageRequest):
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=f"Design ad image for {request.ad_concept}. Follow: {KNOWLEDGE_BASE}",
            size="1024x1024",
            quality="standard",
            n=1
        )
        image_url = response.data[0].url
        # return {"raw_response": response.data}  # Testing: return full DALL-E response
        return {"image_url": image_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate_autoresponder")
async def generate_autoresponder(request: AutoresponderRequest):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": KNOWLEDGE_BASE},
                {"role": "user", "content": f"Create ad opt-in autoresponder for {request.client_info}"}
            ]
        )
        autoresponder = response.choices[0].message.content.strip()
        return {"autoresponder": autoresponder}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
