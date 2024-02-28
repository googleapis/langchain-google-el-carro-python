# Copyright 2024 Google LLC
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

import sqlalchemy

from langchain_google_el_carro import ElCarroEngine

db_host = os.environ["DB_HOST"]
db_port = int(os.environ["DB_PORT"])
db_name = os.environ["DB_NAME"]
db_user = os.environ["DB_USER"]
db_password = os.environ["DB_PASSWORD"]
table_name = "message_store"


def test_elcarro_engine_with_basic_auth() -> None:
    elcarro_engine = ElCarroEngine.from_instance(
        db_host,
        db_port,
        db_name,
        db_user,
        db_password,
    )

    # test connection with query
    with elcarro_engine.connect() as conn:
        res = conn.execute(sqlalchemy.text("SELECT 1 FROM DUAL")).fetchone()
        conn.commit()
        assert res[0] == 1  # type: ignore
