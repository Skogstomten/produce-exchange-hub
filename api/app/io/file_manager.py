from io import open
from os.path import join


class FileManager:
    def __init__(self, file_root: str):
        self._file_root = file_root

    def save_profile_picture(self, file_name: str, file_bytes: bytes) -> str:
        with open(join(self._file_root, "profile_picturs", file_name), mode="wb") as file:
            file.write(file_bytes)

        return f"/profile-picture/{file_name}"


def get_file_manager() -> FileManager:
    return FileManager("C:/produce_exchange_hub/images/")
