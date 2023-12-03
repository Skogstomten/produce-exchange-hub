"""
Module for paging information dependency.
"""
from fastapi import Query


class PagingInformation:
    """
    Data class for paging information.
    """

    def __init__(self, page: int, page_size: int):
        self.page = page
        self.page_size = page_size


def get_paging_information(
    page: int = Query(1),
    page_size: int = Query(20),
) -> PagingInformation:
    """
    Dependency injection method for Paging information.
    :param page: Number of items to take. Default=20.
    :param page_size: Number of items to skip. Default=0.
    :return: PagingInformation.
    """
    return PagingInformation(page, page_size)
