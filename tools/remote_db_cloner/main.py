# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def get_mongo_client() -> MongoClient:
    """
    Get the mongo client.
    Caches the client, since it can not be created more than once.
    :return: MongoClient.
    """
    client = MongoClient(
        f"mongodb+srv://{quote_plus('produce_exchange_hub_api_dev')}:"
        f"{quote_plus('?x?x9e9h@7T45dNe')}"
        "@dev01.sokvl.mongodb.net/produce-exchange-hub-test"
        "?retryWrites=true&w=majority",
        tlsCAFile=certifi.where(),
    )
    return client


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
