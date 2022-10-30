#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright: (c) 2022, Cédric Servais <cedric.servais@outlook.com>
# GNU General Public License v3.0 (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = r'''
---
module: axway_cft_transfer_info
short_description: Retrieves detailed content about a single transfer.
description:
  - Retrieve transfer corresponding to the provided idtu.
version_added: "1.0.0"
author:
  - Cédric Servais (@7893254)
options:
    idtu:
        description: Transfer ID.
        type: str
        required: true
'''

EXAMPLES = r'''
- name: Gather transfer with idtu T12345678
  axway_cft_transfer_info:
    idtu: T12345678
  register: transfer
'''

RETURN = r'''
transfer:
    description: The transfer corresponding to the matching idtu, none otherwise.
    returned: always
    type: dict
    elements: dict
    sample:
        ack: string
        ackexec: string
        ackmindate: string
        ackmintime: string
        ackstate: string
        acktimeout: string
        appstate: string
        blknum: string
        cftv: string
        chkw: string
        comment: string
        commut: string
        commutrva: string
        compatstate: string
        comprate: string
        cos: string
        counterr: string
        cycdate: string
        cycle: string
        cyctime: string
        dateb: string
        dated: string
        datee: string
        datek: string
        delete: string
        dest: string
        destexec: string
        destexeca: string
        destexecpre: string
        diagc: string
        diagi: string
        diagp: string
        diftyp: string
        direct: string
        dirnb: string
        duplicate: string
        ecar: string
        exec: string
        exece: string
        execinfo: string
        execrall: string
        execsub: string
        execsuba: string
        execsubpre: string
        facc: string
        faction: string
        fblksize: string
        fcar: string
        fcharset: string
        fcode: string
        fcomp: string
        fdate: string
        fdb: string
        fdbcomp: string
        fdelete: string
        fdisp: string
        filenotfound: string
        files: string
        filter: string
        filtertype: string
        filtyp: string
        fkeypos: string
        fkeysize: string
        flowname: string
        flrecl: string
        fname: string
        fnum: string
        forg: string
        fpad: string
        fpath: string
        frec: string
        frecfm: string
        frecfmx: string
        froot: string
        fspace: string
        fspaces: string
        fstate: string
        fsuf: string
        fsyst: string
        ftime: string
        ftname: string
        ftype: string
        funit: string
        fver: string
        group: string
        groupid: string
        ida: string
        idappl: string
        idexit: string
        idexita: string
        idexite: string
        idexiteot: string
        idf: string
        idt: string
        idtu: string
        ipart: string
        iselect: string
        isrelay: string
        jobname: string
        lnum: string
        lpath: string
        lpath_r: string
        lracine: string
        lracine_r: string
        lsuffix: string
        lsuffix_r: string
        lunit: string
        lunit_r: string
        lunitc: string
        lunitc_r: string
        maction: string
        maxdate: string
        maxduration: string
        maxtime: string
        mindate: string
        mintime: string
        mkdir: string
        mode: string
        msg: string
        n_ackprocess: string
        n_ackprocess_err: string
        n_ackprot_pending: string
        n_nackprot_recv: string
        n_postprocess: string
        n_postprocess_err: string
        n_preprocess: string
        n_preprocess_err: string
        nblksize: string
        ncar: string
        ncharset: string
        nchkpt: string
        ncode: string
        ncomp: string
        ndays: string
        ndest: string
        netband: string
        nettyp: string
        nextdate: string
        nexttime: string
        nfname: string
        nfver: string
        nidf: string
        nidt: string
        nkeypos: string
        nkeysize: string
        nlrecl: string
        nodeid: string
        norg: string
        norig: string
        notify: string
        npad: string
        npart: string
        nrec: string
        nrecfm: string
        nrecfmx: string
        nrpart: string
        nrst: string
        nspace: string
        nspart: string
        nsyst: string
        ntf: string
        ntype: string
        opath: string
        opath_r: string
        opermsg: string
        oracine: string
        oracine_r: string
        origin: string
        osuffix: string
        osuffix_r: string
        ounit: string
        ounit_r: string
        ounitc: string
        ounitc_r: string
        pacing: string
        parm: string
        part: string
        phase: string
        phasestep: string
        pidtu: string
        postmindate: string
        postmintime: string
        poststate: string
        posttimeout: string
        preexec: string
        premindate: string
        premintime: string
        prestate: string
        pretimeout: string
        priority: string
        progress: string
        proprf: string
        protnum: string
        protocol: string
        protphase: string
        prottype: string
        prover: string
        rappl: string
        recoverystate: string
        relance: string
        reqgroup: string
        requser: string
        resync: string
        retry: string
        retryc: string
        retrym: string
        retryn: string
        retryp: string
        retryw: string
        ridtu: string
        rkerror: string
        rmsg: string
        rpart: string
        rpasswd: string
        rrename_count: string
        ruser: string
        sappl: string
        savstate: string
        savtypf: string
        selfname: string
        sentinel: string
        serial: string
        sfname: string
        sigfname: string
        sminfnm: string
        sminusr: string
        sourceappl: string
        spart: string
        spasswd: string
        ssl: string
        sslauth: string
        sslciph: string
        sslfnam: string
        sslmode: string
        sslparm: string
        sslprof: string
        sslrmca: string
        sslrmus: string
        ssluser: string
        state: string
        statimpl: string
        storageaccount: string
        suser: string
        targetappl: string
        tcycle: string
        timeb: string
        timed: string
        timee: string
        timek: string
        times: string
        timmaxc: string
        timmc: string
        trkr: string
        typcommut: string
        type: string
        typef: string
        userid: string
        workingdir: string
        wphases: string
        wphasesteps: string
        wstates: string
        wtimeout: string
        xlate: string
'''

import logging
from io import StringIO

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.warkdev.axway_cft.plugins.module_utils.axway_cft_transfers import fetch_transfer

from ansible_collections.warkdev.axway_cft.plugins.module_utils.axway_utils import (
    create_return_object, create_return_error, setup_logging, update_logging_info, get_traceback
)

logger = logging.getLogger(__name__)
str_log = StringIO()
error_log = StringIO()


class ArgumentSpec(object):
    def __init__(self):
        self.supports_check_mode = True
        argument_spec = dict(
            idtu=dict(type='str', required=True)
        )
        self.argument_spec = {}
        self.argument_spec.update(argument_spec)


def __exec_get(module, **kwargs):
    response = fetch_transfer(module=module, **kwargs)
    return response


def exec_module(module):
    response = __exec_get(module=module, **module.params)
    return {'transfer': response}


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
