#!/bin/bash


# Путь к папке с миграциями
MIGRATIONS_DIR="./migrations/"

# Создание папки с миграциями (если не существует)
if [ ! -d "$MIGRATIONS_DIR" ]; then
    flask db init -d "$MIGRATIONS_DIR"
    flask db migrate -d "$MIGRATIONS_DIR" -m "new_migration"
    flask db upgrade -d "$MIGRATIONS_DIR"
fi
exec "$@"