#!/usr/bin/python3
import argparse
import os
import shutil
import re
from atcodertools.config.config import Config
from atcodertools.tools.envgen import get_config, USER_CONFIG_PATH
from atcodertools.tools import get_default_config_path
from atcodertools.common.language import ALL_LANGUAGES, CPP
from atcodertools.common.logging import logger
from atcodertools.codegen.code_style_config import DEFAULT_WORKSPACE_DIR_PATH
from atcodertools.codegen.template_engine import render
from atcodertools.tools.models.metadata import Metadata
from atcodertools.executils.run_command import run_command


def copy_to_repository(dir: str, metadata: Metadata, config: Config):
    contest_id = metadata.problem.contest.contest_id
    problem_id = metadata.problem.alphabet
    filename = metadata.code_filename
    result = re.match('(.*[^\d])(\d+)', contest_id)
    if result is None:
        logger.error(with_color("Failed", Fore.RED))
        return
    contest_id = '{}_{}'.format(result.group(1), result.group(2))
    target_dir = os.path.join(config.code_style_config.workspace_dir, '..', 'atcoder', contest_id)
    os.makedirs(target_dir, exist_ok=True)
    source_path = os.path.join(dir, filename)
    target_path = os.path.join(target_dir, filename)
    shutil.copy(source_path, target_path)
    run_command('git add {}'.format(filename), target_dir)
    logger.info("From: {}, To: {}".format(source_path, target_path))


def main(prog, args):
    parser = argparse.ArgumentParser(
        prog=prog,
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--config",
                        help="File path to your config file\n{0}{1}".format("[Default (Primary)] {}\n".format(
                            USER_CONFIG_PATH),
                            "[Default (Secondary)] {}\n".format(
                                get_default_config_path()))
                        )
    parser.add_argument("--template",
                        help="File path to your template code\n{}".format(
                            "\n".join(
                                ["[Default ({dname})] {path}".format(
                                    dname=lang.display_name,
                                    path=lang.default_template_path
                                ) for lang in ALL_LANGUAGES]
                            ))
                        )
    parser.add_argument("--workspace",
                        help="Path to workspace's root directory. This script will create files"
                             " in {{WORKSPACE}}/{{contest_name}}/{{alphabet}}/ e.g. ./your-workspace/arc001/A/\n"
                             "[Default] {}".format(DEFAULT_WORKSPACE_DIR_PATH))
    parser.add_argument("--lang",
                        help="Programming language of your template code, {}.\n"
                        .format(" or ".join([lang.name for lang in ALL_LANGUAGES])) + "[Default] {}".format(CPP.name))
    parser.add_argument("--without-login",
                        action="store_true",
                        help="Download data without login")
    parser.add_argument("--parallel",
                        action="store_true",
                        help="Prepare problem directories asynchronously using multi processors.",
                        default=None)
    parser.add_argument("--save-no-session-cache",
                        action="store_true",
                        help="Save no session cache to avoid security risk",
                        default=None)
    parser.add_argument("--dir", '-d',
                        help="Target directory to test. [Default] Current directory",
                        default=".")
    args = parser.parse_args(args)
    config = get_config(args)

    metadata_file = os.path.join(args.dir, "metadata.json")
    try:
        metadata = Metadata.load_from(metadata_file)
    except IOError:
        logger.error(
            "{0} is not found! You need {0} to use this submission functionality.".format(metadata_file))
        return False

    copy_to_repository(args.dir, metadata, config)


if __name__ == "__main__":
    main(sys.argv[0], sys.argv[1:])
