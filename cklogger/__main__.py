#!/usr/bin/env python3
import base64
import dataclasses
import datetime
import logging
import pprint

import click
import coloredlogs
from bpylist2 import archiver
from bpylist2.archive_types import DataclassArchiver
from pymobiledevice3.lockdown import LockdownClient
from pymobiledevice3.services.os_trace import OsTraceService

coloredlogs.install(level=logging.DEBUG)

logger = logging.getLogger(__name__)

MAX_PACKET = 0x7c00


@dataclasses.dataclass
class NSURL(DataclassArchiver):
    NSbase: str
    NSrelative: str


@dataclasses.dataclass
class CKDTrafficMetadata(DataclassArchiver):
    p: bool
    t: datetime.datetime
    u: NSURL
    m: str
    s: int
    h: dict
    r: str

    @property
    def parsingStandaloneMessage(self):
        return self.p

    @property
    def timestamp(self):
        return self.t

    @property
    def url(self):
        return self.u

    @property
    def method(self):
        return self.m

    @property
    def status(self):
        return self.s

    @property
    def headers(self):
        return self.h

    @property
    def requestClassName(self):
        return self.r


archiver.update_class_map({
    'NSURL': NSURL,
    'CKDTrafficMetadata': CKDTrafficMetadata,
})


def handle_logRequest_toURL_withMethod_withMessageClassString_parsingStandaloneMessage_(metadata: str, payload: bytes):
    request_id = metadata[1:-4]
    sequence_number = metadata[-4:]

    print(f'📱➡️ ☁️  {request_id} {sequence_number}')
    pprint.pprint(archiver.unarchive(payload))


def handle_logPartialRequestObjectData_(metadata: str, payload: bytes):
    print('📱➡️ ☁️')
    print(payload)


def handle_logResponse_(metadata: str, payload: bytes):
    request_id = metadata[1:-4]
    sequence_number = metadata[-4:]

    print(f'📱⬅️️ ☁️  {request_id} {sequence_number}')
    pprint.pprint(archiver.unarchive(payload))


def handle_logResponseConfiguration_withMessageClassString_(metadata: str, payload: bytes):
    """ type '4' """
    payload = archiver.unarchive(payload)
    response_configuration, message_class_string = payload.split(':')
    logger.debug(f'{response_configuration=} {message_class_string=}')


def handle_logPartialResponseObjectData_(metadata: str, payload: bytes):
    print('📱⬅️️ ☁️')
    print(payload)


def handle_finishRequestLog_(metadata: str, payload: bytes):
    pass


@click.command()
def cli():
    lockdown = LockdownClient()

    for entry in OsTraceService(lockdown).syslog():
        if entry.label is None or entry.label.subsystem != 'com.apple.cloudkit' or \
                entry.label.category != 'TrafficBinary':
            continue

        metadata, payload = entry.message.split(':')
        type_ = metadata[0]
        payload = base64.b64decode(payload.encode())

        handlers = {
            '1': handle_logRequest_toURL_withMethod_withMessageClassString_parsingStandaloneMessage_,
            '3': handle_logPartialRequestObjectData_,
            '2': handle_logResponse_,
            '4': handle_logResponseConfiguration_withMessageClassString_,
            '5': handle_logPartialResponseObjectData_,
            '6': handle_finishRequestLog_,
        }

        handlers[type_](metadata, payload)


if __name__ == '__main__':
    cli()
