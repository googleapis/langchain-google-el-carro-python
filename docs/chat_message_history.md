# El Carro Oracle Operator

>
Google [El Carro Oracle Operator](https://github.com/GoogleCloudPlatform/elcarro-oracle-operator)
offers a way to run Oracle databases in Kubernetes as a portable, open source,
community driven, no vendor lock-in container orchestration system. El Carro
provides a powerful declarative API for comprehensive and consistent
configuration and deployment as well as for real-time operations and
monitoring...
Extend your database application to build AI-powered experiences leveraging
Oracle Langchain integrations.

This guide goes over how to use the El Carro Langchain integration to store chat
message
history with the `ElCarroMessageHistory` class.

## Before You Begin

Please complete
the [Getting Started](https://github.com/googleapis/langchain-google-el-carro-python/tree/main/README.md#getting-started)
section of
the README to set up your El Carro Oracle database.

### 🦜🔗 Library Installation

The integration lives in its own `langchain-google-el-carro-python` package, so
we need to install it.

```bash
pip install --upgrade --quiet langchain-google-el-carro-python
```

## Basic Usage

### Set Up Oracle Database Connection

ElCarroEngine configures a connection pool to your Oracle database,
enabling successful connections from your application and following industry
best practices.

You can find the hostname and port values in the status of the El Carro
Kubernetes instance.
Use the user password you created for your PDB.

```python
from langchain_google_el_carro import ElCarroEngine

elcarro_engine = ElCarroEngine.from_instance(
    db_host="127.0.0.1",
    db_port=3307,
    db_name="PDB1",
    db_user="scott",
    db_password="tiger",
)
```

### Initialize a table

The `ElCarroChatMessageHistory` class requires a database table with a specific
schema in order to store the chat message history.

The `ElCarroEngine` class has a
method `init_chat_history_table()` that can be used to create a table with the
proper schema for you.

```python
elcarro_engine.init_chat_history_table(table_name=TABLE_NAME)
```

### ElCarroChatMessageHistory

To initialize the `ElCarroChatMessageHistory` class you need to provide only 3
things:

1. `elcarro_engine` - An instance of an `ElCarroEngine` engine.
1. `session_id` - A unique identifier string that specifies an id for the
   session.
1. `table_name` : The name of the table within the Oracle database to store the
   chat message history.

```python
from langchain_google_el_carro import ElCarroChatMessageHistory

history = ElCarroChatMessageHistory(
    elcarro_engine=elcarro_engine, session_id="test_session", table_name=TABLE_NAME
)
history.add_user_message("hi!")
history.add_ai_message("whats up?")
```

### Cleaning up

When the history of a specific session is obsolete and can be deleted, it can be
done the following way.

**Note:** Once deleted, the data is no longer stored in the Oracle database and
is gone forever.

```python
history.clear()
```

## Full example

Please look
at [chat_history.py](https://github.com/googleapis/langchain-google-el-carro-python/tree/main/samples/demo_chat_history.py)
for a complete
code example.

 


