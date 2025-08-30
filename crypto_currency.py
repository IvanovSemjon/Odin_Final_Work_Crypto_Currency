import requests
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# ТОП 20 популярных криптовалют по версии CoinGecko API
cryptocurrencies = {
    "bitcoin": "Bitcoin (BTC)",
    "ethereum": "Ethereum (ETH)",
    "tether": "Tether (USDT)",
    "binancecoin": "Binance Coin (BNB)",
    "solana": "Solana (SOL)",
    "usd-coin": "USD Coin (USDC)",
    "ripple": "Ripple (XRP)",
    "cardano": "Cardano (ADA)",
    "dogecoin": "Dogecoin (DOGE)",
    "polkadot": "Polkadot (DOT)",
    "tron": "Tron (TRX)",
    "chainlink": "Chainlink (LINK)",
    "polygon": "Polygon (MATIC)",
    "wrapped-bitcoin": "Wrapped Bitcoin (WBTC)",
    "litecoin": "Litecoin (LTC)",
    "bitcoin-cash": "Bitcoin Cash (BCH)",
    "avalanche-2": "Avalanche (AVAX)",
    "dai": "Dai (DAI)",
    "uniswap": "Uniswap (UNI)",
    "cosmos": "Cosmos (ATOM)"
}

# ТОП 20 самых популярных валют
fiat_currencies = {
    "usd": "Доллар США (USD)",
    "eur": "Евро (EUR)",
    "gbp": "Фунт стерлингов (GBP)",
    "jpy": "Японская иена (JPY)",
    "cny": "Китайский юань (CNY)",
    "aud": "Австралийский доллар (AUD)",
    "cad": "Канадский доллар (CAD)",
    "chf": "Швейцарский франк (CHF)",
    "hkd": "Гонконгский доллар (HKD)",
    "sgd": "Сингапурский доллар (SGD)",
    "sek": "Шведская крона (SEK)",
    "nok": "Норвежская крона (NOK)",
    "krw": "Южнокорейская вона (KRW)",
    "inr": "Индийская рупия (INR)",
    "brl": "Бразильский реал (BRL)",
    "rub": "Российский рубль (RUB)",
    "try": "Турецкая лира (TRY)",
    "zar": "Южноафриканский рэнд (ZAR)",
    "mxn": "Мексиканский песо (MXN)",
    "pln": "Польский злотый (PLN)"
}


def get_crypto_price(crypto_id, vs_currency):
    """
    Получение актуальных данных о криптовалюте через бесплатный CoinGecko API
    
    Параметры:
        crypto_id (str): Уникальный идентификатор криптовалюты в системе CoinGecko
                        (например: 'bitcoin', 'ethereum', 'cardano')
        vs_currency (str): Код фиатной валюты для сравнения
                          (например: 'usd', 'eur', 'rub')
    
    Возвращает:
        dict: JSON-объект с данными о криптовалюте или None при ошибке
    """
    try:
        # Базовый URL для CoinGecko API - эндпоинт для получения простых цен
        # Этот эндпоинт позволяет получить цены многих криптовалют одновременно
        url = "https://api.coingecko.com/api/v3/simple/price"
        
        # Параметры запроса к API - определяют, какие данные мы хотим получить
        params = {
            # Идентификатор криптовалюты (можно указать несколько через запятую)
            "ids": crypto_id,
            # Валюта для отображения цен (можно указать несколько через запятую)
            "vs_currencies": vs_currency,
            # Включаем в ответ данные о рыночной капитализации
            "include_market_cap": "true",
            # Включаем в ответ данные о объеме торгов за 24 часа
            "include_24hr_vol": "true",
            # Включаем в ответ данные об изменении цены за 24 часа (в процентах)
            "include_24hr_change": "true"
        }
        
        # Отправляем HTTP GET-запрос к API
        # timeout=10 - максимальное время ожидания ответа (10 секунд)
        # params - параметры автоматически преобразуются в URL query string
        response = requests.get(url, params=params, timeout=10)
        
        # Проверяем статус ответа - вызывает исключение при ошибках HTTP
        # (например, 404 Not Found, 500 Internal Server Error и т.д.)
        response.raise_for_status()
        
        # Преобразуем JSON-ответ в Python-словарь и возвращаем его
        # Ответ содержит все запрошенные данные: цену, капитализацию, объем и изменения
        return response.json()
        
    except Exception as e:
        # Обработка всех возможных ошибок:
        # - Ошибки сети (нет интернета, недоступен сервер)
        # - HTTP ошибки (404, 500, 429 - превышен лимит запросов)
        # - Ошибки парсинга JSON (некорректный ответ от сервера)
        # - Timeout ошибки (сервер не отвечает в течение 10 секунд)
        print(f"Ошибка получения данных о криптовалюте: {e}")
        # Возвращаем None, чтобы сигнализировать о неудаче операции
        # Вызывающая функция должна проверить это значение и обработать ошибку
        return None


def show_result(amount, fiat_currency, crypto_amount, crypto_name, crypto_price, price_data):
    """Показать окно с результатом конвертации"""
    result_window = tk.Toplevel(root)
    result_window.title("Результат конвертации")
    result_window.geometry("600x300")
    
    # Основной фрейм
    frame = tk.Frame(result_window, bg="white", padx=20, pady=20)
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # Заголовок
    title = tk.Label(frame, text="Результат конвертации", font=("Arial", 14, "bold"), bg="white", fg="black")
    title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
    
    # Основной результат
    result_text = f"{amount:,.2f} {fiat_currencies[fiat_currency.lower()]} = {crypto_amount:,.8f} {crypto_name}"
    result_label = tk.Label(frame, text=result_text, font=("Arial", 12), bg="white", fg="#05658F")
    result_label.grid(row=1, column=0, columnspan=2, pady=10)
    
    # Дополнительная информация о криптовалюте
    crypto_data = price_data[crypto_name.split()[0].lower()]
    print(crypto_data)
    
    info_text = f"""
Стоимость за один {crypto_name} равняется {crypto_price:,.2f} {fiat_currencies[fiat_currency.lower()]}

Рыночная капитализация криптовалюты : {crypto_data.get(f'{fiat_currency}_market_cap', 0):,.0f} {fiat_currencies[fiat_currency.lower()]}

Объем торгов криптовалюты на бирже за 24ч: {crypto_data.get(f'{fiat_currency}_24h_vol', 0):,.0f} {fiat_currencies[fiat_currency.lower()]}

Изменение стоимости криптовалюты за последние 24ч: {crypto_data.get(f'{fiat_currency}_24h_change', 0):+.2f}%
    """
    
    info_label = tk.Label(frame, text=info_text.strip(), justify=tk.LEFT, bg="white", fg="#05658F")
    info_label.grid(row=2, column=0, columnspan=2, pady=10)
    
    # Кнопка закрытия - ИСПРАВЛЕНО: используем тот же стиль что и для основной кнопки
    close_btn = ttk.Button(frame, text="Закрыть", command=result_window.destroy, style='Custom.TButton')
    close_btn.grid(row=3, column=0, columnspan=2, pady=20)
    
    # Настройка растягивания
    frame.columnconfigure(0, weight=1)
    result_window.columnconfigure(0, weight=1)
    result_window.rowconfigure(0, weight=1)
    result_window.configure(bg="white")

def convert():
    """Выполнение конвертации"""
    try:
        # Получение данных из полей ввода
        amount = float(amount_var.get())
        
        # Получаем ключи из выбранных значений
        fiat_key = list(fiat_currencies.keys())[list(fiat_currencies.values()).index(fiat_var.get())]
        crypto_key = list(cryptocurrencies.keys())[list(cryptocurrencies.values()).index(crypto_var.get())]
        
        # Получение текущей цены криптовалюты
        price_data = get_crypto_price(crypto_key, fiat_key)
        
        if not price_data or crypto_key not in price_data:
            messagebox.showerror("Ошибка", "Не удалось получить данные о цене криптовалюты")
            return
        
        # Расчет количества криптовалюты
        crypto_price = price_data[crypto_key][fiat_key]
        crypto_amount = amount / crypto_price
        
        # Создание нового окна с результатом
        show_result(amount, fiat_key, crypto_amount, 
                   cryptocurrencies[crypto_key], crypto_price, price_data)
        
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректную сумму")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

def setup_ui():
    """Настройка пользовательского интерфейса"""
    # Основной фрейм
    main_frame = tk.Frame(root, bg="white", padx=20, pady=20)
    main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # Логотип
    logo_image = ImageTk.PhotoImage(Image.open("logo.jpg").resize((50, 50)))
    logo_label = tk.Label(main_frame, image=logo_image, bg="white")
    logo_label.image = logo_image  # Сохраняем ссылку
    logo_label.grid(row=0, column=0, padx=(0, 10), pady=(0, 20))

    # Заголовок
    title_label = tk.Label(main_frame, text="Конвертер криптовалюты", 
                           font=("Arial", 16, "bold"), bg="white")
    title_label.grid(row=0, column=1, columnspan=1, pady=(0, 20), sticky=tk.W)
    
    # Поле ввода суммы
    tk.Label(main_frame, text="Укажите сумму для расчета:", bg="white").grid(row=1, column=0, sticky=tk.W, pady=5)
    amount_entry = ttk.Entry(main_frame, textvariable=amount_var, width=20, style='Custom.TEntry')
    amount_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
    
    # Выбор фиатной валюты
    tk.Label(main_frame, text="Выберите валюту:", bg="white").grid(row=2, column=0, sticky=tk.W, pady=5)
    fiat_combo = ttk.Combobox(main_frame, textvariable=fiat_var, 
                             values=list(fiat_currencies.values()),
                             state="readonly", width=25, style='Custom.TCombobox')
    fiat_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
    
    # Выбор криптовалюты
    tk.Label(main_frame, text="Выберите криптовалюту:", bg="white").grid(row=3, column=0, sticky=tk.W, pady=5)
    crypto_combo = ttk.Combobox(main_frame, textvariable=crypto_var, 
                               values=list(cryptocurrencies.values()),
                               state="readonly", width=25, style='Custom.TCombobox')
    crypto_combo.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
    
    # Кнопка конвертации
    convert_btn = ttk.Button(main_frame, text="Посчитать", command=convert, style='Custom.TButton')
    convert_btn.grid(row=4, column=0, columnspan=2, pady=20)
    
    # Настройка весов для растягивания
    main_frame.columnconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

# Создание главного окна
root = tk.Tk()
root.title("Валютус")
root.geometry("550x250")
root.configure(bg="white")

# ========== НАСТРОЙКА СТИЛЕЙ И ЦВЕТОВОЙ СХЕМЫ ==========
style = ttk.Style()
style.theme_use('clam')  # Используем тему 'clam' для лучшей кастомизации стилей

# Кастомный стиль для выпадающих списков (Combobox)
style.configure('Custom.TCombobox', 
                fieldbackground='black',    # Белый фон внутри поля ввода
                background='white',         # Белый фон самого виджета
                bordercolor='#05658F',      # Цвет границ - темно-синий (#05658F)
                arrowcolor='#05658F',       # Цвет стрелки выпадающего списка - темно-синий (#05658F)
                borderwidth=2,              # Толщина границы - 2 пикселя для заметности
                relief='solid')             # Тип границы - сплошная линия

# Настройка состояний для Combobox (когда виджет в режиме readonly)
style.map('Custom.TCombobox',
          fieldbackground=[('readonly', 'white')],  # Белый фон поля в режиме только чтения
          background=[('readonly', 'white')])       # Белый фон виджета в режиме только чтения

# Кастомный стиль для полей ввода (Entry)
style.configure('Custom.TEntry',
                fieldbackground='white',    # Белый фон внутри поля ввода
                background='white',         # Белый фон самого виджета
                bordercolor='#05658F',      # Цвет границ - темно-синий для единообразия
                borderwidth=2,              # Толщина границы - 2 пикселя
                relief='solid')             # Тип границы - сплошная линия

# Кастомный стиль для кнопки конвертации
style.configure('Custom.TButton',
                background='#F0672F',       # Оранжевый фон кнопки (#F0672F)
                foreground='black',           # Белый цвет текста
                bordercolor='#05658F',         
                borderwidth=2,              # Убираем границу
                focuscolor='none')          # Убираем фокусную рамку
style.map('Custom.TButton',
          background=[('active', '#E55A28')])  # Более темный оранжевый при наведении


# Настройка цветов выпадающего списка (Listbox внутри Combobox)
root.option_add('*TCombobox*Listbox.background', 'white')        # Белый фон списка опций
root.option_add('*TCombobox*Listbox.selectBackground', '#05658F') # Светло-голубой фон при выделении элемента

# Глобальные переменные для хранения состояния
amount_var = tk.StringVar(value="100")
fiat_var = tk.StringVar(value="--выберите валюту--")
crypto_var = tk.StringVar(value="--выберите криптовалюту--")

# Настройка интерфейса
setup_ui()

# Запуск главного цикла
root.mainloop()
