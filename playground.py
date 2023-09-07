#!/usr/bin/python3

import os
import sys
import shutil
import argparse
from pathlib import PosixPath
from python_on_whales import DockerClient

def resolve_path() -> str:
    """
    Resolve playground path
    """
    path = os.path.normpath(os.getcwd()).split(os.sep)
    path[0] = '/'
    for i in range(len(path), 0, -1):
        cpath = os.path.join(*path[:i])
        if ".playground" in os.listdir(cpath):
            break
    if cpath == '/':
        print("Playground config not found! Run \"playground init\" at the root of your project to create example configuration.")
        exit(1)
    return os.path.join(cpath, '.playground')
        
    
def init() -> None:
    """
    Initialize playground
    """
    if not os.path.exists('./.playground'):
        shutil.copytree("/etc/playground/examples", "./.playground")

def start() -> None:
    """
    Start playground
    """
    path = resolve_path()    
    docker = DockerClient(compose_files=[os.path.join(path, 'docker-compose.yml')])
    docker.compose.build()
    docker.compose.up(detach=True)

def stop() -> None:
    """
    Stop playground
    """
    path = resolve_path()    
    docker = DockerClient(compose_files=[os.path.join(path, 'docker-compose.yml')])
    docker.compose.down()


def build(output: str = './bin') -> None:
    """
    Build project using Playground Build System (PBS)
    """
    path = resolve_path()
    docker = DockerClient()
    logs = docker.build(path, file=os.path.join(path, 'build.Dockerfile'), output={"type": "local", "dest": os.path.abspath(os.path.join(os.getcwd(), output))}, stream_logs=True)
    for log in logs:
        print(log)

def shell(command: str = "/bin/bash", mountpoint: str = "/src") -> None:
    """
    Get a shell into a working PBS development environment
    """
    mount_path = str(PosixPath(resolve_path()).parent.absolute())
    path = resolve_path()
    docker = DockerClient()
    image = docker.build(path, file=os.path.join(path, 'build.Dockerfile'), target="build-stage")
    docker.run(image, [command], mounts=[(mount_path, mountpoint)])


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='target')
    start_parser = subparsers.add_parser('start', help='Starts the playground environment.')
    stop_parser = subparsers.add_parser('stop', help='Stops the playground environment.')
    init_parser = subparsers.add_parser('init', help='Initializes the playground environment.')
    build_parser = subparsers.add_parser('build', help='Builds the project using the playground build system (PBS).')
    build_parser.add_argument('--output', type=str, help='Specifies the output location of built binaries.')
    shell_parser = subparsers.add_parser('shell', help='Obtain a shell into a working PBS development environment.')
    shell_parser.add_argument('--command', type=str, help='Command to run in the container.')
    shell_parser.add_argument('--mountpoint', type=str, help='Specify mount point of source code in container.')
    args = parser.parse_args(sys.argv[1:])
    match args.target:
        case "start":
            start()
        case "stop":
            stop()
        case "init":
            init()
        case "build":
            if args.output:
                build(output=args.output)
            else:
                build()
        case "shell":
            if not args.command or args.mountpoint:
                shell()
            else:
                if args.command and args.mountpoint:
                    shell(command=args.command, mountpoint=args.mountpoint)
                elif args.command:
                    shell(command=args.command)
                else:
                    shell(mountpoint=args.mountpoint)
                
if __name__ == "__main__":
    main()
