# from fastapi import APIRouter, Depends
#
# from ..dependencies.firebase_auth import get_auth_client, Client
#
# router = APIRouter(prefix='/auth')
#
#
# @router.get('/')
# def test(
#         client: Client = Depends(get_auth_client)
# ):
#     return {}
