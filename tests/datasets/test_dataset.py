# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from __future__ import annotations

import os

import pytest

from airflow.datasets import Dataset
from airflow.operators.empty import EmptyOperator


@pytest.mark.parametrize(
    ["uri"],
    [
        pytest.param("", id="empty"),
        pytest.param("\n\t", id="whitespace"),
        pytest.param("a" * 3001, id="too_long"),
        pytest.param("airflow:" * 3001, id="reserved_scheme"),
        pytest.param("😊" * 3001, id="non-ascii"),
    ],
)
def test_invalid_uris(uri):
    with pytest.raises(ValueError):
        Dataset(uri=uri)


def test_uri_with_scheme():
    dataset = Dataset(uri="s3://example_dataset")
    EmptyOperator(task_id="task1", outlets=[dataset])


def test_uri_without_scheme():
    dataset = Dataset(uri="example_dataset")
    EmptyOperator(task_id="task1", outlets=[dataset])


def test_fspath():
    uri = "s3://example_dataset"
    dataset = Dataset(uri=uri)
    assert os.fspath(dataset) == uri