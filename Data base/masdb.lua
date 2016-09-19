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

-- Ќачальная загрузка()
local function bootstrap()
	-- test tarantool-c connector
	box.schema.space.create('examples',{id=999})
	box.space.examples:create_index('primary', {type = 'hash', parts = {1, 'unsigned'}})
	box.schema.user.grant('guest','read,write','space','examples')
	box.schema.user.grant('guest','read','space','_space')
	
    local test = box.schema.space.create('test', {id = 1999, temporary = false})
    test:create_index('primary')
	
	box.schema.user.create('utest', {password = 'password', if_not_exists = false})
	box.schema.user.grant('utest', 'read,write,execute', 'space', 'test')
	box.schema.user.grant('guest', 'read,write,execute', 'space', 'test')
--	box.schema.user.drop('utest')
	
	local config = box.schema.space.create('config', {id = 1000})
    config:create_index('primary')
	
	local history = box.schema.space.create('history', {id = 1100})
    history:create_index('primary')
	
	local brocker = box.schema.space.create('brocker', {id = 1200})
    brocker:create_index('primary')
	
	local forecast = box.schema.space.create('forecast', {id = 1300})
    forecast:create_index('primary')
	
	box.schema.user.create('masapp', {password = 'fH4^gG^5c&e34g*%FS24@hDa'})
	box.schema.user.grant('masapp', 'read,write,execute', 'universe')
	
end

-- для первого запуска создать пространство и добавить права пользователей
box.once('run-1.0', bootstrap)