#!/usr/bin/env tarantool
box.cfg{
	--------------------
    -- Basic parameters
    --------------------
	work_dir = "/home/mint/tarantool_masdb";
--	wal_dir = "/var/log/tarantool";
	wal_dir = "wal";
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

-- Начальная загрузка()
local function bootstrap()
    local test = box.schema.create_space('test')
    test:create_index('primary')
	
	box.schema.user.create('utest', { password = 'pass' })
	box.schema.user.grant('utest', 'read,write,execute', 'space', 'test')
	box.schema.user.grant('guest','read,write','space','test')
	
    -- Закомментируйте это, если вам нужно разграниченный контроль доступа (без него, гость будет иметь доступ ко всему)
    --box.schema.user.grant('guest', 'read,write,execute', 'universe')
	
    -- Держите вещи безопасными по умолчанию
    --  box.schema.user.create('utest', { password = 'pass' })
    --  box.schema.user.grant('utest', 'replication')
    --  box.schema.user.grant('utest', 'read,write,execute', 'space', 'test')
end

-- для первого запуска создать пространство и добавить права пользователей
box.once('testrun-1.0', bootstrap)