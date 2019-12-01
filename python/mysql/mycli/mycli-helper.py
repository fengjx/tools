# -*- coding: utf-8 -*-


import argparse
import random
import socket
import os
import time
from sshtunnel import SSHTunnelForwarder
from configparser import ConfigParser


def get_available_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('', 0))
        _, port = sock.getsockname()
        return port
    except EOFError as err:
        print(err)
        print('port %d is used, retry...' % port)
        return get_available_port()
    finally:
        sock.close()

def input_num(len):
    try:
        num = int(input())
        if num > (len - 1):
            print("没有找到配置项，请重新输入配置编号")
            return input_num(len)
        elif num < 0:
            print("没有找到配置项，请重新输入配置编号") 
            return input_num(len)
        return num    
    except:
        print("请输入正确的编号")
        return input_num(len)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("mycli helper")

    parser.add_argument("-c", "--config", default="mycli.ini",
                        help="配置文件，默认当前目录下的 mycli.ini")

    cfg_path = parser.parse_args().config

    print("加载配置： %s" % cfg_path)

    cfg = ConfigParser(allow_no_value=True)
    cfg.read(cfg_path)
    sections = cfg.sections()
    print("情输入连接的MySQL实例编号")
    for i, item in enumerate(sections):
        print("[%d] - %s, %s" % (i, item, cfg.get(item, "desc")))

    num = input_num(len(sections))
    section = sections[num]
    server_cfg = cfg[section]
    local_port = get_available_port()
    print("connect to %s, bind local port %d" % (section, local_port))

    server = None
    if cfg.has_option(section, "remote_password"):
        server = SSHTunnelForwarder(
            ssh_address_or_host=(
                server_cfg.get("remote_host"), server_cfg.getint("remote_port")),
            ssh_username=server_cfg.get("remote_username"),
            ssh_password=server_cfg.get("remote_password"),
            remote_bind_address=(
                server_cfg.get("mysql_host"), server_cfg.getint("mysql_port")),
            local_bind_address=('127.0.0.1', local_port)
        )
    else:
        server = SSHTunnelForwarder(
            ssh_address_or_host=(
                server_cfg.get("remote_host"), server_cfg.getint("remote_port")),
            ssh_username=server_cfg.get("remote_username"),
            ssh_pkey=server_cfg.get("remote_pkey"),
            ssh_private_key_password=server_cfg.get(
                "remote_pkey_password", ""),
            remote_bind_address=(
                server_cfg.get("mysql_host"), server_cfg.getint("mysql_port")),
            local_bind_address=('127.0.0.1', local_port)
        )
    server.start()

    cmd = ["mycli", "mysql://%s:%s@127.0.0.1:%d" % (server_cfg.get("mysql_user"), server_cfg.get("mysql_password"), local_port)]
    print(" ".join(cmd))
    os.system(" ".join(cmd))

    server.stop()
