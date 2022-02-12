from fastapi import APIRouter

router = APIRouter()


@router.get('/')
async def root():
    return 'this is root. Will be more here later'
