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

from langchain_core.documents import Document

from langchain_google_el_carro import ElCarroDocumentSaver, ElCarroEngine, ElCarroLoader

db_host = os.environ["DB_HOST"]
db_port = int(os.environ["DB_PORT"])
db_name = os.environ["DB_NAME"]
db_user = os.environ["DB_USER"]
db_password = os.environ["DB_PASSWORD"]

elcarro_engine = ElCarroEngine.from_instance(
    db_host,
    db_port,
    db_name,
    db_user,
    db_password,
)

table_name = "my_doc_table"

elcarro_engine.init_document_table(
    table_name=table_name,
)

doc = Document(
    page_content="Banana",
    metadata={"type": "fruit", "weight": 100, "organic": 1},
)

print(f"Original Document = [{doc}]")

saver = ElCarroDocumentSaver(
    elcarro_engine=elcarro_engine,
    table_name=table_name,
)
saver.add_documents([doc])

loader = ElCarroLoader(
    elcarro_engine=elcarro_engine,
    table_name=table_name,
)

loaded_docs = loader.load()
print(f"Loaded Document = [{loaded_docs[0]}]")

elcarro_engine.drop_document_table(table_name=table_name)
