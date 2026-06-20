# Python API Autotests

API-тесты для [LearnQA Playground](https://playground.learnqa.ru/) на **PyTest + requests + Allure**.

Fluent API-клиент, pydantic-settings, positive/negative классы (как в enterprise-фреймворках).

## Portfolio

| Проект | Описание |
|--------|----------|
| **API** (этот repo) | [pytest-api-automation](https://github.com/Arman0228/pytest-api-automation) |
| **UI** | [playwright-ui-automation](https://github.com/Arman0228/playwright-ui-automation) |
| **LLM QA** | [llm-qa-automation-framework](https://github.com/Arman0228/llm-qa-automation-framework) |

## Архитектура

```
api/clients/              # Fluent API clients (BaseApi, UserApiClient)
config/settings.py        # Pydantic Settings (ENV → base URL)
tests/user/
  auth/                   # TestPositiveUserAuth / TestNegativeUserAuth
  register/               # TestPositiveUserRegister / TestNegativeUserRegister
  get/                    # TestPositiveUserGet / TestNegativeUserGet
  edit/                   # TestPositiveUserEdit / TestNegativeUserEdit
  delete/                 # TestPositiveUserDelete / TestNegativeUserDelete
  data.py                 # Test data builders
  helpers.py              # register_user / login_user
tests/conftest.py         # Fixtures: api, auth_session
helpers/                  # Request logging
resources/schemas/        # JSON Schema
tests/user/paths.py       # SCHEMAS_DIR constant
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
class TestPositiveUserAuth:
    @pytest.mark.positive
    def test_positive_auth_user(self, api, auth_session):
        api.auth(auth_session.token, auth_session.auth_sid)
        api.response_json_value_by_name_should_be("user_id", auth_session.user_id)
```

## Запуск

```bash
pytest -m positive -v              # только позитивные
pytest -m negative -v              # только негативные
pytest -m smoke -v                 # smoke suite
pytest tests/user/auth/ -v         # auth feature
pytest tests/ --alluredir=allure-results
```

## CI

GitHub Actions (`.github/workflows/ci.yml`) — pytest на каждый push/PR.

## Стек

Python 3.11 · PyTest · requests · pydantic-settings · jsonschema · Allure
