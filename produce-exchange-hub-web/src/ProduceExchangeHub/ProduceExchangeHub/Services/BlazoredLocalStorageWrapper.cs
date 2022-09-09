namespace ProduceExchangeHub.Services;

public class BlazoredLocalStorageWrapper : ILocalStorage
{
    private readonly ILocalStorageService _localStorage;

    public BlazoredLocalStorageWrapper(ILocalStorageService localStorage)
    {
        _localStorage = localStorage;
    }

    public ValueTask SaveAsync<T>(StorageKeys key, T item) => _localStorage.SetItemAsync(key.ToString(), item);
}