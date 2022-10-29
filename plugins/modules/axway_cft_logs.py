#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: axway_cft_logs
short_description: Retrieves a list of log messages
description:
  - Get a list of logs messages based on criterias.
version_added: "1.0.0"
author:
  - Cédric Servais (@7893254)
options:
    severity:
        description: Severity of the log to return
        type: str
        choices: ['F', 'E', 'W', 'I']
    limit:
        description: Maximum number of lines to display
        type: int
    date_time_min:
        description: Use to display logs that happened on or after this start date and time YYYY-MM-DDThh:mm:ssZ
        type: str
    date_time_max:
        description: Use to display logs that happened on or before this end date and time YYYY-MM-DDThh:mm:ssZ
        type: str
    pattern:
        description: Only displays the log lines that match this specific pattern; enter any pattern with a maximum of 63 characters
        type: str
    dest:
        description: A filepath where the returned log messages must be dumped; they will be dumped under the form [date] node severity code message
        type: str
    force:
        description: Indicates that the log content must be dumped to the file specified at dest. It has no effect otherwise.
        type: bool
'''

EXAMPLES = r'''
- name: Gather log entries matching Warning state
  axway_cft_logs:
    severity: W

- name: Gather log entries from 01-01-1970 to 30-01-1970
  axway_cft_logs:
    date_time_min: 1970-01-01T00:00:00Z
    date_time_max: 1970-01-30T23:59:59Z

- name: Gather log entries matching the pattern "transfer error"
  axway_cft_logs:
    pattern: ".*transfer error.*"

- name: Gather and dump log messages to file
  axway_cft_logs:
    dest: "/tmp/messages.log"
'''

RETURN = r'''
logs:
    description: A list of log messages corresponding to the matching criteria's
    returned: always
    type: list
    elements: dict
    sample:
        - node: "cftnode"
          severity: "W"
          code: "99"
          date: "1970-01-01T00:00:00Z"
          message: "This is a log message"
'''

import logging
import os
import os.path
import tempfile
from io import StringIO

from ansible.module_utils._text import to_bytes
from ansible.module_utils.basic import AnsibleModule

from ansible_collections.community.axway_cft.plugins.module_utils.axway_cft_logs import fetch_logs

from ansible_collections.community.axway_cft.plugins.module_utils.axway_utils import (
    create_return_object, create_return_error, setup_logging, update_logging_info, get_traceback
)

from ansible_collections.community.axway_cft.plugins.module_utils.common import (
    validate_arg_pattern
)

logger = logging.getLogger(__name__)
str_log = StringIO()
error_log = StringIO()


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        argument_spec = dict(
            severity=dict(type='str', choices=['F', 'E', 'W', 'I']),
            limit=dict(type='int'),
            date_time_min=dict(type='str'),
            date_time_max=dict(type='str'),
            pattern=dict(type='str'),
            dest=dict(type='str'),
            force=dict(type='bool')
        )
        self.argument_spec = {}
        self.argument_spec.update(argument_spec)


def __exec_get(module, **kwargs):
    response = fetch_logs(module=module, **kwargs)
    return response


def exec_module(module):
    force = module.params.pop('force')
    dest = module.params.pop('dest')

    for arg in ['date_time_min', 'date_time_max']:
        if arg in module.params and module.params[arg]:
            validate_arg_pattern(name=arg, value=module.params[arg], pattern=r'^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$')

    for arg in ['pattern']:
        if arg in module.params and module.params[arg]:
            validate_arg_pattern(name=arg, value=module.params[arg], pattern=r'^[a-zA-Z]{1,5}$')

    if dest:  # This means we need to copy logs to file
        b_dest = to_bytes(dest, errors='surrogate_or_strict')
        response = __exec_get(module=module, **module.params)

        dummy, b_mydest = tempfile.mkstemp(dir=os.path.dirname(b_dest))

        with open(b_mydest, mode='wb') as f_dest:
            for record in response['logs']:
                f_dest.write(str.encode('[{0}] {1} {2} {3} {4}{5}'.format(record['date'], record['node'], record['severity'], record['code'], record['message'], os.linesep)))

        checksum_dest = module.sha1(b_mydest)

        if os.path.isfile(b_dest):
            checksum_src = module.sha1(b_dest)
        else:
            checksum_src = None

        if force or checksum_dest != checksum_src:
            if not module.check_mode:
                module.atomic_move(src=b_mydest, dest=b_dest)

            return {'changed': True}
        else:
            return {}

    else:
        response = __exec_get(module=module, **module.params)
        return {'logs': response['logs']}


def main():
    spec = ArgumentSpec()
    module = AnsibleModule(
        argument_spec=spec.argument_spec,
        supports_check_mode=spec.supports_check_mode
    )
    try:
        setup_logging(str_log, module._verbosity)
        logger.debug('Module parameters %s', module.params)

        response = exec_module(module)
        return_value = create_return_object()
        update_logging_info(return_value, str_log.getvalue(), error_log.getvalue())
        return_value.update(response)

        module.exit_json(**return_value)
    except Exception as e:
        error_log.write(get_traceback(e))
        return_value = create_return_error(msg=str(e), stdout=str_log.getvalue(), stderr=error_log.getvalue())
        module.fail_json(**return_value)


if __name__ == '__main__':
    main()
