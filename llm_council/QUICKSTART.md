# ⚡ Quick Start - Одна команда для установки

## 🚀 Установка через pipx (рекомендуется)

```bash
# 1. Установить pipx (если еще нет)
python3 -m pip install --user pipx && python3 -m pipx ensurepath

# 2. Установить LLM Council глобально
pipx install -e /home/user/claude-code-council

# 3. Использовать!
llm-council ask "What is Docker?"
```

---

## 📦 После каждого изменения кода

### Вариант 1: Переустановка (безопасно)

```bash
pipx reinstall llm_council
```

### Вариант 2: Upgrade (если из Git)

```bash
pipx upgrade llm_council
```

### Вариант 3: Для разработки (автоматически)

Если установлено с флагом `-e` (editable), изменения применяются автоматически!

```bash
# Изменили код? Просто вызовите:
llm-council version  # Сразу увидите изменения!
```

---

## 🎯 Полный цикл разработки

```bash
# 1. Сделали изменения в коде
vim llm_council/cli.py

# 2. Обновили версию
echo "1.0.1" > llm_council/VERSION

# 3. Обновили CHANGELOG
vim llm_council/CHANGELOG.md

# 4. Переустановили (если не editable mode)
pipx reinstall llm_council

# 5. Протестировали
llm-council version
llm-council ask "test question"

# 6. Закоммитили
git add -A
git commit -m "Update to v1.0.1"
git push
```

---

## ⚙️ Команды после установки

```bash
# Основное использование
llm-council ask "your question"
llm-council "short syntax"

# Управление
llm-council models     # Список моделей
llm-council setup      # Настройка API ключей
llm-council config     # Показать конфигурацию
llm-council version    # Версия

# Короткий алиас
council ask "same as llm-council"
```

---

## 🔄 Одна команда для всего (копировать целиком)

### Первая установка:

```bash
cd /home/user/claude-code-council && \
  python3 -m pip install --user pipx 2>/dev/null || true && \
  python3 -m pipx ensurepath && \
  pipx install -e . && \
  llm-council version
```

### После изменений:

```bash
pipx reinstall llm_council && llm-council version
```

### Удалить:

```bash
pipx uninstall llm_council
```

---

## ✅ Проверка работоспособности

```bash
# Должна вывести версию
llm-council version

# Должна показать список моделей
llm-council models

# Должна задать вопрос (нужны API ключи)
llm-council ask "What is 2+2?"
```

Если команда не найдена:
```bash
source ~/.bashrc  # или ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

---

## 💡 Pro Tips

### 1. Быстрая проверка после изменений

```bash
# Editable mode - изменения применяются автоматически!
pipx install -e /path/to/llm-council

# Теперь просто редактируйте код и запускайте:
llm-council version  # Сразу видны изменения!
```

### 2. Тестирование нового кода

```bash
# В одной команде
cd /home/user/claude-code-council/llm_council && \
  python -m llm_council ask "test"
```

### 3. Быстрый reinstall

```bash
alias llm-reinstall="pipx reinstall llm_council && llm-council version"

# Теперь просто:
llm-reinstall
```

---

## 📊 Сравнение методов установки

| Метод | Команда | Изменения применяются | Где доступно |
|-------|---------|----------------------|--------------|
| **pipx -e** | `pipx install -e .` | Автоматически ✅ | Везде 🌍 |
| **pipx** | `pipx install .` | Нужен reinstall | Везде 🌍 |
| **python** | `python cli.py` | Сразу | Только в директории 📁 |
| **pip** | `pip install .` | Нужен reinstall | Глобально ⚠️ |

**Рекомендация:** `pipx install -e` для разработки!

---

## 🎯 Workflow для продуктивности

```bash
# Alias в ~/.bashrc или ~/.zshrc
alias llm="llm-council"
alias ask="llm-council ask"
alias llm-reload="pipx reinstall llm_council"

# Теперь:
ask "What is async?"
llm models
llm-reload  # После изменений
```
