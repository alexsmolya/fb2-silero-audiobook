# Установка в Arch Linux и CachyOS

Для проекта подготовлен пакетный шаблон в [`packaging/arch/`](../packaging/arch/). Он устанавливает приложение системно, добавляет команду `fb2-silero-audiobook`, ярлык меню и иконку.

## Почему не один универсальный Linux-бинарник

Приложение зависит от Python 3.12, Tk, FFmpeg, PyTorch, torchaudio и системного NVIDIA runtime при использовании CUDA. Один собранный файл нельзя честно объявить совместимым со всеми Linux-дистрибутивами: различаются glibc, драйверы, графические библиотеки и CUDA-runtime.

Для Arch/CachyOS пакетная установка надёжнее:

- системные компоненты ставит `pacman`;
- Python-зависимости берутся из закреплённого `uv.lock`;
- окружение приложения хранится отдельно в пользовательском каталоге;
- одна и та же установка работает на CPU и использует CUDA автоматически, если она доступна.

## Локальная проверка PKGBUILD

До первого публичного релиза создайте Git-тег, совпадающий с `pkgver` в `PKGBUILD`, например `v0.2.1`.

Затем:

```fish
cd packaging/arch
makepkg -si
```

После установки один раз подготовьте окружение:

```fish
fb2-silero-audiobook --setup
```

Команда создаёт окружение в:

```text
$XDG_DATA_HOME/fb2-silero-audiobook/venv
```

или, если `XDG_DATA_HOME` не задан:

```text
~/.local/share/fb2-silero-audiobook/venv
```

После этого приложение запускается из меню либо командой:

```fish
fb2-silero-audiobook
```

## Дополнительные форматы

Для одного FB2 Calibre не требуется. Для EPUB, MOBI, AZW/AZW3, TXT, DOCX, ODT, RTF и HTML установите:

```fish
sudo pacman -S calibre
```

## CPU и CUDA

Отдельный пакет CUDA не нужен. Закреплённое окружение PyTorch работает на CPU, если CUDA недоступна. При совместимой NVIDIA-видеокарте и драйвере приложение использует CUDA через `torch.cuda.is_available()`.

Проверка:

```fish
set env_dir (fb2-silero-audiobook --print-environment)
$env_dir/bin/python -c "import torch; print(torch.__version__); print(torch.cuda.is_available())"
```

## Сброс окружения

При повреждении окружения или после существенного изменения зависимостей:

```fish
fb2-silero-audiobook --reset-environment
fb2-silero-audiobook --setup
```

## Перед публикацией в AUR

1. Проверить отсутствие одноимённого пакета в официальных репозиториях и AUR.
2. Создать и опубликовать Git-тег и GitHub Release.
3. Обновить `pkgver` и `pkgrel`.
4. Выполнить `makepkg --printsrcinfo > .SRCINFO` в отдельном AUR-репозитории.
5. Проверить пакет командами `makepkg -si`, `namcap PKGBUILD` и `namcap` для собранного пакета.
6. Проверить ярлык через `desktop-file-validate packaging/arch/fb2-silero-audiobook.desktop`.

В основной GitHub-репозиторий хранится исходный шаблон. В AUR публикуются как минимум `PKGBUILD`, `.SRCINFO`, launcher, desktop-файл и install-hook.
