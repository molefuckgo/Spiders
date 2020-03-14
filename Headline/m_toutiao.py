# !/usr/bin/env python
# coding=utf-8
"""
@File: m_toutiao.py
@Time: 2020-02-26 01:12
@Desc:
"""

from pathlib import Path
from typing import Dict
import execjs

toutiao_dir = Path(__file__).absolute().parent
with open(toutiao_dir/'_get_as_cp_signature.js') as f:
    ctx = execjs.compile(f.read())


def get_as_cp_signature(user_agent: str, behot_time: int = 0) -> Dict[str, str]:
    params = {
        'page_type' : 1,
        'count' : 20,
        '_siganture': '',
        'as': '',
        'cp': ''
    }

    key = "min_behot_time" if not behot_time else "max_behot_time"
    params[key] = behot_time
    _as_cp = ctx.call('get_as_cp')
    params.update(_as_cp)
    _signature = ctx.call('get_signature', behot_time, user_agent)
    params['_siganture'] = _signature
    return params