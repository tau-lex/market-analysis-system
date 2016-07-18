#!/usr/bin/env tarantool
-- Пример стартового скрипта для запуска Таратул
-- Скрипт использует функции ОС и параметр
box.cfg{
	listen				= os.getenv("LISTEN_URI"),
	slab_alloc_arena	= 0.1,
	pid_file			= "tarantool.pid",
	rows_per_wal		= 50
}
print('Starting ', arg[1])

--		$ export LISTEN_URI=3301
--		$ ~/tarantool/src/tarantool script.lua ARG
--		... ...
--		Starting  ARG
--		... ...