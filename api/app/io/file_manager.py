from io import open
from os.path import splitext, join
from pathlib import Path

from fastapi import Depends, UploadFile

from app.dependencies.log import AppLogger, AppLoggerInjector
from app.errors import NotFoundError

logger_injector = AppLoggerInjector("FileManager")


class FileManager:
    def __init__(self, file_root: str, logger: AppLogger):
        self._file_root = file_root
        self._logger = logger

    @property
    def _profile_picture_path(self):
        return join(self._file_root, "profile_picturs")

    async def save_profile_picture(self, company_id: str, upload_file: UploadFile) -> str:
        self._logger.debug(f"save_profile_picture(company_id={company_id})")
        file_name = company_id + splitext(upload_file.filename)[1]
        file_path = join(self._profile_picture_path, file_name)
        self._logger.debug(f"save_profile_picture: file_path={file_path}")

        with open(file_path, mode="wb") as file:
            file.write(await upload_file.read())
            self._logger.debug(f"save_profile_picture: File written to path {file_path}")

        url_path = f"/profile-pictures/{file_name}"
        self._logger.debug(f"save_profile_picture: url_path={url_path}")
        return url_path

    def get_profile_picture_physical_path(self, image_file_name: str) -> str:
        image_file_path = join(self._profile_picture_path, image_file_name)
        if not Path(image_file_path).exists():
            raise NotFoundError(f"There's no picture with the name '{image_file_name}'")
        return image_file_path


def get_file_manager(logger: AppLogger = Depends(logger_injector)) -> FileManager:
    return FileManager("C:/produce_exchange_hub/images/", logger)
