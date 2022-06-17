from fastapi import Query


class PagingInformation:
    def __init__(self, take: int, skip: int):
        self.take = take
        self.skip = skip


def get_paging_information(
    take: int = Query(20),
    skip: int = Query(0),
) -> PagingInformation:
    return PagingInformation(take, skip)
