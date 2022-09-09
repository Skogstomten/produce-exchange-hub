namespace ProduceExchangeHub.Services;

public interface ILocalStorage
{
    ValueTask SaveAsync<T>(StorageKeys key, T item);
}