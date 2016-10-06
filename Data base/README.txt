Module name: Data base
Short name: masdb
OS: GNU Linux x86
Platform, framework: Redis 3.2.4 (Tarantool 1.6.9)

Description: роль модуля в следующем - центр хранения всех конфигураций и данных, узел обмена данными.

Redis:
/home/mint/redis_masdb/ - рабочий каталог.
redis-masdb.conf - файл конфигурации сервера.

Tarantool:
/home/mint/tarantool_masdb/ - рабочий каталог.
masdb.lua, masdb_http.lua, example.lua - файлы конфигурации сервера.
masdb_lib.lua - библиотека функций masdb(/usr/share/tarantool/).