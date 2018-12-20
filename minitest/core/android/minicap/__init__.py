#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pathlib import Path

from minitest.config import MINITEST_ROOT

# MINICAP path
MINICAP_PATH = Path.joinpath(MINITEST_ROOT, 'resources/android/minicap')
MINICAP_SHARED_PATH = Path.joinpath(MINICAP_PATH, 'minicap-shared')
