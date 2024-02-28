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

import json
from typing import List

import sqlalchemy
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, messages_from_dict
from sqlalchemy.dialects import oracle

from .engine import ElCarroEngine


class ElCarroChatMessageHistory(BaseChatMessageHistory):
    """Chat message history stored in an ElCarro-Oracle database.

    Args:
        elcarro_engine (ElCarroEngine):
            ElCarroEngine connection object.
        session_id (str):
            Arbitrary key that is used to store the messages
            of a single chat session.
        table_name (str):
            The name of the table to use for storing/retrieving
            the chat message history.
    """

    def __init__(
        self,
        elcarro_engine: ElCarroEngine,
        session_id: str,
        table_name: str,
    ) -> None:
        self.elcarro_engine = elcarro_engine
        self.session_id = session_id
        self.table_name = table_name

        # Verify that the table exists and has a correct schema
        self.elcarro_engine.verify_chat_history_table_schema(table_name)

        # Cache database metadata
        meta_data = sqlalchemy.MetaData()
        sqlalchemy.MetaData.reflect(meta_data, bind=self.elcarro_engine.connect())
        self.s_table = meta_data.tables[self.table_name]

    @property
    def messages(self) -> List[BaseMessage]:  # type: ignore
        """Retrieve the messages from database"""

        stmt = (
            sqlalchemy.select(self.s_table.c.data, self.s_table.c.type)
            .where(self.s_table.c.session_id == self.session_id)
            .order_by(self.s_table.c.id.asc())
        )

        with self.elcarro_engine.connect() as conn:
            results = conn.execute(stmt).fetchall()
            print(results)
            # load SQLAlchemy row objects into dicts
            items = [
                {"data": json.loads(result[0]), "type": result[1]} for result in results
            ]
            messages = messages_from_dict(items)
            return messages

    def add_message(self, message: BaseMessage) -> None:
        """Append the message to the record in the database"""
        stmt = sqlalchemy.insert(self.s_table).values(
            session_id=self.session_id,
            data=json.dumps(message.dict(), sort_keys=True),
            type=message.type,
        )

        with self.elcarro_engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()

    def clear(self) -> None:
        """Clear session memory from the database"""

        stmt = sqlalchemy.delete(self.s_table).where(
            self.s_table.c.session_id == self.session_id
        )
        with self.elcarro_engine.connect() as conn:
            conn.execute(stmt)
            conn.commit()
