namespace ProduceExchangeHub.Services;

public class BlazoredLocalStorageWrapper : ILocalStorage
{
    private readonly ILocalStorageService _localStorage;

    public BlazoredLocalStorageWrapper(ILocalStorageService localStorage)
    {
        _localStorage = localStorage;
    }

    public ValueTask SaveAsync<T>(StorageKey key, T item) => _localStorage.SetItemAsync(key.ToString(), item);

    public async ValueTask<T?> GetAsync<T>(StorageKey key)
    {
        if (await _localStorage.ContainKeyAsync(key.ToString()))
            return await _localStorage.GetItemAsync<T>(key.ToString());
        return default;
    }
}