#!/usr/bin/env tarantool
-- tarantool v1.6
-- Это по умолчанию файл инициализации Tarantool
-- с простым в использовании примеры конфигурации, 
-- включая репликацию, сегментирование и всех основных функций
-- Complete documentation available in:  http://tarantool.org/doc/
--
-- чтобы начать этот пример просто запустите "sudo tarantoolctl start example" 
-- или использовать сценарии инициализации, предоставляемые бинарными пакетами.
-- Для того, чтобы подключиться к экземпляру, используйте "sudo tarantoolctl enter example"
-- Features:
-- 1. Database configuration
-- 2. Binary logging and snapshots
-- 3. Replication
-- 4. Automatinc sharding
-- 5. Message queue
-- 6. Data expiration

-----------------
-- Configuration
-----------------
box.cfg {
    --------------------
    -- Basic parameters
    --------------------

    -- Абсолютный путь к каталогу, в котором записи сохраняются вперед файла 
    -- журнала (.xlog). Если не указано, по умолчанию /var/lib/tarantool/INSTANCE
    -- wal_dir = nil;

    -- Абсолютный путь к каталогу, в котором сохраняются файлы снимков(.snap).
    -- If not specified, defaults to /var/lib/tarantool/INSTANCE
    -- snap_dir = nil;

    -- Абсолютный путь к каталогу, в котором хранятся файлы Sophia.
    -- If not specified, defaults to /var/lib/tarantool/INSTANCE
    -- sophia_dir = nil;

    -- The read/write data port number or URI
    -- не имеет значения по умолчанию, поэтому необходимо указать, если 
	-- подключение будет происходить от удаленных клиентов, которые 
	-- не используют "адрес администратора"
    listen = 3301;

    -- Выводит данную строку в названии процесса сервера
    -- custom_proc_title = 'example';

    -------------------------
    -- Storage configuration
    -------------------------

    -- Сколько памяти Tarantool выделяет на самом деле для хранения 
	-- кортежей, в гигабайтах
    slab_alloc_arena = 0.5;

    -- Размер самого маленького выделенного блока
    -- Он может быть настроен, если большинство из кортежей не настолько малы
    slab_alloc_minimal = 16;

    -- Размер самого большого выделенного блока
    -- It can be tuned up if it is necessary to store large tuples
    slab_alloc_maximal = 1048576;

    -- Используйте slab_alloc_factor как множитель для вычисления размеров областей памяти, где хранятся кортежи
    slab_alloc_factor = 1.06;

    -------------------
    -- Snapshot daemon
    -------------------

    -- Интервал между действиями snapshot демона, в секундах
    snapshot_period = 0;

    -- Максимальное количество снимков, которое поддерживает snapshot демон
    snapshot_count = 6;

    --------------------------------
    -- Binary logging and snapshots
    --------------------------------

    -- Прервать, если есть ошибка при чтении файла снимка (при запуске сервера)
    panic_on_snap_error = true;

    -- Прервать если есть ошибка при чтении файла журнала 
	-- (при запуске сервера или передаче на реплику)
    panic_on_wal_error = true;

    -- Сколько записей журнала для сохранения одного лог-файла
    rows_per_wal = 5000000;

    -- Уменьшите дроссельный эффект box.snapshot () на 
	-- INSERT/UPDATE/DELETE производительность, установив ограничение 
	-- на сколько мегабайт в секунду он может записать на диск
    snap_io_rate_limit = nil;

    -- Specify fiber-WAL-disk synchronization mode as:
    -- "none": write-ahead log is not maintained;
    -- "write": fibers wait for their data to be written to the write-ahead log;
    -- "fsync": fibers wait for their data, fsync follows each write;
    wal_mode = "none";

    -- Количество секунд между периодическими сканированиями каталога 
	-- файла журнала
    wal_dir_rescan_delay = 2.0;

    ---------------
    -- Replication
    ---------------

    -- Сервер рассматривается в качестве реплики Tarantool. 
	-- Он будет пытаться подключиться к мастеру, который в качестве 
	-- replication_source определяет URI
    -- for example konstantin:secret_password@tarantool.org:3301
    -- by default username is "guest"
    -- replication_source="127.0.0.1:3102";

    --------------
    -- Networking
    --------------

    -- The server will sleep for io_collect_interval seconds
    -- between iterations of the event loop
    io_collect_interval = nil;

    -- The size of the read-ahead buffer associated with a client connection
    readahead = 16320;

    -----------
    -- Logging
    -----------

    -- How verbose the logging is. There are six log verbosity classes:
    -- 1 – SYSERROR
    -- 2 – ERROR
    -- 3 – CRITICAL
    -- 4 – WARNING
    -- 5 – INFO
    -- 6 – DEBUG
    log_level = 5;

    -- By default, the log is sent to /var/log/tarantool/INSTANCE.log
    -- If logger is specified, the log is sent to the file named in the string
    -- logger = "example.log";

    -- If true, tarantool does not block on the log file descriptor
    -- when it’s not ready for write, and drops the message instead
    logger_nonblock = true;

    -- If processing a request takes longer than
    -- the given value (in seconds), warn about it in the log
    too_long_threshold = 0.5;
}

-- Test connectors
box.schema.space.create('examples',{id=999})
box.space.examples:create_index('primary', {type = 'hash', parts = {1, 'unsigned'}})
box.schema.user.grant('guest','read,write','space','examples')
box.schema.user.grant('guest','read','space','_space')

local function bootstrap()
    local space = box.schema.create_space('example')
    space:create_index('primary')
    -- Закомментируйте это, если вам нужно разграниченный контроль доступа (без него, гость будет иметь доступ ко всему)
    box.schema.user.grant('guest', 'read,write,execute', 'universe')

    -- Keep things safe by default
    --  box.schema.user.create('example', { password = 'secret' })
    --  box.schema.user.grant('example', 'replication')
    --  box.schema.user.grant('example', 'read,write,execute', 'space', 'example')
end

-- для первого запуска создать пространство и добавить установленные гранты
box.once('example-1.0', bootstrap)

-----------------------
-- Automatinc sharding
-----------------------
-- Обрати особое внимание вам необходимо установить пакет tarantool-shard 
-- чтобы использовать shadring
-- Docs: https://github.com/tarantool/shard/blob/master/README.md
-- Example:
--local shard = require('shard')
--local shards = {
--    servers = {
--        { uri = [[host1.com:4301]]; zone = [[0]]; };
--        { uri = [[host2.com:4302]]; zone = [[1]]; };
--    };
--    login = 'tester';
--    password = 'pass';
--    redundancy = 2;
--    binary = '127.0.0.1:3301';
--    monitor = false;
--}
--shard.init(shards)

-----------------
-- Message queue
-----------------
-- Обрати особое внимание вам необходимо установить пакет tarantool-queue чтобы использовать очереди
-- Docs: https://github.com/tarantool/queue/blob/master/README.md
-- Example:
--queue = require('queue')
--queue.start()
--queue.create_tube(tube_name, 'fifottl')

-------------------
-- Data expiration
-------------------
-- N.B. you need to install tarantool-expirationd package to use expirationd
-- Docs: https://github.com/tarantool/expirationd/blob/master/README.md
-- Example:
--job_name = 'clean_all'
--expirationd = require('expirationd')
--function is_expired(args, tuple)
--  return true
--end
--function delete_tuple(space_id, args, tuple)
--  box.space[space_id]:delete{tuple[1]}
--end
--expirationd.run_task(job_name, space.id, is_expired, {
--    process_expired_tuple = delete_tuple, args = nil,
--    tuple_per_item = 50, full_scan_time = 3600
--})
