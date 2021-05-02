from atcodertools.common.logging import logger


def load_text_file(text_file: str) -> str:
    for encoding in ['utf8', 'utf-8_sig', 'cp932']:
        try:
            with open(text_file, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            logger.warning("text wasn't recognized as {}".format(encoding))
    return None
