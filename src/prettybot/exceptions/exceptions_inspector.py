import inspect


def get_traceback(stack, exception: Exception = 'Undefinded') -> str:
    return 'ERROR: {} in file: [{}] func: [{}] line: [{}]'.format(
        exception, stack[0].filename, stack[0].function, stack[0].lineno
    )
