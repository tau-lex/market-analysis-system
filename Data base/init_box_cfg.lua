#!/usr/bin/env tarantool
-- Ïðèìåð ñêðèïòà äëÿ èíèöèàëèçàöèè Òàðàíòóë
-- box.cfg{ key = value [, key = value ...]]}
box.cfg{
	background,
	-- Run the server as a background task. The logger and pid_file parameters must be non-null for this to work.
	--Type: boolean
	--Default: false

	custom_proc_title = 'MAS',
	-- Add the given string to the server's Process title
	--Type: string
	--Default: null
	--Dynamic: yes
	
	listen,
	-- The read/write data port number or URI (Universal Resource Identifier) string. Has no default value, so must be specified if connections will occur from remote clients that do not use “admin address” (the administrative host and port).
	--Type: integer or string
	--Default: null
	--Dynamic: yes
	
	pid_file,
	-- Store the process id in this file. Can be relative to work_dir. A typical value is “tarantool.pid”.
	--Type: string
    --Default: null
	
	read_only,
	-- Put the server in read-only mode. After this, any requests that try to change data will fail with error ER_READONLY.
    --Type: boolean
    --Default: false
    --Dynamic: yes
	
	snap_dir,
	-- A directory where snapshot (.snap) files will be stored. Can be relative to work_dir. If not specified, defaults to work_dir. See also wal_dir.
    --Type: string
    --Default: "."
	
	vinyl_dir,
    -- A directory where vinyl files or sub-directories will be stored. Can be relative to work_dir. If not specified, defaults to work_dir.
	--Type: string
    --Default: "."
	
	username,
	-- UNIX user name to switch to after start.
	--Type: string
    --Default: null
	
	wal_dir,
	-- A directory where write-ahead log (.xlog) files are stored. Can be relative to work_dir. Sometimes wal_dir and snap_dir are specified with different values, so that write-ahead log files and snapshot files can be stored on different disks. If not specified, defaults to work_dir.
	--Type: string
    --Default: "."
	
	work_dir
	-- A directory where database working files will be stored. The server switches to work_dir with chdir(2) after start. Can be relative to the current directory. If not specified, defaults to the current directory. Other directory parameters may be relative to work_dir, for example
    --box.cfg{work_dir='/home/user/A',wal_dir='B',snap_dir='C'}
    --will put xlog files in /home/user/A/B, snapshot files in /home/user/A/C, and all other files or sub-directories in /home/user/A.
    --Type: string
    --Default: null
}
-- next https://tarantool.org/doc/book/configuration/index.html#id6
