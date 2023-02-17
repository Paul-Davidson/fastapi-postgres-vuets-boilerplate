from fastapi import APIRouter, Request


router = APIRouter()



@router.get("/")
async def get_hello_world(
    request: Request,
):
    return "hello world"
