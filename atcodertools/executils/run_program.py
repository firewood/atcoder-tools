import subprocess
import time
from enum import Enum
import threading
from typing import Optional

from atcodertools.common.judgetype import Judge, MultiSolutionJudge, InteractiveJudge, DecimalJudge, \
    NormalJudge
import tempfile

from atcodertools.common.language import Language


class ExecStatus(Enum):
    NORMAL = "NORMAL"
    TLE = "TLE"
    RE = "RE"
    JUDGE_ERROR = "JUDGE_ERROR"


class JudgeStatus(Enum):
    AC = "AC"
    WA = "WA"


class UnknownJudgeError(Exception):
    pass


class JudgeError(Exception):
    def __init__(self, stdout: str = "", stderr: str = ""):
        self.stdout = stdout
        self.stderr = stderr


class ExecResult:
    def __init__(
            self,
            status: ExecStatus, output: str = None,
            stderr: str = None,
            elapsed_sec: float = None,
            special_judge_status: JudgeStatus = None,
            judge_message: str = None
    ):
        self.status = status
        self.output = output
        self.stderr = stderr
        self.special_judge_status = special_judge_status
        self.judge_message = judge_message

        if elapsed_sec is not None:
            self.elapsed_ms = int(elapsed_sec * 1000 + 0.5)
        else:
            self.elapsed_ms = None

    def is_correct_output(
            self,
            expected_answer_text: Optional[str] = None,
            judge_method: Optional[Judge] = None,
            sample_input_file: Optional[str] = None,
            sample_output_file: Optional[str] = None,
            cwd: Optional[str] = None,
            judge_program_language: Optional[Language] = None
    ):
        if self.status != ExecStatus.NORMAL:
            return False

        if self.special_judge_status is not None:
            return self.special_judge_status == JudgeStatus.AC

        if isinstance(judge_method, MultiSolutionJudge):
            judge_exec_res = run_multisolution_judge_program(
                judge_program_language.get_test_command('judge', cwd),
                self.output,
                sample_input_file,
                sample_output_file
            )
            self.judge_message = judge_exec_res.stderr
            return judge_exec_res.special_judge_status == JudgeStatus.AC
        elif isinstance(judge_method, InteractiveJudge):
            raise UnknownJudgeError("No judge status error for interactive!!")
        elif isinstance(judge_method, DecimalJudge):
            return judge_method.verify(self.output, expected_answer_text)
        elif isinstance(judge_method, NormalJudge):
            return judge_method.verify(self.output, expected_answer_text)
        else:
            raise NotImplementedError

    def has_stderr(self):
        if self.stderr is None:
            return False
        return len(self.stderr) > 0


def run_program(exec_file: str, input_file: str, timeout_sec: float, args=None, current_working_dir: str = None) -> ExecResult:
    if args is None:
        args = []
    try:
        elapsed_sec = -time.time()
        proc = subprocess.run(
            exec_file.split(" ") + args, stdin=open(input_file, 'r'), universal_newlines=True, timeout=timeout_sec,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=current_working_dir
        )

        if proc.returncode == 0:
            code = ExecStatus.NORMAL
        else:
            code = ExecStatus.RE

        elapsed_sec += time.time()
        return ExecResult(code, proc.stdout, proc.stderr, elapsed_sec=elapsed_sec)
    except subprocess.TimeoutExpired as e:
        return ExecResult(ExecStatus.TLE, e.stdout or "", e.stderr or "")
    except subprocess.CalledProcessError as e:
        return ExecResult(ExecStatus.RE, e.stdout, e.stderr)
    except JudgeError as e:
        return ExecResult(ExecStatus.JUDGE_ERROR, e.stdout, e.stderr)
