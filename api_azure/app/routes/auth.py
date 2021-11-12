from fastapi import APIRouter, Depends

router = APIRouter(prefix='/auth')


@router.get('/')
def test(
):
    return {}
