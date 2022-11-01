# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.warkdev.axway_cft.plugins.module_utils.axway_utils import parse_fail_message
from ansible_collections.warkdev.axway_cft.plugins.module_utils.common import AxwayModuleError, build_query_str, build_payload
from ansible.module_utils.connection import Connection

import logging

uri = '/cft/api/v1/transfers'

logger = logging.getLogger(__name__)


def fetch_transfer(module, idtu):
    """Retrieves an unique transfer based on identifier

    Returns:
        __type__: _description
    """
    path = '{0}/{1}'.format(uri, idtu)
    logger.debug('Calling path %s', path)
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
    query_str = build_query_str(ida=ida, idtu=idtu, idt=idt, nidt=nidt, part=part, idf=idf,
                                phase=phase, phasestep=phasestep, fields=fields, offset=offset, limit=limit)
    path = '{0}?{1}'.format(uri, query_str)
    logger.debug('Calling path %s', path)
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path)

    if response['code'] != 200:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return response['contents']


def delete_transfer(module, idtu):
    """Deletes a given transfer.

    """
    path = '{0}/{1}'.format(uri, idtu)
    logger.debug('Calling path %s', path)
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path, method='DELETE')

    if response['code'] != 200 and response['code'] != 202:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return {'changed': response['code'] == 200}


def halt_transfer(module, idtu):
    """Interrupts a given transfer.

    """
    path = '{0}/{1}/halt'.format(uri, idtu)
    logger.debug('Calling path %s', path)
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path, method='PUT')

    if response['code'] != 200 and response['code'] != 202:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return {'changed': response['code'] == 200}


def keep_transfer(module, idtu):
    """Suspends a given transfer.

    """
    path = '{0}/{1}/keep'.format(uri, idtu)
    logger.debug('Calling path %s', path)
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path, method='PUT')

    if response['code'] != 200 and response['code'] != 202:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return {'changed': response['code'] == 200}


def start_transfer(module, idtu):
    """Restarts a given transfer.

    """
    path = '{0}/{1}/start'.format(uri, idtu)
    logger.debug('Calling path %s', path)
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path, method='PUT')

    if response['code'] != 200 and response['code'] != 202:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return {'changed': response['code'] == 200}


def resume_transfer(module, idtu):
    """Resumes a given transfer.

    """
    path = '{0}/{1}/resume'.format(uri, idtu)
    logger.debug('Calling path %s', path)
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path, method='PUT')

    if response['code'] != 200 and response['code'] != 202:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return {'changed': response['code'] == 200}


def submit_transfer(module, idtu):
    """Submits a processing procedure for a given transfer

    """
    path = '{0}/{1}/resume'.format(uri, idtu)
    logger.debug('Calling path %s', path)
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path, method='PUT')

    if response['code'] != 200 and response['code'] != 202:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return {'changed': response['code'] == 200}


def ack_transfer(module, idtu, idm, msg):
    """Acknowledges a given transfer.

    """
    query_str = build_query_str(idm=idm)
    payload = build_payload(msg=msg)
    path = '{0}/{1}/ack?{2}'.format(uri, idtu, query_str)
    logger.debug('Calling path %s', path)
    logger.debug('Payload content: %s', payload)
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path, method='PUT', payload=payload)

    if response['code'] != 200 and response['code'] != 202:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return {'changed': response['code'] == 200}


def nack_transfer(module, idtu, idm, msg):
    """Acknowledges negatively a given transfer.

    """
    query_str = build_query_str(idm=idm)
    payload = build_payload(msg=msg)
    path = '{0}/{1}/nack?{2}'.format(uri, idtu, query_str)
    logger.debug('Calling path %s', path)
    logger.debug('Payload content: %s', payload)
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path, method='PUT', payload=payload)

    if response['code'] != 200 and response['code'] != 202:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return {'changed': response['code'] == 200}


def end_transfer(module, idtu):
    """Ends a given transfer.

    """
    path = '{0}/{1}/end'.format(uri, idtu)
    logger.debug('Calling path %s', path)
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path, method='PUT')

    if response['code'] != 200 and response['code'] != 202:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return {'changed': response['code'] == 200}


def create_send_file_transfer_request(module, partner, idf=None, apitimeout=None, ida=None, fname=None, parm=None):
    """Creates a new send file transfer request.

    """
    query_str = build_query_str(part=partner, idf=idf, apitimeout=apitimeout)
    payload = build_payload(ida=ida, fname=fname, parm=parm)
    path = '{0}/files/outgoings?{1}'.format(uri, query_str)
    logger.debug('Calling path %s', path)
    logger.debug('Payload content: %s', payload)
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path, method='POST', payload=payload)

    if response['code'] != 201 and response['code'] != 202:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return {'changed': response['code'] == 201, 'transfer': response['contents']}


def create_receive_file_transfer_request(module, partner, idf=None, apitimeout=None, ida=None, fname=None, parm=None):
    """Creates a new receive file transfer request.

    """
    query_str = build_query_str(part=partner, idf=idf, apitimeout=apitimeout)
    payload = build_payload(ida=ida, fname=fname, parm=parm)
    path = '{0}/files/incomings?{1}'.format(uri, query_str)
    logger.debug('Calling path %s', path)
    logger.debug('Payload content: %s', payload)
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path, method='POST', payload=payload)

    if response['code'] != 201 and response['code'] != 202:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return {'changed': response['code'] == 201, 'transfer': response['contents']}


def create_message_transfer_request(module, partner, idm, msg, apitimeout=None, ida=None):
    """Creates a new message transfer request.

    """
    query_str = build_query_str(part=partner, idm=idm, apitimeout=apitimeout)
    payload = build_payload(ida=ida, msg=msg)
    path = '{0}/messages?{1}'.format(uri, query_str)
    logger.debug('Calling path %s', path)
    logger.debug('Payload content: %s', payload)
    connection = Connection(module._socket_path)
    response = connection.send_request(path=path, method='POST', payload=payload)

    if response['code'] != 201 and response['code'] != 202:
        raise AxwayModuleError(parse_fail_message(response['code'], response['contents']))

    return {'changed': response['code'] == 201, 'transfer': response['contents']}
