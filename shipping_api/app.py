from fastapi import Depends, FastAPI, status

from .database import get_session
from .model import Batch, OrderLine, allocate
from .orm import create_database_tables

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_database_tables()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get(
    "/allocate",
    status_code=status.HTTP_201_CREATED,
    response_model=OrderLine,
)
async def allocate_endpoint(
    line: OrderLine,
    session=Depends(get_session),
):
    # Load batches from the database
    batches = session.query(Batch).all()

    # Call domain service to allocate order line
    allocate(line, batches)

    # Save allocation to database
    session.commit()

    return line
