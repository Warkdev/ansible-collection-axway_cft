# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.community.axway_cft.plugins.module_utils.axway_utils import parse_fail_message
from ansible_collections.community.axway_cft.plugins.module_utils.common import AxwayModuleError, build_query_str, build_payload
from ansible.module_utils.connection import Connection

import logging

uri = '/transfers'

logger = logging.getLogger(__name__)


def fetch_transfer(module, idtu):
    """Retrieves an unique transfer based on identifier

    Returns:
        __type__: _description
    """
    path='{}/{}'.format(uri, idtu)
    logger.debug('Calling path {}'.format(path))
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path)

    if response['code'] != 200:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']


def fetch_transfers(module, ida=None, idtu=None, idt=None, nidt=None, part=None, idf=None, phase=None, phasestep=None, fields=None, offset=0, limit=0):
    """ Retrieves a list of transfers

    Returns:
        _type_: _description_
    """
    query_str = build_query_str(ida=ida, idtu=idtu, idt=idt, nidt=nidt, part=part, idf=idf, phase=phase, phasestep=phasestep, fields=fields, offset=offset, limit=limit)
    path = '{}?{}'.format(uri, query_str)
    logger.debug('Calling path {}'.format(path))
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path)

    if response['code'] != 200:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']


def delete_transfer(module, idtu):
    """Deletes a given transfer.

    """
    path='{}/{}'.format(uri, idtu)
    logger.debug('Calling path {}'.format(path))
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path, method='DELETE')

    if response['code'] != 200:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']


def halt_transfer(module, idtu):
    """Interrupts a given transfer.

    """
    path='{}/{}/halt'.format(uri, idtu)
    logger.debug('Calling path {}'.format(path))
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path, method='PUT')

    if response['code'] != 200:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']


def keep_transfer(module, idtu):
    """Suspends a given transfer.

    """
    path='{}/{}/keep'.format(uri, idtu)
    logger.debug('Calling path {}'.format(path))
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path, method='PUT')

    if response['code'] != 200:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']


def start_transfer(module, idtu):
    """Restarts a given transfer.

    """
    path='{}/{}/start'.format(uri, idtu)
    logger.debug('Calling path {}'.format(path))
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path, method='PUT')

    if response['code'] != 200:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']


def resume_transfer(module, idtu):
    """Resumes a given transfer.

    """
    path='{}/{}/resume'.format(uri, idtu)
    logger.debug('Calling path {}'.format(path))
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path, method='PUT')

    if response['code'] != 200:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']


def submit_transfer(module, idtu):
    """Submits a processing procedure for a given transfer

    """
    path='{}/{}/resume'.format(uri, idtu)
    logger.debug('Calling path {}'.format(path))
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path, method='PUT')

    if response['code'] != 200:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']


def ack_transfer(module, idtu):
    """Acknowledges a given transfer.

    """
    path='{}/{}/ack'.format(uri, idtu)
    logger.debug('Calling path {}'.format(path))
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path, method='PUT')

    if response['code'] != 200:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']


def nack_transfer(module, idtu):
    """Acknowledges negatively a given transfer.

    """
    path='{}/{}/nack'.format(uri, idtu)
    logger.debug('Calling path {}'.format(path))
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path, method='PUT')

    if response['code'] != 200:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']


def end_transfer(module, idtu):
    """Ends a given transfer.

    """
    path='{}/{}/end'.format(uri, idtu)
    logger.debug('Calling path {}'.format(path))
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path, method='PUT')

    if response['code'] != 200:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']


def create_send_file_transfer_request(module, partner, idf=None, apitimeout=None, ida=None, fname=None, parm=None):
    """Creates a new send file transfer request.

    """
    query_str = build_query_str(part=partner, idf=idf, apitimeout=apitimeout)
    payload = build_payload(ida=ida, fname=fname, parm=parm)
    path='{}/files/outgoings'.format(uri)
    logger.debug('Calling path {}'.format(path))
    logger.debug('Payload content: {}'.format(payload))
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path, method='POST', payload=payload)

    if response['code'] != 201:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']


def create_receive_file_transfer_request(module, partner, idf=None, apitimeout=None, ida=None, fname=None, parm=None):
    """Creates a new receive file transfer request.

    """
    query_str = build_query_str(part=partner, idf=idf, apitimeout=apitimeout)
    payload = build_payload(ida=ida, fname=fname, parm=parm)
    path='{}/files/incomings'.format(uri)
    logger.debug('Calling path {}'.format(path))
    logger.debug('Payload content: {}'.format(payload))
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path, method='POST', payload=payload)

    if response['code'] != 201:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']


def create_message_transfer_request(module, partner, idm, msg, apitimeout=None, ida=None):
    """Creates a new message transfer request.

    """
    query_str = build_query_str(part=partner, idm=idm, apitimeout=apitimeout)
    payload = build_payload(ida=ida, msg=msg)
    path='{}/messages'.format(uri)
    logger.debug('Calling path {}'.format(path))
    logger.debug('Payload content: {}'.format(payload))
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path, method='POST', payload=payload)

    if response['code'] != 201:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']