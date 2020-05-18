import logging


def noop(*args, **kwargs):
    sample_variable = kwargs['sample_variable']

    logging.info(sample_variable)