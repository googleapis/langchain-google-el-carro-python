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

from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage

from langchain_google_el_carro import ElCarroEngine
from langchain_google_el_carro.chat_message_history import ElCarroChatMessageHistory

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

# Create a new table
elcarro_engine.init_chat_history_table("my_table")

# Create ElCarroChatMessageHistory
history = ElCarroChatMessageHistory(
    elcarro_engine=elcarro_engine, session_id="test_session", table_name="my_table"
)

# Add a few messages
history.add_user_message("hi!")
history.add_ai_message("whats up?")
messages = history.messages

print(f"Messages = {messages}")

# verify messages are correct
assert messages[0].content == "hi!"
assert type(messages[0]) is HumanMessage
assert messages[1].content == "whats up?"
assert type(messages[1]) is AIMessage

history.clear()
assert len(history.messages) == 0

# Drop the table
elcarro_engine.drop_chat_history_table("my_table")
