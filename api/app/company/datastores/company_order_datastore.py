# from fastapi import Depends
#
# from app.authentication.models.db.user import User
# from app.company.datastores.company_datastore import CompanyDatastore
# from app.company.models.db.order import Order
# from app.company.models.v1.orders import AddOrderModel
# from app.database.abstract.document_database import DocumentDatabase
# from app.database.dependencies.document_database import get_document_database
# from app.logging.log import AppLogger, AppLoggerInjector
# from app.shared.models.db.change import Change, ChangeType
#
# logger_injector = AppLoggerInjector("CompanyOrderDatastore")
#
#
# class CompanyOrderDatastore(CompanyDatastore):
#     def __init__(self, db: DocumentDatabase, logger: AppLogger):
#         super().__init__(db, logger)
#
#     def add_order(self, company_id: str, order_model: AddOrderModel, authenticated_user: User) -> Order:
#         update_context = self.db.update_context()
#         new_order = Order.create(
#             self.db.new_id(),
#             order_model.product_id,
#             order_model.description,
#             order_model.price_per_unit,
#             order_model.unit_type,
#             order_model.currency,
#         )
#         update_context.push_to_list("orders", new_order.dict())
#         update_context.push_to_list(
#             "changes",
#             Change.create(
#                 self.db.new_id(), f"orders/{new_order.id}", ChangeType.add, authenticated_user.email, new_order.dict()
#             ).dict(),
#         )
#         self._companies.update_document(company_id, update_context)
#         return new_order
#
#
# def get_company_order_datastore(
#     db: DocumentDatabase = Depends(get_document_database),
#     logger: AppLogger = Depends(logger_injector),
# ) -> CompanyOrderDatastore:
#     return CompanyOrderDatastore(db, logger)
