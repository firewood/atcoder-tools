import subprocess
import locale


def run_command(exec_cmd: str, current_working_dir: str) -> str:
    proc = subprocess.run(exec_cmd,
                          shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,
                          cwd=current_working_dir)
<<<<<<< HEAD
    return proc.stdout.decode("utf8")


def run_command_with_returncode(exec_cmd: str, current_working_dir: str) -> str:
=======
    return proc.stdout.decode(locale.getpreferredencoding())


def run_command_with_returncode(exec_cmd: str, current_working_dir: str):
>>>>>>> test_fmtprediction
    proc = subprocess.run(exec_cmd,
                          shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,
                          cwd=current_working_dir)
<<<<<<< HEAD
    return proc.returncode, proc.stdout.decode("utf8")
=======
    return proc.returncode, proc.stdout.decode(locale.getpreferredencoding())
>>>>>>> test_fmtprediction
