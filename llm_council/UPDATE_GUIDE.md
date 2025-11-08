# 🔄 Гайд по обновлениям LLM Council

## После КАЖДОГО изменения кода

### ⚡ ОДНА КОМАНДА (используйте эту):

```bash
pipx reinstall llm_council && llm-council version
```

**Это всё!** Изменения применены, проверьте версию.

---

## 📝 Полный цикл обновления с версионированием

### 1. Сделали изменения в коде

```bash
vim llm_council/core/synthesizer.py
# или любой другой файл
```

### 2. Обновили версию

```bash
# Если минорное изменение: 1.0.0 -> 1.0.1
echo "1.0.1" > llm_council/VERSION
```

### 3. Обновили CHANGELOG.md

```bash
vim llm_council/CHANGELOG.md
```

Добавьте под `## [Unreleased]`:

```markdown
## [1.0.1] - 2025-11-07

### Fixed
- Improved consensus algorithm accuracy
- Fixed import error in gemini adapter

### Added
- New feature X
```

### 4. Переустановили и протестировали

```bash
pipx reinstall llm_council
llm-council version  # Должно показать 1.0.1
llm-council ask "Test question"
```

### 5. Закоммитили

```bash
git add -A
git commit -m "Release v1.0.1: Improved consensus algorithm"
git push
```

---

## 🎯 Схема версионирования (Semantic Versioning)

```
MAJOR.MINOR.PATCH
  |     |     |
  |     |     +-- Багфиксы (1.0.0 -> 1.0.1)
  |     +-------- Новые фичи (1.0.0 -> 1.1.0)
  +-------------- Breaking changes (1.0.0 -> 2.0.0)
```

### Примеры:

| Изменение | Старая | Новая | Причина |
|-----------|--------|-------|---------|
| Исправлен баг в синтезе | 1.0.0 | **1.0.1** | Patch (багфикс) |
| Добавлен веб UI | 1.0.1 | **1.1.0** | Minor (новая фича) |
| Изменен API адаптеров | 1.1.0 | **2.0.0** | Major (breaking change) |

---

## 🔧 Файлы для обновления

При каждом релизе обновляйте:

1. **VERSION** - номер версии
   ```bash
   echo "1.0.1" > llm_council/VERSION
   ```

2. **CHANGELOG.md** - описание изменений
   ```markdown
   ## [1.0.1] - 2025-11-07
   ### Fixed
   - Bug fix description
   ```

3. **.version.py** (опционально) - программное API
   ```python
   __version__ = "1.0.1"
   __version_info__ = (1, 0, 1)
   ```

4. **pyproject.toml** (опционально) - для публикации
   ```toml
   [project]
   version = "1.0.1"
   ```

---

## 🚀 Quick Commands для разработки

### Вариант 1: Editable Mode (рекомендуется)

```bash
# Установить один раз
pipx install -e /home/user/claude-code-council/llm_council

# Теперь изменения применяются АВТОМАТИЧЕСКИ!
# Просто редактируйте код и запускайте:
llm-council version
```

**Плюсы:**
- ✅ Не нужен reinstall после каждого изменения
- ✅ Мгновенное применение изменений
- ✅ Идеально для разработки

### Вариант 2: Regular Install

```bash
# После каждого изменения:
pipx reinstall llm_council
```

**Плюсы:**
- ✅ Как в production
- ✅ Проверяет правильность установки

---

## 📊 Checklist перед релизом

- [ ] Код работает локально
- [ ] Обновлен VERSION
- [ ] Обновлен CHANGELOG.md
- [ ] Обновлена документация (если нужно)
- [ ] Протестирован после reinstall
- [ ] Закоммичено и запушено
- [ ] Создан Git tag (опционально)

### Создание Git tag:

```bash
git tag -a v1.0.1 -m "Release v1.0.1: Description"
git push origin v1.0.1
```

---

## 🎨 Aliases для продуктивности

Добавьте в `~/.bashrc` или `~/.zshrc`:

```bash
# LLM Council development aliases
alias llm="llm-council"
alias ask="llm-council ask"
alias llm-reload="pipx reinstall llm_council && llm-council version"
alias llm-dev="cd /home/user/claude-code-council/llm_council"
alias llm-version="echo \$(cat llm_council/VERSION)"
alias llm-changelog="vim llm_council/CHANGELOG.md"

# Полный цикл обновления одной командой
alias llm-release='read -p "New version: " ver && \
  echo "$ver" > llm_council/VERSION && \
  vim llm_council/CHANGELOG.md && \
  pipx reinstall llm_council && \
  llm-council version && \
  git add -A && \
  git commit -m "Release v$ver" && \
  git push && \
  git tag -a "v$ver" -m "Release v$ver" && \
  git push origin "v$ver"'
```

После добавления:
```bash
source ~/.bashrc
llm-reload  # Быстрая переустановка!
```

---

## 💡 Troubleshooting

### "ModuleNotFoundError" после изменений

```bash
# Переустановить полностью
pipx uninstall llm_council
pipx install -e /home/user/claude-code-council/llm_council
```

### "Command not found: llm-council"

```bash
# Обновить PATH
pipx ensurepath
source ~/.bashrc
```

### Изменения не применяются

```bash
# Проверьте, установлено ли в editable mode
pipx list | grep llm_council

# Если нет "(editable)" - переустановите с -e
pipx uninstall llm_council
pipx install -e /home/user/claude-code-council/llm_council
```

---

## 🎯 Типичный workflow

```bash
# Утром: начало работы
llm-dev  # cd в директорию

# Делаете изменения
vim core/synthesizer.py

# Тестируете (если editable mode - сразу работает!)
llm-council ask "test"

# Если не editable mode:
llm-reload

# Перед коммитом: обновите версию
vim VERSION CHANGELOG.md

# Коммит и пуш
git add -A && git commit -m "Improve synthesis" && git push
```

---

## ✅ Best Practices

1. **Всегда используйте editable mode** для разработки
2. **Обновляйте VERSION** при каждом релизе
3. **Пишите в CHANGELOG** что изменилось
4. **Тестируйте после reinstall** перед коммитом
5. **Используйте git tags** для важных релизов
6. **Следуйте semver** для версий

---

**Happy coding!** 🚀
