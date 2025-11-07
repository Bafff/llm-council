# 📋 LLM Council - Шпаргалка команд

## 🚀 Установка (один раз)

```bash
# Автоматическая установка
bash install.sh

# Или вручную
cd /home/user/claude-code-council
python3 -m pip install --user pipx
python3 -m pipx ensurepath
pipx install -e ./llm_council
```

**После установки перезагрузите терминал или:**
```bash
source ~/.bashrc  # или ~/.zshrc
```

---

## ✅ Проверка установки

```bash
llm-council version
llm-council models
```

Должно показать версию и список моделей.

---

## 🔑 Настройка API ключей (один раз)

```bash
# Интерактивная настройка
llm-council setup

# Или вручную создайте .env файл:
cd llm_council
nano .env
```

Добавьте хотя бы Gemini (бесплатно):
```env
GOOGLE_API_KEY=ваш_ключ_здесь
```

Получить ключ: https://ai.google.dev/

---

## 💬 Использование

### Основные команды:

```bash
# Задать вопрос
llm-council ask "What is Docker?"

# Короткий синтаксис (без 'ask')
llm-council "What is async/await?"

# Еще короче (алиас)
council "Explain Python decorators"

# Показать только финальный ответ (без индивидуальных)
llm-council ask "What is CI/CD?" --hide-individual
```

### Управление:

```bash
# Список моделей и их статус
llm-council models

# Показать конфигурацию
llm-council config

# Настроить API ключи
llm-council setup

# Версия
llm-council version
```

---

## 🔄 После КАЖДОГО изменения кода

### ⚡ ОДНА КОМАНДА (копируйте эту):

```bash
pipx reinstall llm_council && llm-council version
```

**Или если установлено в editable mode (`-e` флаг):**

Изменения применяются автоматически! Просто запускайте:
```bash
llm-council version  # Сразу увидите изменения
```

---

## 📝 Обновление версии

### 1. Изменили код:

```bash
vim llm_council/core/synthesizer.py
```

### 2. Обновили версию:

```bash
echo "1.0.1" > llm_council/VERSION
```

### 3. Обновили CHANGELOG:

```bash
vim llm_council/CHANGELOG.md
```

### 4. Переустановили (если не editable mode):

```bash
pipx reinstall llm_council
```

### 5. Протестировали:

```bash
llm-council version
llm-council ask "test"
```

### 6. Закоммитили:

```bash
git add -A
git commit -m "Release v1.0.1: Description"
git push
```

---

## 🎯 Полезные алиасы

Добавьте в `~/.bashrc` или `~/.zshrc`:

```bash
# LLM Council shortcuts
alias llm="llm-council"
alias ask="llm-council ask"
alias llm-reload="pipx reinstall llm_council && llm-council version"
alias llm-dev="cd /home/user/claude-code-council/llm_council"

# После добавления:
source ~/.bashrc
```

Теперь можно:
```bash
ask "What is Kubernetes?"
llm models
llm-reload  # После изменений
llm-dev     # Перейти в директорию
```

---

## 🔧 Troubleshooting

### "Command not found: llm-council"

```bash
pipx ensurepath
source ~/.bashrc
export PATH="$HOME/.local/bin:$PATH"
```

### "ModuleNotFoundError"

```bash
pipx uninstall llm_council
pipx install -e /home/user/claude-code-council/llm_council
```

### Изменения не применяются

```bash
# Полная переустановка
pipx uninstall llm_council
cd /home/user/claude-code-council
pipx install -e ./llm_council
```

### "No models available"

```bash
# Проверьте .env файл
cat llm_council/.env

# Должно быть хотя бы:
# GOOGLE_API_KEY=AIzaSy...

# Настроить интерактивно:
llm-council setup
```

---

## 📚 Документация

| Файл | Описание |
|------|----------|
| **COMMANDS.md** | Эта шпаргалка |
| **QUICKSTART.md** | Быстрый старт |
| **UPDATE_GUIDE.md** | Гайд по разработке |
| **INSTALL_PIPX.md** | Детали установки |
| **README.md** | Полная документация |
| **EXAMPLES.md** | 18 примеров использования |
| **CHANGELOG.md** | История версий |

---

## 🎨 Примеры использования

### Техническое объяснение:

```bash
llm-council ask "Explain how JWT tokens work"
```

### Сравнение технологий:

```bash
llm-council ask "Compare PostgreSQL vs MongoDB"
```

### Принятие решений:

```bash
llm-council ask "Should I use microservices or monolith?"
```

### Отладка:

```bash
llm-council ask "Why does useEffect in React run infinitely?"
```

### Обучение:

```bash
llm-council ask "What's the best way to learn Rust?"
```

---

## 💡 Pro Tips

1. **Editable mode** для разработки:
   ```bash
   pipx install -e ./llm_council  # Изменения сразу работают!
   ```

2. **Скрывайте индивидуальные ответы** для скорости:
   ```bash
   llm-council ask "question" --hide-individual
   ```

3. **Используйте алиасы** для продуктивности:
   ```bash
   alias ask="llm-council ask"
   ask "anything"
   ```

4. **Проверяйте консенсус** для важных решений:
   - Strong consensus (>80%) = надежный ответ
   - Conflicted (<40%) = субъективный вопрос

---

## 🚀 Workflow для ежедневной работы

```bash
# 1. Установить (один раз)
bash install.sh

# 2. Настроить API ключи (один раз)
llm-council setup

# 3. Использовать!
llm-council ask "your question"

# 4. Если делаете изменения:
vim llm_council/some_file.py
pipx reinstall llm_council

# 5. Коммит
git add -A && git commit -m "message" && git push
```

---

## ⚡ Самые частые команды

```bash
# ТОП-5 команд которые вы будете использовать:

1. llm-council ask "question"           # Задать вопрос
2. llm-council models                    # Проверить модели
3. pipx reinstall llm_council            # После изменений
4. llm-council setup                     # Настройка
5. llm-council version                   # Проверить версию
```

---

**Сохраните этот файл в закладки!** 🔖

Или добавьте алиас:
```bash
alias llm-help="cat /home/user/claude-code-council/COMMANDS.md | less"
```
