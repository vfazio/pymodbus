"""Test client async."""
import asyncio
import logging

import pytest_asyncio

from pymodbus import pymodbus_apply_logging_config
from pymodbus.client import AsyncModbusTcpClient
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusServerContext,
    ModbusSlaveContext,
)
from pymodbus.server import ServerAsyncStop, StartAsyncUnixServer
from pymodbus.transaction import ModbusSocketFramer


_logger = logging.getLogger()
_logger.setLevel("DEBUG")
pymodbus_apply_logging_config(logging.DEBUG)
PATH = "/tmp/unix_domain_socket"  # nosec
HOST = f"unix:{PATH}"


@pytest_asyncio.fixture(name="_mock_run_server")
async def _helper_server():
    """Run server."""
    datablock = ModbusSequentialDataBlock(0x00, [17] * 100)
    context = ModbusSlaveContext(
        di=datablock, co=datablock, hr=datablock, ir=datablock, unit=1
    )
    asyncio.create_task(
        StartAsyncUnixServer(
            context=ModbusServerContext(slaves=context, single=True),
            path=PATH,
            framer=ModbusSocketFramer,
        )
    )
    await asyncio.sleep(0.1)
    yield
    await ServerAsyncStop()



async def test_unix_server(_mock_run_server):
    """Run async server with unit domain socket."""
    await asyncio.sleep(0.1)


async def test_unix_async_client(_mock_run_server):
    """Run async client with unit domain socket."""
    await asyncio.sleep(0.1)
    client = AsyncModbusTcpClient(
        HOST,
        framer=ModbusSocketFramer,
    )
    await client.connect()
    assert client.connected

    rr = await client.read_coils(1, 1, slave=1)
    assert not rr.isError()
