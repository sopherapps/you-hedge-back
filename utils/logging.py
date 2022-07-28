"""Module containing the utility functions for logging"""

import gzip
import itertools
import logging
import os
import shutil
import sys
from logging.handlers import RotatingFileHandler

from flask import has_request_context, request


class RequestFormatter(logging.Formatter):
    """Formatter injects in safe details connected to the request"""

    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)


class RotatingGzipFileHandler(RotatingFileHandler):
    """
    This rotating file handler class compresses past logs and saves them
    in ascending order whereby .1 is the first back up and say .2 is after .1
    Courtesy of https://stackoverflow.com/questions/40150821/in-the-logging-modules-rotatingfilehandler-how-to-set-the-backupcount-to-a-pra#answer-53288524
    """

    def doRollover(self):
        """Method to create the next log, and save the last log"""
        if self.stream:
            self.stream.close()
            self.stream = None

        # start of override
        for i in itertools.count(1):
            next_log_name = f"{self.baseFilename}.{i}.gz"

            if not os.path.exists(next_log_name):
                with open(self.baseFilename, 'rb') as original_log:
                    # gzip old log with a number at its end
                    with gzip.open(next_log_name, 'wb') as gzipped_log:
                        shutil.copyfileobj(original_log, gzipped_log)

                os.remove(self.baseFilename)
                break

        # end of override
        if not self.delay:
            self.stream = self._open()


def setup_rotating_file_logger(
        logger: logging.Logger,
        file_path: str,
        level: int,
        max_bytes: int = 2000000):
    """
    Makes the logger to use a file that rotates when a given size is reached.
    It has a single back up and logs errors and above
    """
    handler = RotatingGzipFileHandler(file_path, maxBytes=max_bytes)
    handler.setLevel(level)
    request_formatter = RequestFormatter(
        '%(asctime)-15s %(remote_addr)s requested %(url)s\n'
        '%(levelname)s:\n%(message)s\n\n'
    )
    handler.setFormatter(request_formatter)
    logger.addHandler(handler)
    return logger


def setup_stderr_logger(logger: logging.Logger, level: int):
    """Sets up the given logger to log to standard output"""
    handler = logging.StreamHandler(sys.stderr, )
    handler.terminator = '\r'
    handler.setLevel(level)
    log_formatter = logging.Formatter('[%(name)s]%(levelname)s: %(message)s')
    handler.setFormatter(log_formatter)
    logger.addHandler(handler)
    return logger


def initialize_logger(
        name: str,
        should_log_to_file: bool = True,
        level: int = logging.ERROR) -> logging.Logger:
    """Initializes the appropriate logger"""
    logger = logging.getLogger(name)

    if should_log_to_file:
        logs_folder_path = os.path.join(os.getcwd(), 'logs')
        log_file_path = os.path.join(logs_folder_path, f'{name}.log')
        os.makedirs(logs_folder_path, exist_ok=True)
        return setup_rotating_file_logger(file_path=log_file_path, logger=logger, level=level)

    return setup_stderr_logger(logger=logger, level=level)
