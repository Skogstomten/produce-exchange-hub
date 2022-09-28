using ProduceExchangeHub.Models;

namespace ProduceExchangeHub.Services;

public interface ILocalStorage
{
    ValueTask SaveAsync<T>(StorageKey key, T item);
    ValueTask<T?> GetAsync<T>(StorageKey key);
    ValueTask<T?> GetAsync<T>(string key);
    ValueTask RemoveValuesAsync(params StorageKey[] keys);
}