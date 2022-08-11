"""
Module for paging information dependency.
"""
from fastapi import Query


class PagingInformation:
    """
    Data class for paging information.
    """

    def __init__(self, take: int, skip: int):
        self.take = take
        self.skip = skip


def get_paging_information(
    take: int = Query(20),
    skip: int = Query(0),
) -> PagingInformation:
    """
    Dependency injection method for Paging information.
    :param take: Number of items to take. Default=20.
    :param skip: Number of items to skip. Default=0.
    :return: PagingInformation.
    """
    return PagingInformation(take, skip)
