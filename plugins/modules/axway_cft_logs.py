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
extends_documentation_fragment:
  - community.axway_cft.logging_info_options
'''

EXAMPLES = r'''
- name: Gathering log entries matching Warning state
  axway_cft_logs:
    severity: W

- name: Gathering log entries from 01-01-1970 to 30-01-1970
  axway_cft_logs:
    date_time_min: 1970-01-01T00:00:00Z
    date_time_max: 1970-01-30T23:59:59Z

- name: Gathering log entries matching the pattern "transfer error"
  axway_cft_logs:
    pattern: ".*transfer error.*"
'''

RETURN = r'''
logs:
  description: A list of log messages corresponding to the matching criteria's
  returned: always
  type: list
  contains:
    node:
      description: The CFT node
      type: str
      sample: "cftnode"
    severity:
      description: Message severity
      type: str
      sample: "W"
    code:
      description: Message code
      type: str
      sample: "99"
    date:
      description: Message date
      type: str
      sample: "1970-01-01T00:00:00Z
    message:
      description: The log message
      type str
      sample: "This is a log message"
'''

import logging
from io import StringIO

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.community.axway_cft.plugins.module_utils.axway_cft_logs import fetch_logs

from ansible_collections.community.axway_cft.plugins.module_utils.axway_utils import (
    create_return_object, create_return_error, setup_logging, update_logging_info, get_traceback
)

from ansible_collections.community.axway_cft.plugins.module_utils.common import (
    validate_arg_pattern, logging_argument_spec
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
          pattern=dict(type='str')
        )
        self.argument_spec = {}
        self.argument_spec.update(argument_spec)
        self.argument_spec.update(logging_argument_spec())


def __exec_get(module, **kwargs):
    response = fetch_logs(module=module, **kwargs)
    return response


def exec_module(module):
    for arg in ['date_time_min', 'date_time_max']:
      if arg in module.params:
        validate_arg_pattern(name=arg, value=module.params[arg], pattern=r'^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$')

    for arg in ['pattern']:
      if arg in module.params:
        validate_arg_pattern(name=arg, value=module.params[arg], pattern=r'^[a-zA-Z]{1,5}$')

    response = __exec_get(module=module, **module.params)

    return_value = create_return_object()

    return return_value.update({'logs': response['logs']})


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
