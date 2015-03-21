import logging
import uuid as _uuid


def _get_logger():
    _logger = logging.getLogger("iu")
    _logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s: %(message)s'
    ))
    _logger.addHandler(ch)
    return _logger


def uuid():
    return str(_uuid.uuid4())


logger = _get_logger()
