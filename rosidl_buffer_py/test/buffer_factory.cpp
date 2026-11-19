// Copyright 2026 StableKite contributors.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#include <pybind11/pybind11.h>

#include <cstdint>

#include "rosidl_buffer/buffer.hpp"

namespace py = pybind11;

#ifdef Py_GIL_DISABLED
PYBIND11_MODULE(_rosidl_buffer_test_support, m, py::mod_gil_not_used())
#else
PYBIND11_MODULE(_rosidl_buffer_test_support, m)
#endif
{
  m.def("make_cpu_buffer", []() {
      return reinterpret_cast<uintptr_t>(new rosidl::Buffer<uint8_t>({0, 1, 2, 255}));
    });
}
