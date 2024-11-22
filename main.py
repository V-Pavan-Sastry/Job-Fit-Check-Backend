import fastapi
from typing import Optional
import fitz
import io
import geminiresp
import json
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = fastapi.FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Basic GET route
@app.get("/")
def read_root():
    return {"message": "API is Live"}

# POST to handle requests
@app.post("/upload/")
async def upload_file(
    resume: Optional[fastapi.UploadFile] = fastapi.File(None),
    jobdesc: Optional[str] = fastapi.Form(None),
    apiKey: Optional[str] = fastapi.Form(None)
):
    if resume is not None:
        if resume.content_type != "application/pdf":
            return {"error": "Only PDF files are allowed"}
        content = await resume.read()
        doc=fitz.open("pdf", io.BytesIO(content))
        text=""
        links=[]
        for page in doc:
            for link in page.get_links():
                links.append(link.get('uri')) 
            text =text +str(page.get_text())
        tx= " ".join(text.split("\n"))
        res=geminiresp.getResp(tx,jobdesc,apiKey)
        for i in range(len(res)-1):
            if res[i]=='{' :
                res=json.loads(res[i:-4])
                break
        
        return {
            "filename": resume.filename,
            "content_type": resume.content_type,
            "parsed_content":tx,
            "analysis":res,
            "links":links
        }
    return {"error": "No input provided / Incorrect Input"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",  
        host="0.0.0.0",  
        port=8000, 
        reload=True 
    )
