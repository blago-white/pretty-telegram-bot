import inspect


def get_traceback(exception: Exception, stack) -> str:
    return 'ERROR: {} in file: [{}] func: [{}] line: [{}]'.format(
        exception or 'Undefinded', stack[0].filename, stack[0].function, stack[0].lineno
    )
