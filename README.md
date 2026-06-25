# Bert4Rec Music Recommendations

> Курсовой проект по дисциплине «Системы Искусственного Интеллекта», 4 курс

Система музыкальных рекомендаций на основе трансформерной модели **BERT4Rec**. Предсказывает следующий трек для пользователя по его истории прослушиваний.

---

## Содержание

- [Описание](#описание)
- [Стек технологий](#стек-технологий)
- [Архитектура](#архитектура)
- [Установка и запуск](#установка-и-запуск)
- [API](#api)
- [Модель BERT4Rec](#модель-bert4rec)
- [Структура проекта](#структура-проекта)

---

## Описание

Приложение позволяет пользователям:

- Регистрироваться и авторизовываться
- Слушать музыку с встроенным плеером
- Накапливать историю прослушиваний
- Получать персонализированные рекомендации от BERT4Rec
- Искать треки по жанрам и слушать «радио» со случайными треками

Музыкальные файлы загружаются с внешнего источника и кэшируются локально. Модель дообучается по мере накопления пользовательских данных через эндпоинт `/service/relearn_net`.

---

## Стек технологий

| Слой | Технологии |
|---|---|
| ML-модель | TensorFlow 2.x (режим TF1 compat), BERT4Rec |
| Backend | Python 3, FastAPI, Uvicorn |
| База данных | SQLite3 |
| Парсинг | Requests, BeautifulSoup4 |
| Frontend | React 18, React Router v6, Axios |
| Аудио | use-sound |

---

## Архитектура

```
┌─────────────────────────────────────────────────────┐
│                   React Frontend                    │
│   Аутентификация / Плеер / Радио / Рекомендации     │
└───────────────────────┬─────────────────────────────┘
                        │ HTTP (axios)
                        ▼
┌─────────────────────────────────────────────────────┐
│              FastAPI Backend (main.py)              │
│  /users  /music  /history  /service                 │
└───────┬───────────────┬─────────────────────────────┘
        │               │
        ▼               ▼
┌──────────────┐  ┌─────────────────────────────────┐
│  SQLite DB   │  │        BERT4Rec (RecommSystem)   │
│ MusicGuru.db │  │  TF Estimator + Transformer      │
└──────────────┘  └─────────────────────────────────┘
```

---

## Установка и запуск

### Требования

- Python 3.8+
- Node.js 16+ и npm

### 1. Клонировать репозиторий

```bash
git clone <repository-url>
cd Bert4Rec_Music_Recommendations
```

### 2. Backend

```bash
# Установить зависимости
pip install fastapi uvicorn tensorflow pydantic requests beautifulsoup4 termcolor

# Запустить сервер
python main.py
```

Сервер поднимется на `http://localhost:8000`.

### 3. Frontend

```bash
cd music_recommendations_app

# Установить зависимости
npm install

# Запустить dev-сервер
npm start
```

Приложение откроется на `http://localhost:3000`.

### 4. База данных

SQLite-база создаётся автоматически при первом запуске по пути `api/data/MusicGuru.db`. Миграции не требуются.

---

## API

### Пользователи

| Метод | Путь | Описание |
|---|---|---|
| GET | `/users/select` | Список всех пользователей |
| POST | `/users/insert` | Регистрация пользователя |
| POST | `/users/is_exist_by_values` | Проверка логина/пароля |

### Музыка

| Метод | Путь | Описание |
|---|---|---|
| GET | `/music/select_all_genres` | Список жанров |
| POST | `/music/insert` | Добавить трек |
| POST | `/music/get_random_music` | Случайный трек по жанру |
| POST | `/music/get_predicted_track` | Рекомендация BERT4Rec |

### История

| Метод | Путь | Описание |
|---|---|---|
| GET | `/history/select_user_last_music` | Последний прослушанный трек |
| GET | `/history/get_all_tracks_user_history` | Вся история пользователя |

### Сервис

| Метод | Путь | Описание |
|---|---|---|
| GET | `/service/get_track_file/{name}` | Скачать аудиофайл |
| POST | `/service/relearn_net` | Переобучить модель |

---

## Модель BERT4Rec

Кастомная реализация BERT, адаптированная для задачи последовательных рекомендаций (sequential recommendation).

**Конфигурация (music):**

| Параметр | Значение |
|---|---|
| Hidden size | 64 |
| Attention heads | 2 |
| Transformer layers | 2 |
| Max sequence length | 128 |
| Vocabulary size | 13 048 |
| Mask probability | 20% |
| Max predictions per seq | 20 |

**Принцип работы:**

1. История прослушиваний пользователя кодируется как последовательность item ID
2. Случайные позиции маскируются (`[MASK]` токен)
3. BERT предсказывает замаскированные треки
4. На инференсе последний элемент истории заменяется `[MASK]` — модель предсказывает следующий трек

Предобученные чекпоинты лежат в `api/models/music/`.

---

## Структура проекта

```
Bert4Rec_Music_Recommendations/
├── main.py                          # Точка входа FastAPI
├── services.py                      # DI-контейнер (БД, ML-система)
├── api/
│   ├── database/
│   │   └── Database.py              # Обёртка над SQLite
│   ├── data/
│   │   └── music/                   # Датасет, TFRecord-файлы, конфиг BERT
│   ├── models/music/                # Чекпоинты обученной модели
│   ├── getting_music.py             # Загрузчик треков
│   └── recommendation_system/
│       ├── RecommSystem.py          # Главный класс рекомендательной системы
│       ├── GeneratorData.py         # Генерация TFRecord для обучения
│       ├── model/
│       │   └── modeling/
│       │       ├── BertModel.py     # BERT-трансформер
│       │       └── BertConfig.py    # Конфигурация модели
│       └── vocab/
│           └── Vocab.py             # Словарь треков
├── server/
│   ├── api_routes/                  # FastAPI-роутеры
│   └── api_models/                  # Pydantic-схемы
└── music_recommendations_app/       # React-приложение
    └── src/
        ├── components/
        │   ├── authentication/      # Логин / регистрация
        │   └── main_window/
        │       ├── player/          # Музыкальный плеер
        │       ├── sidebar/         # Навигация
        │       └── window/          # Главная / радио / поиск
        └── scripts/backend/         # Axios-запросы к API
```
