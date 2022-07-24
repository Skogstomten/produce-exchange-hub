from io import open
from os.path import splitext, join
from pathlib import Path

from fastapi import Depends, UploadFile

from app.shared.dependencies.log import AppLogger, AppLoggerInjector
from app.shared.errors import NotFoundError

logger_injector = AppLoggerInjector("FileManager")


def _get_profile_picture_physical_path(image_file_name: str, directory: str) -> str:
    image_file_path = join(directory, image_file_name)
    if not Path(image_file_path).exists():
        raise NotFoundError(f"There's no picture with the name '{image_file_name}'")
    return image_file_path


class FileManager:
    def __init__(self, file_root: str, logger: AppLogger):
        self._file_root = file_root
        self._logger = logger

        self._ensure_folders_exist()

    @property
    def _company_profile_picture_path(self) -> str:
        return join(self._file_root, "profile_picturs")

    @property
    def _user_profile_picture_path(self) -> str:
        return join(self._file_root, "user_profile_pictures")

    async def save_company_profile_picture(self, company_id: str, upload_file: UploadFile) -> str:
        return await self._save_profile_picture(
            "company_id", company_id, upload_file, self._company_profile_picture_path
        )

    def get_company_profile_picture_physical_path(self, image_file_name: str) -> str:
        return _get_profile_picture_physical_path(image_file_name, self._company_profile_picture_path)

    def get_user_profile_picture_physical_path(self, image_file_name: str) -> str:
        return _get_profile_picture_physical_path(image_file_name, self._user_profile_picture_path)

    async def save_user_profile_picture(self, user_id: str, file: UploadFile) -> str:
        return await self._save_profile_picture("user_id", user_id, file, self._user_profile_picture_path)

    async def _save_profile_picture(
        self, id_name: str, entity_id: str, upload_file: UploadFile, directory_path: str
    ) -> str:
        self._logger.debug(f"save_profile_picture({id_name}={entity_id})")
        file_name = entity_id + splitext(upload_file.filename)[1]
        file_path = join(directory_path, file_name)
        self._logger.debug(f"save_profile_picture: file_path={file_path}")

        with open(file_path, mode="wb") as file:
            file.write(await upload_file.read())
            self._logger.debug(f"save_profile_picture: File written to path {file_path}")

        url_path = f"/profile-pictures/{file_name}"
        self._logger.debug(f"save_profile_picture: url_path={url_path}")
        return url_path

    def _ensure_folders_exist(self):
        Path(self._company_profile_picture_path).mkdir(parents=True, exist_ok=True)
        Path(self._user_profile_picture_path).mkdir(parents=True, exist_ok=True)


def get_file_manager(logger: AppLogger = Depends(logger_injector)) -> FileManager:
    return FileManager("C:/produce_exchange_hub/images/", logger)
