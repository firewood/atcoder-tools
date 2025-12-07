from atcodertools.client.atcoder import ProblemContent
from atcodertools.fmtprediction.predict_simple_format import predict_simple_format, SimpleFormatPredictionFailedError
from atcodertools.fmtprediction.tokenize_format import NoFormatFoundError, \
    search_formats_with_minimum_vars
from atcodertools.fmtprediction.predict_types import predict_types, TypePredictionFailedError
from atcodertools.fmtprediction.models.format_prediction_result import FormatPredictionResult
import re


class NoPredictionResultError(Exception):
    pass


class MultiplePredictionResultsError(Exception):

    def __init__(self, cands):
        self.cands = cands


def suspect_single_string(input_format: list[str], samples):
    # TODO: input_formatの長さが2以上のsingle stringは考えないことにする
    if len(input_format) >= 2:
        return None
    input_format = input_format[0]
    a = input_format.strip().split()
    if len(a) != 1:
        return None
    input_format = a[0].strip()
    for sample in samples:
        s = sample.get_input().split()
        if len(s) != 1:
            return None
    i = input_format.find('_')
    if i == -1:
        return None
    pattern = input_format[0:i + 1]
    if len([m.start() for m in re.finditer(pattern, input_format)]) < 2:
        return None
    return [input_format[0:i]]


def predict_format(content: ProblemContent) -> list[FormatPredictionResult]:
    input_format = content.get_input_format()
    samples = content.get_samples()
    # TODO: primeの置換、ここでいいのか？
    input_format_str_list = list(map(lambda x: x.replace('\'', 'prime'), input_format.input_format))
    if len(samples) == 0:
        raise NoPredictionResultError

    results = []

    # Process each input format separately
    for input_format_str in input_format_str_list:
        # Try to predict format for this individual input format
        found_format = False

        # 1周目(ct = 0)
        # 通常の文字列として実行。見つからなければ二周目へ
        # 2周目(ct = 1)
        # 1文字を疑う
        for ct in [0, 1]:
            tokenized_possible_formats = []
            if ct == 0:
                try:
                    tokenized_possible_formats = search_formats_with_minimum_vars(input_format_str)
                except NoFormatFoundError:
                    continue
            elif ct == 1:
                input_format_str_list2 = suspect_single_string([input_format_str], samples)
                if input_format_str_list2 is not None:
                    try:
                        for suspected_format in input_format_str_list2:
                            tokenized_possible_formats += search_formats_with_minimum_vars(suspected_format)
                    except NoFormatFoundError:
                        continue

            output_cands = []
            # Similar to original predict_format logic
            for tokenized_possible_format in tokenized_possible_formats:
                for to_1d_flag in [False, True]:
                    try:
                        simple_format = predict_simple_format(
                            tokenized_possible_format.var_tokens, to_1d_flag)
                        typed_format = predict_types(simple_format, samples)
                        output_cands.append(
                            FormatPredictionResult.create_typed_format(simple_format, typed_format))
                        break
                    except (TypePredictionFailedError, SimpleFormatPredictionFailedError):
                        pass

            if len(output_cands) > 1:
                raise MultiplePredictionResultsError(output_cands)
            if len(output_cands) == 1:
                results.append(output_cands[0])
                found_format = True
                break

        if not found_format:
            raise NoPredictionResultError

    return results
