# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import logging
import logging.config
import traceback

logger = logging.getLogger(__name__)

MAP_VERBOSITY_TO_LOG_LEVEL = {
    0: 'ERROR',
    1: 'ERROR',
    2: 'INFO',
    3: 'DEBUG',
    4: 'DEBUG',
    5: 'DEBUG'
}


def setup_logging(str_log, verbosity):
    log_level = MAP_VERBOSITY_TO_LOG_LEVEL[verbosity]
    DEFAULT_LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '[%(asctime)s] [PID:%(process)d TID:%(thread)d] [%(levelname)s] [%(name)s] [%(funcName)s():%(lineno)s] %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': log_level,
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': str_log
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': log_level,
                'propagate': True
            }
        }
    }
    logging.config.dictConfig(DEFAULT_LOGGING)


def get_traceback(ex, ex_traceback=None):
    if ex_traceback is None:
        ex_traceback = ex.__traceback__
    tb_lines = [ line.rstrip('\n') for line in traceback.format_exception(ex.__class__, ex, ex_traceback)]
    return '\n'.join(tb_lines)

def parse_fail_message(code, response):
    return 'Axway Transfer CFT returned error {0} with message {1}'.format(code, response)


def update_logging_info(return_value, stdout='', stderr=''):
    return return_value.update({'stdout': stdout, 'stdout_lines': stdout.splitlines(), 'stderr': stderr, 'stderr_lines': stderr.splitlines()})


def create_return_error(msg='', stdout='', stderr=''):
    return {'msg': msg, 'stdout': stdout, 'stdout_lines': stdout.splitlines(), 'stderr': stderr, 'stderr_lines': stderr.splitlines()}


def create_return_object(changed=False, failed=False, rc=0, skipped=False, stderr='', stderr_lines=None, stdout='', stdout_lines=None, warnings=None):
    if not stderr_lines:
        stderr_lines = []
    if not stdout_lines:
        stdout_lines = []
    if not warnings:
        warnings = []

    return {'changed': changed,
            'failed': failed,
            'rc': rc,
            'skipped': skipped,
            'stderr': stderr,
            'stderr_lines': stderr_lines,
            'stdout': stdout,
            'stdout_lines': stdout_lines,
            'warnings': warnings}


def convert_filesystem_to_dict(filesystem):
    ret = {}
    for entry in filesystem:
        if entry['type'] == 'Directory':
            ret[entry['name']] = {}
            if entry['children']:
                ret[entry['name']].update(convert_filesystem_to_dict(entry['children']))
        elif entry['type'] == 'File':
            ret[entry['name']] = entry

    return ret


def identical_files(module, src, dest):  # Compare 2 files based on their checksum.
    if not os.path.isfile(src) or not os.path.isfile(dest):
        return False

    sha_src = module.sha256(src)
    sha_dest = module.sha256(dest)

    return sha_src == sha_dest
