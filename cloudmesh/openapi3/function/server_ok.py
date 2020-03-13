from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from cloudmesh.common.debug import VERBOSE
import sys
import connexion
from importlib import import_module
import os
from platform import platform
from cloudmesh.common.Shell import Shell
import subprocess

import os, time

def daemon(func):
    def wrapper(*args, **kwargs):
        pid = os.fork()
        if pid != 0:
            print ("PID", pid)
        if pid: return
        r = func(*args, **kwargs)
        os._exit(os.EX_OK)
    return wrapper

def dynamic_import(abs_module_path, class_name):
    module_object = import_module(abs_module_path)
    target_class = getattr(module_object, class_name)
    return target_class

class Server(object):

    def __init__(self,
                 name=None,
                 spec=None,
                 directory=None,
                 host="127.0.0.1",
                 server="flask",
                 port=8080,
                 debug=True):
        if spec is None:
            Console.error("No service specification file defined")
            raise FileNotFoundError


        self.spec = path_expand(spec)

        if directory is None:
            self.directory = os.path.dirname(self.spec)
        else:
            self.directory = directory

        print (name)
        if name is None:
            self.name = os.path.basename(self.spec).replace(".yaml", "")

        self.host = host
        self.port = port
        self.debug = debug
        self.server = server or "flask"
        self.server_command = ""

        data = dict(self.__dict__)
        #data['import'] = __name__

        VERBOSE(data, label="Server parameters")

        if server == "tornado":
            try:
                import tornado
            except Exception as e:
                print(e)
                Console.error(
                    "tornado not install. Please use `pip install tornado`")
                sys.exit(1)
                return ""
            if self.debug:
                Console.error("Tornado does not support --verbose")
                sys.exit(1)
                return ""

        Console.ok(self.directory)

    @daemon
    def _run(self):
        Console.ok("starting server")

        sys.path.append(self.directory)
        app = connexion.App(__name__,
                            specification_dir=self.directory)

        # ### app.add_cls(self.directory)
        app.add_api(self.spec)
        r = app.run(host=self.host,
                    port=self.port,
                    debug=self.debug,
                    server=self.server)
    """
    def stop(self, name=None):
        ps = Shell.ps().splitlines()
        ps = Shell.find_lines_with(ps, "openapi3 server gstart")
        for p in ps:
            pid, rest = p.split(" ", 1)
            info = p.split("start")[1].split("--")[0].strip()
            print(f"{pid}: {info}")
    """

    def ps(self, name=None):
        ps = Shell.ps().splitlines()
        ps = Shell.find_lines_with(ps, "openapi3 server gstart")
        for p in ps:
            pid, rest = p.split(" ", 1)
            info = p.split("start")[1].split("--")[0].strip()
            print (f"{pid}: {info}")

