# Импорт необходимых библиотек
import requests  # Для HTTP-запросов к CoinGecko API
import tkinter as tk  # Основная библиотека для GUI
from tkinter import ttk, messagebox  # Стилизованные виджеты и диалоги
from PIL import Image, ImageTk  # Для работы с изображениями

# Словарь поддерживаемых криптовалют
cryptocurrencies = {
    "bitcoin": "Bitcoin (BTC)",
    "ethereum": "Ethereum (ETH)",
    "tether": "Tether (USDT)",
    "solana": "Solana (SOL)",
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
    "dai": "Dai (DAI)",
    "uniswap": "Uniswap (UNI)",
    "cosmos": "Cosmos (ATOM)"
}

# Словарь поддерживаемых фиатных валют
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
}


def get_crypto_price(crypto_id, vs_currency):
    """Получение данных о криптовалюте через CoinGecko API"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": crypto_id,
            "vs_currencies": vs_currency,
            "include_market_cap": "true",
            "include_24hr_vol": "true",
            "include_24hr_change": "true"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        print(f"Ошибка получения данных о криптовалюте: {e}")
        return None


def show_result(amount, fiat_currency, crypto_amount, crypto_name, crypto_price, price_data):
    """Создание окна с результатами конвертации"""
    # Создание нового окна
    result_window = tk.Toplevel(root)
    result_window.title("Результат конвертации")
    result_window.geometry("600x300")
    
    # Основной контейнер
    frame = tk.Frame(result_window, bg="white", padx=20, pady=20)
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # Заголовок
    title = tk.Label(frame, text="Результат конвертации", font=("Arial", 14, "bold"), bg="white", fg="black")
    title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
    
    # Основной результат
    result_text = f"{amount:,.2f} {fiat_currencies[fiat_currency.lower()]} = {crypto_amount:,.8f} {crypto_name}"
    result_label = tk.Label(frame, text=result_text, font=("Arial", 12), bg="white", fg="#05658F")
    result_label.grid(row=1, column=0, columnspan=2, pady=10)
    
    # Дополнительная информация
    crypto_data = price_data[crypto_name.split()[0].lower()]
    
    info_text = f"""
Стоимость одного {crypto_name} = {crypto_price:,.2f} {fiat_currencies[fiat_currency.lower()]}

Рыночная капитализация криптовалюты = {crypto_data.get(f'{fiat_currency}_market_cap', 0):,.0f} {fiat_currencies[fiat_currency.lower()]}

Объем торгов на бирже за 24ч = {crypto_data.get(f'{fiat_currency}_24h_vol', 0):,.0f} {fiat_currencies[fiat_currency.lower()]}

Изменение стоимости за последние 24ч = {crypto_data.get(f'{fiat_currency}_24h_change', 0):+.2f}%
    """
    
    info_label = tk.Label(frame, text=info_text.strip(), justify=tk.LEFT, bg="white", fg="#05658F")
    info_label.grid(row=2, column=0, columnspan=2, pady=10)
    
    # Кнопка закрытия
    close_btn = ttk.Button(frame, text="Закрыть", command=result_window.destroy, style='Custom.TButton')
    close_btn.grid(row=3, column=0, columnspan=2, pady=20)
    
    # Настройка растягивания
    frame.columnconfigure(0, weight=1)
    result_window.columnconfigure(0, weight=1)
    result_window.rowconfigure(0, weight=1)
    result_window.configure(bg="white")


def convert():
    """Выполнение конвертации с проверками ввода"""
    try:
        # Проверка суммы
        amount_str = amount_var.get().strip()
        if not amount_str:
            messagebox.showerror("Ошибка ввода", "Поле суммы не может быть пустым")
            return
        
        amount = float(amount_str)
        
        if amount <= 0:
            messagebox.showerror("Ошибка ввода", "Сумма должна быть больше нуля")
            return
        
        # Проверка выбора валют
        if fiat_var.get() == "--выберите валюту--" or not fiat_var.get():
            messagebox.showerror("Ошибка выбора", "Обязательно выберите фиатную валюту")
            return
        
        if crypto_var.get() == "--выберите криптовалюту--" or not crypto_var.get():
            messagebox.showerror("Ошибка выбора", "Обязательно выберите криптовалюту")
            return
        
        # Получение ключей валют
        fiat_key = list(fiat_currencies.keys())[list(fiat_currencies.values()).index(fiat_var.get())]
        crypto_key = list(cryptocurrencies.keys())[list(cryptocurrencies.values()).index(crypto_var.get())]
        
        # Получение данных о цене
        price_data = get_crypto_price(crypto_key, fiat_key)
        
        if not price_data or crypto_key not in price_data:
            messagebox.showerror("Ошибка", "Не удалось получить данные о цене криптовалюты")
            return
        
        # Расчет количества криптовалюты
        crypto_price = price_data[crypto_key][fiat_key]
        crypto_amount = amount / crypto_price
        
        # Показ результата
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

    # Инструкция
    tk.Label(main_frame,
              text="""
- в поле "Укажите сумму для расчета:" введите положительное число;
- выберите интересующую вас валюту из выпадающего списка;
- выберите интересующую вас криптовалюту для покупки;
- нажмите кнопку "Посчитать".""",
             bg="white", fg='#05658F', 
             font=("Arial", 10), justify=tk.LEFT).grid(row=4, column=0, columnspan=2, pady=(20, 0), sticky=tk.W)

    # Кнопка конвертации
    convert_btn = ttk.Button(main_frame, text="Посчитать", command=convert, style='Custom.TButton')
    convert_btn.grid(row=5, column=0, columnspan=2, pady=10)
    
    # Настройка растягивания
    main_frame.columnconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)


# Создание главного окна
root = tk.Tk()
root.title("ВалютУС")
root.geometry("550x350")
root.configure(bg="white")

# Настройка стилей
style = ttk.Style()
style.theme_use('clam')

# Стиль для выпадающих списков
style.configure('Custom.TCombobox', 
                fieldbackground='white',
                background='white',
                bordercolor='#05658F',
                arrowcolor='#05658F',
                borderwidth=2,
                relief='solid')

style.map('Custom.TCombobox',
          fieldbackground=[('readonly', 'white')],
          background=[('readonly', 'white')])

# Стиль для полей ввода
style.configure('Custom.TEntry',
                fieldbackground='white',
                background='white',
                bordercolor='#05658F',
                borderwidth=2,
                relief='solid')

# Стиль для кнопок
style.configure('Custom.TButton',
                background='#F0672F',
                foreground='black',
                bordercolor='#05658F',
                borderwidth=2,
                focuscolor='none')
style.map('Custom.TButton',
          background=[('active', '#E55A28')])

# Настройка цветов выпадающего списка
root.option_add('*TCombobox*Listbox.background', 'white')
root.option_add('*TCombobox*Listbox.selectBackground', '#05658F')

# Глобальные переменные
amount_var = tk.StringVar(value="100")
fiat_var = tk.StringVar(value="--выберите валюту--")
crypto_var = tk.StringVar(value="--выберите криптовалюту--")

# Настройка интерфейса
setup_ui()

# Запуск приложения
root.mainloop()