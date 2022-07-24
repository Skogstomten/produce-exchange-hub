from fastapi import UploadFile, Depends

from app.database.abstract.document_database import DocumentDatabase
from app.company.datastores.company_datastore import CompanyDatastore
from app.database.dependencies.document_database import get_document_database
from app.shared.dependencies.log import AppLogger, AppLoggerInjector
from app.shared.io.file_manager import FileManager, get_file_manager
from app.user.models.v1.users import User
from app.shared.models.db.change import Change, ChangeType
from app.company.models.db.company import CompanyDatabaseModel

logger_injector = AppLoggerInjector("CompanyProfilePictureDatastore")


class CompanyProfilePictureDatastore(CompanyDatastore):
    def __init__(self, db: DocumentDatabase, file_manager: FileManager, logger: AppLogger):
        super().__init__(db, logger)
        self._file_manager = file_manager

    async def save_profile_picture(self, company_id: str, file: UploadFile, user: User) -> str:
        """
        Saves profile picture for company.
        If a profile picture already exists for company, it will be overwritten.
        URL of file will be stored on company in DB.
        :param company_id: ID of company to save picture for.
        :param file: Image bytes.
        :param user: Authenticated user.
        :return: URL for new file.
        :raise NotFoundError: If company was not found.
        """
        company = CompanyDatabaseModel(**self._get_company_doc(company_id))
        file_url = await self._file_manager.save_company_profile_picture(company.id, file)
        update_context = self.db.update_context()
        update_context.set_values({"profile_picture_url": file_url})
        update_context.push_to_list(
            "changes", Change.create("profile_picture_url", ChangeType.update, user.email, file_url).dict()
        )
        self._companies.update_document(
            company_id,
            update_context,
        )
        return file_url

    def get_company_profile_picture_physical_path(self, image_file_name: str) -> str:
        return self._file_manager.get_company_profile_picture_physical_path(image_file_name)


def get_company_profile_picture_datastore(
    db: DocumentDatabase = Depends(get_document_database),
    file_manager: FileManager = Depends(get_file_manager),
    logger: AppLogger = Depends(logger_injector),
) -> CompanyProfilePictureDatastore:
    return CompanyProfilePictureDatastore(db, file_manager, logger)
