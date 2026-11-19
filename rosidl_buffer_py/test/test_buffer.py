# Copyright 2026 StableKite contributors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import subprocess
import sys


def test_shared_buffer_preserves_free_threading() -> None:
    environment = dict(os.environ)
    environment.pop('PYTHON_GIL', None)
    subprocess.run([sys.executable, '-c', '''
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
import sys
import sysconfig

free_threaded = sysconfig.get_config_var('Py_GIL_DISABLED')
if free_threaded:
    assert sys.flags.gil is None and not sys._is_gil_enabled()

from _rosidl_buffer_py import _take_buffer_from_ptr
from _rosidl_buffer_test_support import make_cpu_buffer

buffer = _take_buffer_from_ptr(make_cpu_buffer())
expected = bytes([0, 1, 2, 255])
ready = Barrier(8)

def copy_buffer(_worker):
    ready.wait(timeout=10)
    for _ in range(50):
        assert len(buffer) == len(expected)
        assert buffer.backend_type == 'cpu'
        assert buffer.to_bytes() == expected
        assert buffer.to_array().tobytes() == expected
        assert repr(buffer) == "Buffer(size=4, backend='cpu')"

with ThreadPoolExecutor(max_workers=8) as executor:
    list(executor.map(copy_buffer, range(8)))

if free_threaded:
    assert not sys._is_gil_enabled()
'''], env=environment, check=True)
