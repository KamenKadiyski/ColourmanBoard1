# ColourmanBoard

Проектът моделира реалния процес по използване и контрол на етикети в работна среда, като проследява качеството на отпечатаните етикети и регистрира допуснатите нередности от служителите. Системата събира, структурира и анализира данните от тези операции, след което генерира подробни отчети, които отразяват грешките, тенденциите и общото качество на изпълнение. Архитектурата е изградена така, че да поддържа реални производствени нужди и да осигурява надеждна отчетност и прозрачност.


## 🚀 Технологичен стек
*   **Backend:** [Django](https://www.djangoproject.com/)
*   **Database:** [PostgreSQL (Neon.tech)](https://neon.tech/)
*   **Environment:** [Python 3.14](https://www.python.org)
*   **Infrastructure:** [GitHub](https://github.com)
## 📁 Структура на проекта
ColourmanBoard/
│
├── .github/
├── .qodo/
├── .venv/
│
├── colourman/
├── ColourmanBoard/
├── images/
├── jobs/
├── labels/
├── reports/
├── static/
│
├── templates/
│   ├── colourman/
│   ├── jobs/
│   ├── labels/
│   ├── reports/
│   └── shared/
│       ├── 404.html
│       └── index.html
│
├── .env
├── manage.py
├── README.md
└── requirements.txt

## 🛠️ Инсталация и Настройка

Следвайте тези стъпки, за да стартирате проекта локално:

#### **Стъпка 1: Клониране и Среда**
1. Използвайте `git clone` за сваляне на кода : gh repo clone KamenKadiyski/ColourmanBoard1   
   или git clone https://github.com/KamenKadiyski/ColourmanBoard1.git
2. Активирайте виртуална среда (`venv`), за да не замърсявате системните си пакети.
   ```bash
    python -m venv venv
    # За Windows:
    venv\Scripts\activate
    # За macOS/Linux:
    source venv/bin/activate

3. Инсталирайте нужните библиотеки и пакети с помощта на `requirements.txt` файла.
   ```bash
   pip install -r requirements.txt

4.За да стартирате проекта с готовата база данни, създайте файл `.env` и поставете следното:
   ```bash
   DATABASE_URL='postgresql://neondb_owner:npg_qgncKi2OVo8l@ep-super-flower-aipfcska.c-4.us-east-1.aws.neon.tech/colourmen?sslmode=require&channel_binding=require'
```

5. 


