import pytest
import os
import shutil
import tempfile

import pandas as pd
from pandas.testing import assert_frame_equal
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


@pytest.fixture
def temp_dir(tmpdir_factory):
    return tmpdir_factory.mktemp('test', numbered=True)


def test_get_headers(steem, bchain):
    offset = bchain.get_current_block_num()
    now = pd.datetime.utcnow()
    minutes_ago = now - pd.Timedelta(minutes=3)
    headers = tpbg.get_block_headers_between_offset_start(minutes_ago, now, offset, steem)
    assert headers


def test_get_headers2(steem):
    target = pd.datetime.utcnow() - pd.Timedelta(days=3)
    minutes_ago = target - pd.Timedelta(minutes=3)
    headers = tpbg.get_block_headers_between(minutes_ago, target, steem)
    assert headers


def test_find_offset(steem, bchain):
    now = pd.datetime.utcnow()
    target = now - pd.Timedelta(days=42)
    latest_block_num = bchain.get_current_block_num()
    offset, datetime = tpbg.find_nearest_block_num(target, steem, latest_block_num)
    assert 0 < offset <  latest_block_num


def test_get_all_posts_between(steem):
    now = pd.datetime.utcnow()
    end = now
    start = end - pd.Timedelta(minutes=10)
    posts = tpbg.get_all_posts_between(start, end, steem, stop_after=25)
    assert posts


def test_scrape_date(steem, temp_dir):
    yesterday = (pd.datetime.utcnow() - pd.Timedelta(days=1)).date()

    p1 = tpbg.scrape_or_load_full_day(yesterday, steem, temp_dir, stop_after=25)

    assert len(os.listdir(temp_dir)) == 1

    p2 = tpbg.scrape_or_load_full_day(yesterday, steem, temp_dir, stop_after=25)

    assert len(os.listdir(temp_dir)) == 1

    assert_frame_equal(p1, p2)
    assert len(p1) > 0


def test_scrape_or_load_data_parallel(temp_dir):
    frames = tpbg.scrape_or_load_training_data_parallel([config.NODE_URL],
                                                       temp_dir,
                                                       days=5,
                                                       stop_after=10,
                                                       ncores=5)
    assert len(frames) == 5