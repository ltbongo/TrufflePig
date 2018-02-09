import pytest

import pandas as pd
from steem import Steem
from steem.blockchain import Blockchain

from trufflepig import config
import trufflepig.bchain.getdata as tpbg

@pytest.fixture
def steem():
    return Steem(nodes=[config.NODE_URL])


@pytest.fixture
def bchain(steem):
    return Blockchain(steem)


def test_get_headers(steem, bchain):
    offset = bchain.get_current_block_num()
    now = pd.datetime.utcnow()
    minutes_ago = now - pd.Timedelta(minutes=3)
    headers = tpbg.get_block_headers_between_offset_start(minutes_ago, now, offset, steem)
    assert headers


def test_get_headers_bchain(steem):
    target = pd.datetime.utcnow() - pd.Timedelta(days=3)
    minutes_ago = target - pd.Timedelta(minutes=3)
    headers = tpbg.get_block_headers_between(minutes_ago, target, steem)
    assert headers


def test_find_offset(steem, bchain):
    now = pd.datetime.utcnow()
    target = now - pd.Timedelta(days=42)
    offset, datetime = tpbg.find_nearest_block_num(target, steem, bchain)
    assert 0 < offset <  bchain.get_current_block_num()
