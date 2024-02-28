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
from __future__ import annotations

import copy
from typing import List, Optional

import sqlalchemy
import sqlalchemy.dialects.oracle

DEFAULT_CONTENT_COL = "page_content"
DEFAULT_METADATA_COL = "langchain_metadata"


class ElCarroEngine:
    def __init__(
        self,
        engine: sqlalchemy.engine.Engine,
    ) -> None:
        self._engine = engine

    @classmethod
    def from_instance(
        cls,
        db_host: str,
        db_port: int,
        db_name: str,
        db_user: str,
        db_password: str,
        thick_mode=False,
    ) -> ElCarroEngine:
        """Create an instance of ElCarroEngine from El Carro instance details

        Args:
            db_host (str): Host of the Oracle Database endpoint
            db_port (int): Host of the Oracle Database endpoint
            db_name (str): The name of the PDB to connect to.
            db_user (str): Database user to use for basic database
                authentication and login.
            db_password (str): Database password to use for basic database
                authentication and login.
            thick_mode(bool): Use thick mode (require installed Oracle drivers).

            Returns:
                (ElCarroEngine): The engine configured to connect to an
                Oracle instance database.
        """
        url_object = sqlalchemy.URL.create(
            "oracle+oracledb",
            username=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            query=dict(service_name=db_name),
        )
        if thick_mode:
            engine = sqlalchemy.create_engine(
                url_object, thick_mode={"driver_name": "ElCarro"}
            )
        else:
            engine = sqlalchemy.create_engine(url_object)
        # Test connectivity
        engine.connect()
        return cls(engine=engine)

    def connect(self) -> sqlalchemy.engine.Connection:
        """Create a connection from an SQLAlchemy connection pool.

        Returns:
            (sqlalchemy.engine.Connection): a single DBAPI connection checked
                out from the connection pool.
        """
        return self._engine.connect()

    def init_chat_history_table(self, table_name: str) -> None:
        """Create an Oracle table with schema required for ElCarroChatMessageHistory class.

        Required schema is as follows:

            CREATE TABLE {table_name} (
              id NUMBER GENERATED BY DEFAULT AS IDENTITY (START WITH 1),
              session_id VARCHAR2(128) NOT NULL,
              data CLOB NOT NULL CONSTRAINT ensure_json_{table_name} CHECK (data IS JSON),
              type VARCHAR2(128) NOT NULL,
              PRIMARY KEY (id)
            )

        Args:
            table_name (str): Name of database table to create for storing chat
                message history.
        """

        with self.connect() as conn:
            table_exists = sqlalchemy.inspect(conn).has_table(table_name)
            if not table_exists:
                columns: List[sqlalchemy.Column] = [
                    sqlalchemy.Column(
                        "id",
                        sqlalchemy.Integer,
                        sqlalchemy.Identity(start=1),
                        primary_key=True,
                    ),
                    sqlalchemy.Column(
                        "session_id",
                        sqlalchemy.dialects.oracle.VARCHAR2(128),
                        nullable=False,
                    ),
                    sqlalchemy.Column(
                        "data",
                        sqlalchemy.dialects.oracle.CLOB,
                        nullable=False,
                    ),
                    sqlalchemy.Column(
                        "type",
                        sqlalchemy.dialects.oracle.VARCHAR2(128),
                        nullable=False,
                    ),
                ]
                table = sqlalchemy.Table(table_name, sqlalchemy.MetaData(), *columns)
                table.append_constraint(sqlalchemy.CheckConstraint(f"data is json"))
                table.create(conn)

    def drop_chat_history_table(self, table_name: str) -> None:
        """Delete chat history table.

        Args:
            table_name (str): Name of database table for storing chat
                message history.
        """

        meta_data = sqlalchemy.MetaData()
        sqlalchemy.MetaData.reflect(meta_data, bind=self.connect())
        table = meta_data.tables.get(table_name)
        if table is not None:
            meta_data.drop_all(self.connect(), [table], checkfirst=True)

    def verify_chat_history_table_schema(self, table_name: str) -> None:
        """Verify table exists with required schema for
            ElCarroChatMessageHistory class.

        Use helper method init_chat_history_table(...) to create
        a table with a valid schema.

        Args:
            table_name (str): Name of database table for storing chat
                message history.
        """
        insp = sqlalchemy.inspect(self.connect())
        # check table exists
        if insp.has_table(table_name):
            # check that all required columns are present
            required_columns = ["id", "session_id", "data", "type"]
            column_names = [c["name"] for c in insp.get_columns(table_name=table_name)]
            if not (all(x in column_names for x in required_columns)):
                raise IndexError(
                    f"Table '{table_name}' has incorrect schema. Got "
                    f"column names '{column_names}' but required column names "
                    f"'{required_columns}'.\n"
                    f"See init_chat_history_table() for a helper method."
                )
        else:
            raise AttributeError(
                f"Table '{table_name}' does not exist. Please create "
                "it before initializing ElCarroChatMessageHistory. See "
                "init_chat_history_table() for a helper method."
            )

    def init_document_table(
        self,
        table_name: str,
        metadata_columns: List[sqlalchemy.Column] = [],
        content_column: str = DEFAULT_CONTENT_COL,
        metadata_json_column: Optional[str] = DEFAULT_METADATA_COL,
    ) -> None:
        """
        Create a table for saving of langchain documents.

        Args:
            table_name (str): The database table name.
            metadata_columns (List[sqlalchemy.Column]): A list of sqlalchemy.Columns
                to create for custom metadata. Optional.
            content_column (str): The column to store document content.
                Default: `page_content` with datatype VARCHAR2(4000).
            metadata_json_column (Optional[str]): The column to store extra
                metadata in JSON format.
                Default: `langchain_metadata` with datatype VARCHAR2(4000),
                    set to None to disable
        """
        with self.connect() as conn:
            table_exists = sqlalchemy.inspect(conn).has_table(table_name)
            if not table_exists:
                columns = [
                    sqlalchemy.Column(
                        content_column, sqlalchemy.dialects.oracle.VARCHAR2(4000)
                    )
                ]
                for mc in metadata_columns:
                    columns.append(copy.deepcopy(mc))
                if metadata_json_column:
                    columns.append(
                        sqlalchemy.Column(
                            metadata_json_column,
                            sqlalchemy.dialects.oracle.VARCHAR2(4000),
                        )
                    )
                table = sqlalchemy.Table(table_name, sqlalchemy.MetaData(), *columns)
                if metadata_json_column:
                    table.append_constraint(
                        sqlalchemy.CheckConstraint(f"{metadata_json_column} is json")
                    )
                table.create(conn)

    def drop_document_table(self, table_name: str):
        """Delete table for langchain documents.

        Args:
            table_name (str): Name of database table for langchain documents.
        """

        meta_data = sqlalchemy.MetaData()
        sqlalchemy.MetaData.reflect(meta_data, bind=self.connect())
        table = meta_data.tables.get(table_name)
        if table is not None:
            meta_data.drop_all(self.connect(), [table], checkfirst=True)
