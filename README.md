# Python API Autotests

API-тесты для [LearnQA Playground](https://playground.learnqa.ru/) на **PyTest + requests + Allure**.

Демонстрирует современную структуру: fluent API-клиент, pydantic-settings, JSON Schema, pytest fixtures.

## Архитектура

```
api/clients/          # Fluent API clients (BaseApi, UserApiClient)
config/settings.py    # Pydantic Settings (ENV → base URL)
tests/user/data.py    # Test data builders
tests/conftest.py     # Fixtures: api, auth_session
resources/schemas/    # JSON Schema для валидации ответов
lib/                  # Legacy слой (MyRequests) — совместимость
```

## Быстрый старт

```bash
git clone https://github.com/Arman0228/pytest-api-automation.git
cd pytest-api-automation
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
pytest tests/ -v
```

## Конфигурация

| Переменная | Значение | URL |
|------------|----------|-----|
| `ENV=DEV` | dev stand (default) | `https://playground.learnqa.ru/api_dev` |
| `ENV=PROD` | prod stand | `https://playground.learnqa.ru/api` |

## Пример fluent-клиента

```python
def test_auth_user(api, auth_session):
    api.auth(auth_session.token, auth_session.auth_sid)
    api.response_json_value_by_name_should_be("user_id", auth_session.user_id)
```

## Запуск

```bash
pytest tests/test_user_auth.py -v          # auth suite
pytest -m smoke -v                         # smoke markers
pytest tests/ --alluredir=allure-results   # with Allure
```

## CI

GitHub Actions (`.github/workflows/ci.yml`) — pytest на каждый push/PR.

## Стек

Python 3.11 · PyTest · requests · pydantic-settings · jsonschema · Allure
