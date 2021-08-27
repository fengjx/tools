# -*- coding: utf-8 -*-

"""
删除集合类型大 key
pip(3) install packaging redis
"""

import time
import sys
import redis
from packaging import version

host="localhost"
port=6379
# host="localhost"
# port=6379
del_key="test_sortedset"
count=500

redis_cli = redis.Redis(host=host, port=port, db=0)


def del_large_hash(key):
    """
    删除 hash
    """
    cursor = '0'
    while cursor != 0:
        cursor, data = redis_cli.hscan(key, cursor=cursor, count=count)
        for item in data.items():
            redis_cli.hdel(key, item[0])
            time.sleep(0.01)


def del_large_set(key):
    """
    删除 set
    """
    cursor = '0'
    while cursor != 0:
        cursor, data = redis_cli.sscan(key, cursor=cursor, count=count)
        for item in data:
            redis_cli.srem(key, item)
            time.sleep(0.01)


def del_large_list(key):
    """
    删除 list，使用 ltrim 每次删除 500 个元素
    """
    while redis_cli.llen(key)>0:
        redis_cli.ltrim(key, 0, -count)
        time.sleep(0.01)


def del_large_sortedset(key):
    """
    删除 sortedset，每次删除top 500
    """
    while redis_cli.zcard(key) > 0:
        redis_cli.zremrangebyrank(key,0, count)
        time.sleep(0.01)


def main():
    key = del_key
    if len(sys.argv) > 1:
        key = sys.argv[1]
    print("key: %s" % key)
    exists = redis_cli.exists(key)
    if not exists:
        print("key [%s] is not exists" % key)
        return

    info = redis_cli.info()
    redis_version = info["redis_version"]
    print("server version: ", redis_version)
    ver = version.parse(info["redis_version"])

    handler_fun = {
        "zset": del_large_sortedset,
        "list": del_large_list,
        "set": del_large_set,
        "hash": del_large_hash
    }

    if ver > version.parse("4.0.0"):
        # 大于 4.0.0 版本直接用 unlink，redis 会在异步线程执行删除
        print("unlink %s" % key)
        redis_cli.unlink(key)
    else:
        key_type = redis_cli.type(key).decode("utf-8")
        print("del %s:%s" % (key_type, key))
        fun = handler_fun[key_type]
        if fun:
            fun(key)
        else:
            print("no handler function")
    print("done")


if __name__ == "__main__":
    main()