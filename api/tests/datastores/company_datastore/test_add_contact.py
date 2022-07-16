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

    target = CompanyDatastore(db, logger)
    target.add_contact(company_id, contact_model)

    collection.push_to_list.assert_called_with(company_id, "contacts", contact_model)
