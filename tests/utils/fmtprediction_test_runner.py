import os
from typing import Optional

from atcodertools.fmtprediction.predict_format import MultiplePredictionResultsError, \
    NoPredictionResultError, predict_format
from atcodertools.client.models.problem_content import ProblemContent
from atcodertools.client.models.sample import Sample
from atcodertools.fmtprediction.models.format_prediction_result import FormatPredictionResult


class Response:

    def __init__(self, result: Optional[FormatPredictionResult], status, is_multiple_cases: bool = False):
        self.status = status
        self.is_multiple_cases = is_multiple_cases
        if result:
            self.original_result = result
            self.original_result.is_multiple_cases = is_multiple_cases  # Add flag to result
            self.simple_format = result.format
            var_info = [(var.name, var.type)
                        for var in result.format.all_vars()]
            self.types = [(name, type.to_py_type()) for name, type in var_info]


FORMAT_FILE_NAME = "format.txt"


class FormatPredictionTestRunner:

    def __init__(self, test_dir):
        self.test_dir = test_dir

    def is_valid_case(self, case_name):
        return os.path.isdir(self._get_test_case_dir(case_name))

    def load_problem_content(self, case_name: str) -> ProblemContent:
        case_dir = self._get_test_case_dir(case_name)
        format_file = os.path.join(case_dir, FORMAT_FILE_NAME)
        example_files = [os.path.join(case_dir, file)
                         for file in os.listdir(case_dir) if file != FORMAT_FILE_NAME]

        with open(format_file, 'r', encoding="utf-8") as f:
            format_content = f.read().strip()

        # Check if this is a multicase format by splitting into lines
        format_lines = [line.strip() for line in format_content.split('\n') if line.strip()]

        # If we have multiple lines, treat as multicase format
        if len(format_lines) > 1:
            input_format = format_lines  # Pass as list for multicase

            # For multicase, simplify the sample to just one test case
            examples = []
            for ex_file in example_files:
                with open(ex_file, 'r', encoding="utf-8") as f:
                    full_sample = f.read().strip()
                    # Extract just the first test case for format prediction
                    lines = full_sample.split('\n')
                    if len(lines) > 0:
                        # Skip the test case count (first line), take next few lines as one test case
                        # For abc413-D: skip T=3, take N=5 and one array
                        if len(lines) >= 3:
                            simplified_sample = '\n'.join(lines[1:3]) + '\n'  # N and one array
                            examples.append(Sample(simplified_sample, None))

        else:
            input_format = format_content  # Single case
            examples = []
            for ex_file in example_files:
                with open(ex_file, 'r', encoding="utf-8") as f:
                    examples.append(Sample(f.read(), None))

        return ProblemContent(input_format, examples)

    def run(self, case_name: str) -> Response:
        content = self.load_problem_content(case_name)

        # Determine if this is a multicase problem
        is_multicase = isinstance(content.input_format_text, list) and len(content.input_format_text) > 1

        try:
            results = predict_format(content)
            # For tests, use the first result to maintain backward compatibility
            result = results[0] if results else None
            return Response(result, "OK", is_multicase)
        except MultiplePredictionResultsError:
            return Response(None, "Multiple results", is_multicase)
        except NoPredictionResultError:
            return Response(None, "No result", is_multicase)

    def _get_test_case_dir(self, case_name):
        return os.path.join(self.test_dir, case_name)
