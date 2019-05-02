#!/usr/bin/env python3
"""UDP Ping Client"""
import argparse
from socket import *
import time
import sys

from debug import *


def _parse_args(parser):
    parser.add_argument(
        "host",
        help="Specify the ping Host"
    )
    parser.add_argument(
        "port",
        help="specify the ping Port"
    )
    parser.add_argument(
        '-c', '--count',
        default=4,
        help='count'
    )
    return parser.parse_args()


def ping(host='127.0.0.1', port=62000, count=4):

    # Statistics data
    statistics = {}
    statistics['transmitted'] = 0
    statistics['received'] = 0
    statistics['loss'] = 0

    try:
        for i in range(0, count):
            try:
                # Tic
                start_time = time.time()

                # Ping
                client_socket.sendto(b'a', (host, port))
                statistics['transmitted'] += 1

                # Set timeout
                client_socket.settimeout(1.0)

                # Pong
                client_socket.recvfrom(1024)

                # Toc
                end_time = time.time()

                # Print Static
                print(f'Pong from {host}: seq={i} time={round(end_time - start_time, 6)}ms')

                # Sleep for 1 sec
                time.sleep(1.0)

            except timeout:
                print(f'Request timeout for seq {i}')
                statistics['loss'] += 1

    except KeyboardInterrupt:
        error('KeyboardInterrupt!')
    finally:
        statistics['received'] = statistics['transmitted'] - statistics['loss']

    return statistics


def _show_statistics(host, port, statistics):
    print()
    print(f'--- {host}:{port} ping statistics ---')
    print(f'{statistics["transmitted"]} packets transmitted, {statistics["received"]} packets received, {round(statistics["loss"] / statistics["transmitted"] * 100, 1)}% packet loss')


if __name__ == '__main__':

    # Parse CLI args
    parser = argparse.ArgumentParser()
    args = _parse_args(parser)

    host = args.host

    try:
        port = int(args.port)
    except ValueError as e:
        print('Invalid port!')
        parser.print_help()
        sys.exit(0)

    try:
        count = int(args.count)
    except ValueError as e:
        print('Invalid count!')
        parser.print_help()
        sys.exit(0)

    debug(f'Host: {host}')
    debug(f'Port: {port}')
    debug(f'count: {count}')

    # Create udp socket
    debug('Creating udp socket...')
    client_socket = socket(AF_INET, SOCK_DGRAM)

    # Start ping
    print(f'PING {host}:{port}')
    statistics = ping(host, port, count)

    # Show statistics
    _show_statistics(host, port, statistics)

