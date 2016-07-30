#!/usr/bin/env tarantool
box.cfg{
	--------------------
    -- Basic parameters
    --------------------
	work_dir = "/home/mint/tarantool_masdb";
	wal_dir = "/var/log/tarantool";
	snap_dir = "snap";
	sophia_dir = "sophia";
	listen = 3313;
	custom_proc_title = 'masdb';
	pid_file = "masdb.pid";
	-------------------------
	-- Storage configuration
	-------------------------
	slab_alloc_arena = 1.5;
--	slab_alloc_minimal = 16;
--	slab_alloc_maximal = 1048576;
	slab_alloc_factor = 1.06;
	-------------------
    -- Snapshot daemon
    -------------------
--	snapshot_period = 0;
	snapshot_count = 10;
	-----------
    -- Logging
    -----------
--	log_level = 5;
	logger = "masdb.log";
	--------------------------------
    -- Binary logging and snapshots
    --------------------------------
--	panic_on_snap_error;
--	panic_on_wal_error;
--	rows_per_wal;
--	snap_io_rate_limit;
--	wal_mode;
--	wal_dir_rescan_delay
}

if masdb ~= nil then
	-- Код горячего перезапуска с помощью tarantoolctl или dofile()

	-- Выгрузить старое приложение
	masdb.stop()
	-- Очистить кэш для загруженных модулей и зависимостей
	package.loaded['masdb'] = nil
	--package.loaded['somedep'] = nil; -- зависимости 'masdb'
end

-- Загрузить новую версию приложения и все зависимости
masdb = require('masdb').start()

-- Начальная загрузка()
local function bootstrap()
    local space = box.schema.create_space('test')
    space:create_index('primary')
    -- Закомментируйте это, если вам нужно разграниченный контроль доступа (без него, гость будет иметь доступ ко всему)
    box.schema.user.grant('guest', 'read,write,execute', 'universe')

    -- Держите вещи безопасными по умолчанию
    --  box.schema.user.create('example', { password = 'secret' })
    --  box.schema.user.grant('example', 'replication')
    --  box.schema.user.grant('example', 'read,write,execute', 'space', 'example')
end

-- для первого запуска создать пространство и добавить установленные гранты
box.once('testrun-1.0', bootstrap)