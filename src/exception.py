import sys
import os, logging

""""
sys :
module provides functions and variables used to manipulate different parts of 
the Python runtime environment. It lets you interact directly with the interpreter 
and the host operating system.

OS:
os module lets your Python script talk directly to the host operating system.
"""


def error_message_detail(error, error_detail: sys):

    _, _, exc_tb = error_detail.exc_info()

    if exc_tb is not None:
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
    else:
        file_name = "Unknown"
        line_number = "Unknown"

    error_message = (
        "Error occurred in Python script name [{0}] "
        "line number [{1}] error message [{2}]"
    ).format(file_name, line_number, str(error))

    return error_message


class CustomException(Exception):

    def __init__(self, error_message, error_detail: sys):

        super().__init__(error_message)

        self.error_message = error_message_detail(
            error=error_message,
            error_detail=error_detail
        )

    def __str__(self):
        return self.error_message


# if __name__ == "__main__":

#     try:
#         a = 10 / 0

#     except Exception as e:
#         logging.error("An error occurred")
#         raise CustomException(e, sys) from e
