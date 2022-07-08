from app.datastores.company_datastore import CompanyDatastore


def test_add_contact_adds_contact(
    doc_database_collection_mocks,
    user_datastore,
    logger,
    contact_model,
    company_id,
    file_manager,
):
    db, collection = doc_database_collection_mocks

    target = CompanyDatastore(db, file_manager, user_datastore, logger)
    target.add_contact(company_id, contact_model)

    collection.add_to_sub_collection.assert_called_with(company_id, "contacts", contact_model)
