using Blazored.LocalStorage;
using ProduceExchangeHub.Shared.Models;

namespace ProduceExchangeHub.Shared.Services;

public class BlazoredLocalStorageWrapper : ILocalStorage
{
    private readonly ILocalStorageService _localStorage;

    public BlazoredLocalStorageWrapper(ILocalStorageService localStorage)
    {
        _localStorage = localStorage;
    }

    public ValueTask SaveAsync<T>(StorageKey key, T item) => _localStorage.SetItemAsync(key.ToString(), item);
    public ValueTask<T?> GetAsync<T>(StorageKey key) => GetAsync<T>(key.ToString());

    public async ValueTask<T?> GetAsync<T>(string key)
    {
        if (await _localStorage.ContainKeyAsync(key))
            return await _localStorage.GetItemAsync<T>(key);
        return default;
    }

    public ValueTask RemoveValuesAsync(params StorageKey[] keys) =>
        _localStorage.RemoveItemsAsync(keys.Select(key => key.ToString()));
}