#!/usr/bin/python3
import argparse
<<<<<<< HEAD

from atcodertools.common.judgetype import MultiSolutionJudge, InteractiveJudge
from atcodertools.executils.run_command import run_command_with_returncode
from atcodertools.tools.models.metadata import Metadata
import os
import pathlib
=======
from os.path import expanduser

from atcodertools.executils.run_command import run_command_with_returncode
from atcodertools.tools.models.metadata import Metadata
from atcodertools.common.language import Language
import os
import pathlib
from atcodertools.config.config import Config, ConfigType
from atcodertools.tools import get_default_config_path

USER_CONFIG_PATH = os.path.join(expanduser("~"), ".atcodertools.toml")
>>>>>>> test_fmtprediction


class BadStatusCodeException(Exception):
    pass


<<<<<<< HEAD
def _compile(code_filename: str, exec_filename: str, compile_cmd: str, cwd: str, force_compile: bool) -> None:
=======
def _compile(code_filename: str, exec_filename: str, compile_command: str, cwd: str, force_compile: bool) -> None:
>>>>>>> test_fmtprediction
    if not force_compile:
        code_path = pathlib.Path(os.path.join(cwd, code_filename))
        exec_path_name = os.path.join(cwd, exec_filename)

        if os.path.exists(exec_path_name) and code_path.stat().st_mtime < pathlib.Path(exec_path_name).stat().st_mtime:
            print("No need to compile")
            return

<<<<<<< HEAD
    print("Compiling... (command: `{}`)".format(compile_cmd))
    code, stdout = run_command_with_returncode(compile_cmd, cwd)
=======
    print("Compiling... (command: `{}`)".format(compile_command))
    code, stdout = run_command_with_returncode(compile_command, cwd)
>>>>>>> test_fmtprediction
    print(stdout)
    if code != 0:
        raise BadStatusCodeException


<<<<<<< HEAD
def compile_main_and_judge_programs(metadata: Metadata, cwd="./", force_compile=False) -> None:
    lang = metadata.lang
    print("[Main Program]")
    compile_cmd = lang.get_compile_command('main')
=======
def compile_main_and_judge_programs(lang: Language, cwd="./", force_compile=False, compile_command=None) -> None:
    print("[Main Program]")
    if compile_command is None:
        compile_command = lang.get_compile_command('main')
    print("compile command: ", compile_command)
>>>>>>> test_fmtprediction
    code_filename = lang.get_code_filename('main')
    exec_filename = lang.get_exec_filename('main')

    try:
<<<<<<< HEAD
        _compile(code_filename, exec_filename, compile_cmd, cwd, force_compile)
    except BadStatusCodeException as e:
        raise e

    if isinstance(metadata.judge_method, MultiSolutionJudge) or isinstance(metadata.judge_method, InteractiveJudge):
        print("[Judge Program]")
        # TODO: Use judge_lang instead of lang
        compile_cmd = lang.get_compile_command('judge')
        code_filename = lang.get_code_filename('judge')
        exec_filename = lang.get_exec_filename('judge')

        try:
            _compile(code_filename, exec_filename,
                     compile_cmd, cwd, force_compile)
        except BadStatusCodeException as e:
            raise e

=======
        _compile(code_filename, exec_filename,
                 compile_command, cwd, force_compile)
    except BadStatusCodeException as e:
        raise e

>>>>>>> test_fmtprediction

def main(prog, args):
    parser = argparse.ArgumentParser(
        prog=prog,
        usage="Compile your program in the current directory (no argument)",
        formatter_class=argparse.RawTextHelpFormatter)
<<<<<<< HEAD
    parser.parse_args(args)

    metadata = Metadata.load_from("./metadata.json")
    compile_main_and_judge_programs(metadata, force_compile=True)
=======
    parser.add_argument('--compile-command',
                        help='set compile command'
                             ' [Default]: None',
                        type=str,
                        default=None)

    parser.add_argument('--compile-only-when-diff-detected',
                        help='compile only when diff detected [true, false]'
                             ' [Default]: false',
                        type=bool,
                        default=None)

    parser.add_argument("--config",
                        help="File path to your config file\n{0}{1}".format("[Default (Primary)] {}\n".format(
                            USER_CONFIG_PATH),
                            "[Default (Secondary)] {}\n".format(
                                get_default_config_path())),
                        default=None)

    args = parser.parse_args(args)
    if args.config is None:
        if os.path.exists(USER_CONFIG_PATH):
            args.config = USER_CONFIG_PATH
        else:
            args.config = get_default_config_path()

    metadata = Metadata.load_from("./metadata.json")
    lang = metadata.lang

    with open(args.config, "r") as f:
        config = Config.load(f, {ConfigType.COMPILER}, args, lang.name)

    if args.compile_only_when_diff_detected:
        force_compile = not args.compile_only_when_diff_detected
    else:
        force_compile = not config.compiler_config.compile_only_when_diff_detected

    if args.compile_command:
        compile_command = args.compile_command
    else:
        compile_command = config.compiler_config.compile_command
    if compile_command:
        compile_command = lang.get_compile_command("main", compile_command)
    compile_main_and_judge_programs(metadata.lang, force_compile=force_compile,
                                    compile_command=compile_command)
>>>>>>> test_fmtprediction
