from fastapi import APIRouter, Request


router = APIRouter()


@router.get("/postgres")
async def get_hello_world(
    request: Request,
):
    return await request.app.state.pool.fetch(
        """
        select
            1 as number,
            'yes' as string,
            '{
                "cool": true,
                "wow": [1, 2, 3]
            }'::json as json,
            array['a', 'b', 'c'] as array
    """)
