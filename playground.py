#!/usr/bin/python3

import os
import shutil
from pathlib import PosixPath
from python_on_whales import DockerClient

def resolve_path() -> None:
    """
    Resolve playground path
    """
    paths = [os.getcwd()]
    path = os.getcwd()
    while True:
        if (cpath :=PosixPath(path).parent) in paths:
            break
        paths.append(str(cpath.absolute()))
    

    for path in paths:
        if '.playground' in os.listdir(path):
            break

    if path == '/':
        print('No playground config found. Run "playground init" in your project root to initialize playground.')
        exit(1)
    
    return os.path.join(path, '.playground')

def init() -> None:
    """
    Initialize playground
    """
    if not os.path.exists('./.playground'):
        os.mkdir("./.playground")
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


def build_project() -> None:
    """
    Build project using Playground Build System (PBS)
    """
    path = resolve_path()
    docker = DockerClient()
    logs = docker.build(path, file=os.path.join(path, 'build.Dockerfile'), output={"type": "local", "dest": os.path.abspath(os.path.join(os.getcwd(), "bin"))}, stream_logs=True)
    for log in logs:
        print(log)

def shell() -> None:
    """
    Get a shell into a working PBS development environment
    """
    mount_path = str(PosixPath(resolve_path()).parent.absolute())
    path = resolve_path()
    docker = DockerClient()
    image = docker.build(path, file=os.path.join(path, 'build.Dockerfile'), target="build-stage")
    docker.run(image, ["/bin/bash"], mounts=[(mount_path, "/src")])



