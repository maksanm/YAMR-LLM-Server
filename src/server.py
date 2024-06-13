from dotenv import load_dotenv
load_dotenv()

import uvicorn
import os
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from chains.yamr_chain import YAMRChainFactory, YAMRChainInput

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

yamr_chain = YAMRChainFactory().create()

@app.get("/")
async def redirect_root_to_docs():
    return RedirectResponse("/docs")

@app.post("/")
async def generate_recommendations(input: YAMRChainInput):
    recommendations = await yamr_chain.ainvoke(input)
    return recommendations.split(YAMRChainFactory.SEPARATOR)

if __name__ == "__main__":
    uvicorn.run(app,
                host=os.environ.get("SERVER_HOST"),
                port=int(os.environ.get("SERVER_PORT")))