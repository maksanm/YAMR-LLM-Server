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
    MAX_REQUEST_RETRY_COUNT = int(os.environ.get("MAX_REQUEST_RETRY_COUNT"))
    RECOMMENDATIONS_COUNT = os.environ.get("RECOMMENDATIONS_COUNT")

    recommendations = []
    i = 0
    while len(recommendations) != RECOMMENDATIONS_COUNT and i < MAX_REQUEST_RETRY_COUNT:
        response = await yamr_chain.ainvoke(input)
        recommendations = response.split(YAMRChainFactory.SEPARATOR)
        i += 1

    return recommendations[-3:]

if __name__ == "__main__":
    uvicorn.run(app,
                host=os.environ.get("SERVER_HOST"),
                port=int(os.environ.get("SERVER_PORT")))