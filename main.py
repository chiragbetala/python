from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import get_all_routers
import uvicorn

app = FastAPI()

# Allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Automatically register all routers
for router in get_all_routers():
    app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    import uvicorn
    import pathlib
    import sys
    
    # Add the project directory to Python path
    sys.path.append(str(pathlib.Path(__file__).parent))
    
    uvicorn.run(
        app,  # Pass the app instance directly
        host="0.0.0.0",
        port=8000,
        reload=True
    )