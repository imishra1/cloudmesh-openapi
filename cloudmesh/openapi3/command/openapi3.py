from __future__ import print_function

from pathlib import Path, PureWindowsPath
import sys
from importlib import import_module

from cloudmesh.common.console import Console
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import path_expand
from cloudmesh.openapi3.function import generator
import sys, pathlib
from importlib import import_module
# added by Ishan
from cloudmesh.common.Shell import Shell
import os
from cloudmesh.openapi3.function.server import Server
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command, map_parameters
from cloudmesh.openapi3.registry.Registry import Registry

class Openapi3Command(PluginCommand):

    # noinspection PyUnusedLocal,PyPep8Naming
    @command
    def do_openapi3(self, args, arguments):
        """
        ::

          Usage:
              openapi3 generate FUNCTION [YAML]
                                         --baseurl=BASEURL
                                         --filename=FILENAME
                                         --yamldirectory=DIRECTORY
                                         [--verbose]
              openapi3 server start YAML
                              NAME
                              [--directory=DIRECTORY]
                              [--port=PORT]
                              [--server=SERVER]
                              [--verbose]
              openapi3 server stop NAME
              openapi3 server list [NAME] [--output=OUTPUT]
              openapi3 register add NAME ENDPOINT
              openapi3 register remove NAME
              openapi3 register list [NAME] [--output=OUTPUT]
              openapi3 tbd
              openapi3 tbd merge [SERVICES...] [--dir=DIR] [--verbose]
              openapi3 tdb list [--dir=DIR]
              openapi3 tbd description [SERVICES...] [--dir=DIR]
              openapi3 tbd md FILE [--indent=INDENT]
              openapi3 tbd codegen [SERVICES...] [--srcdir=SRCDIR]
                              [--destdir=DESTDIR]

          Arguments:
              DIR   The directory of the specifications
              FILE  The specification

          Options:
              --verbose              specifies to run in debug mode [default: False]
              --port=PORT            the port for the server [default: 8080]
              --directory=DIRECTORY  the directory in which the server is run [default: ./]
              --server=SERVER        the server [default: flask]
              --output=OUTPUT        the outputformat, table, csv, yaml, json [default: table]
              --srcdir=SRCDIR   The directory of the specifications
              --destdir=DESTDIR  The directory where the generated code should be put

          Description:
            This command does some useful things.


        """

        map_parameters(arguments,
                       'output',
                       'verbose',
                       'port',
                       'directory',
                       'yamldirectory',
                       'baseurl',
                       'filename',
                       'name')
        arguments.debug = arguments.verbose

        # VERBOSE(arguments)

        if arguments.generate:

            try:
                function = arguments.FUNCTION
                yamlfile = arguments.YAML
                baseurl = path_expand(arguments.baseurl)
                filename = arguments.filename.strip().split(".")[0]
                yamldirectory = path_expand(arguments.yamldirectory)

                sys.path.append(baseurl)

                module_name = pathlib.Path(f"{filename}").stem

                imported_module = import_module(module_name)

                func_obj = getattr(imported_module, function)

                setattr(sys.modules[module_name], function, func_obj)

                openAPI = generator.Generator()

                # BUG: theis is windows specific and must be done differently

                rc = openAPI.generate_openapi(func_obj,
                                              baseurl.split("\\")[-1],
                                              yamldirectory, yamlfile)
                if rc != 0:
                    Console.error("Failed to generate openapi yaml")
                    raise Exception
            except Exception as e:
                print(e)


        elif arguments.server and arguments.start:

            try:
                #
                # BUG: this is completely wrong as i it is not portable
                #
                print("directory: ",
                      Path(PureWindowsPath(path_expand(arguments.directory))))
                s = Server(
                    spec=arguments.YAML,
                    directory=path_expand(arguments.directory),
                    port=arguments.port,
                    server=arguments.wsgi,
                    debug=arguments.debug,
                    name=arguments.NAME)

                s._run()

                VERBOSE(arguments, label="Server parameters")


            except FileNotFoundError:

                Console.error("specification file not found")


            except Exception as e:

                print(e)


        elif arguments.server and arguments.stop:
            """

            name = arguments.NAME


            try:

                get_pid = os.popen("ps -ef|grep {name}|grep -v grep|awk '{print $2}'")

                pid = get_pid.read()


            except FileNotFoundError:


                Console.error("specification file not found")


            except Exception as e:

                print(e)

            """
            try:
                Server.shutdown(self, name=arguments.NAME)
            except ConnectionError:
                Console.Error("Server not running")


        elif arguments.register and arguments.add:

            raise NotImplementedError

        elif arguments.register and arguments.remove:

            raise NotImplementedError

        elif arguments.register and arguments.list:

            registry = Registry()
            result = registry.list()

            registry.Print(data=result, output=arguments.output)



        '''

        arguments.wsgi = arguments["--server"]

        m = Manager(debug=arguments.debug)

        arguments.dir = path_expand(arguments["--dir"] or ".")

        # pprint(arguments)

        if arguments.list:
            files = m.get(arguments.dir)
            print("List of specifications")
            print(79 * "=")
            print('\n'.join(files))

        elif arguments.merge:
            d = m.merge(arguments.dir, arguments.SERVICES)
            print(yaml.dump(d, default_flow_style=False))

        elif arguments.description:
            d = m.description(arguments.dir, arguments.SERVICES)

        elif arguments.md:

            converter = OpenAPIMarkdown()

            if arguments["--indent"] is None:
                indent = 1
            else:
                indent = int(arguments["--indent"])
            filename = arguments["FILE"]

            converter.title(filename, indent=indent)
            converter.convert_definitions(filename, indent=indent + 1)
            converter.convert_paths(filename, indent=indent + 1)
        elif arguments.codegen:
            m.codegen(arguments.SERVICES, arguments.dir)

        
        elif arguments.server and arguments.stop:

            print("implement me")

        return ""
        '''
