# El Carro Oracle Operator

>
Google [El Carro Oracle Operator](https://github.com/GoogleCloudPlatform/elcarro-oracle-operator)
offers a way to run Oracle databases in Kubernetes as a portable, open source,
community driven, no vendor lock-in container orchestration system. El Carro
provides a powerful declarative API for comprehensive and consistent
configuration and deployment as well as for real-time operations and
monitoring..
Extend your database application to build AI-powered experiences leveraging
Oracle Langchain integrations.

This guide goes over how to use El Carro Langchain integration to
[save, load and delete langchain documents](https://python.langchain.com/docs/modules/data_connection/document_loaders/)
with `ElCarroLoader` and `ElCarroDocumentSaver`.

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

Initialize a table of default schema
via `elcarro_engine.init_document_table(<table_name>)`. Table Columns:

- page_content (type: text)
- langchain_metadata (type: JSON)

```python

elcarro_engine.init_document_table(
    table_name=TABLE_NAME,
)
```

### Save documents

Save langchain documents with `ElCarroDocumentSaver.add_documents(<documents>)`.
To initialize `ElCarroDocumentSaver` class you need to provide 2 things:

1. `elcarro_engine` - An instance of a `ElCarroEngine` engine.
2. `table_name` - The name of the table within the Oracle database to store
   langchain documents.

```python
from langchain_google_el_carro import ElCarroDocumentSaver
from langchain_core.documents import Document

doc = Document(
    page_content="Banana",
    metadata={"type": "fruit", "weight": 100, "organic": 1},
)

saver = ElCarroDocumentSaver(
    elcarro_engine=elcarro_engine,
    table_name=table_name,
)
saver.add_documents([doc])
```

### Load documents

Load langchain documents with `ElCarroLoader.load()`
or `ElCarroLoader.lazy_load()`.
`lazy_load` returns a generator that only queries database during the iteration.
To initialize `ElCarroLoader` class you need to provide:

1. `elcarro_engine` - An instance of a `ElCarroEngine` engine.
2. `table_name` - The name of the table within the Oracle database to store
   langchain documents.

```python
from langchain_google_el_carro import import ElCarroLoader

loader = ElCarroLoader(elcarro_engine=elcarro_engine, table_name=TABLE_NAME)
docs = loader.lazy_load()
for doc in docs:
    print("Loaded documents:", doc)
```

### Load documents via query

Other than loading documents from a table, we can also choose to load documents
from a view generated from a SQL query. For example:

```python
from langchain_google_el_carro import ElCarroLoader

loader = ElCarroLoader(
    elcarro_engine=elcarro_engine,
    query=f"SELECT * FROM {table_name} WHERE json_value(extra_json_metadata, '$.shape') = 'round'"
)
onedoc = loader.load()
print(onedoc)
```

The view generated from SQL query can have different schema than default table.
In such cases, the behavior of ElCarroLoader is the same as loading from table
with non-default schema. Please refer to
section [Load documents with customized document page content & metadata](#load-documents-with-customized-document-page-content--metadata).

### Delete documents

Delete a list of langchain documents from an Oracle table
with `ElCarroDocumentSaver.delete(<documents>)`.

For a table with a default schema (page_content, langchain_metadata), the
deletion criteria is:

A `row` should be deleted if there exists a `document` in the list, such that

- `document.page_content` equals `row[page_content]`
- `document.metadata` equals `row[langchain_metadata]`

```python
docs = loader.load()
print("Documents before delete:", docs)
saver.delete(onedoc)
print("Documents after delete:", loader.load())
```

## Advanced Usage

### Load documents with customized document page content & metadata

First we prepare an example table with non-default schema, and populate it with
some arbitrary data.

```python
import sqlalchemy

create_table_query = f"""CREATE TABLE {table_name} (
    fruit_id NUMBER GENERATED BY DEFAULT AS IDENTITY (START WITH 1),
    fruit_name VARCHAR2(100) NOT NULL,
    variety VARCHAR2(50),  
    quantity_in_stock NUMBER(10) NOT NULL,
    price_per_unit NUMBER(6,2) NOT NULL,
    organic NUMBER(3) NOT NULL
)"""
        
with elcarro_engine.connect() as conn:
    conn.execute(sqlalchemy.text(create_table_query))
    conn.commit()
    conn.execute(
        sqlalchemy.text(
            f"""
            INSERT INTO {table_name} (fruit_name, variety, quantity_in_stock, price_per_unit, organic)
            VALUES ('Apple', 'Granny Smith', 150, 0.99, 1)
            """
        )
    )
    conn.execute(
        sqlalchemy.text(
            f"""
            INSERT INTO {table_name} (fruit_name, variety, quantity_in_stock, price_per_unit, organic)
            VALUES ('Banana', 'Cavendish', 200, 0.59, 0)
            """
        )
    )
    conn.execute(
        sqlalchemy.text(
            f"""
            INSERT INTO {table_name} (fruit_name, variety, quantity_in_stock, price_per_unit, organic)
            VALUES ('Orange', 'Navel', 80, 1.29, 1)
            """
        )
    )
    conn.commit()
```

If we still load langchain documents with default parameters of `ElCarroLoader`
from this example table, the `page_content` of loaded documents will be the
first column of the table, and `metadata` will be consisting of key-value pairs
of all the other columns.

```python
loader = ElCarroLoader(
    elcarro_engine=elcarro_engine,
    table_name=TABLE_NAME,
)
loader.load()
```

We can specify the content and metadata we want to load by setting
the `content_columns` and `metadata_columns` when initializing
the `ElCarroLoader`.

1. `content_columns`: The columns to write into the `page_content` of the
   document.
2. `metadata_columns`: The columns to write into the `metadata` of the document.

For example here, the values of columns in `content_columns` will be joined
together into a space-separated string, as `page_content` of loaded documents,
and `metadata` of loaded documents will only contain key-value pairs of columns
specified in `metadata_columns`.

```python
loader = ElCarroLoader(
    elcarro_engine=elcarro_engine,
    table_name=table_name,
    content_columns=[
        "variety",
        "quantity_in_stock",
        "price_per_unit",
        "organic",
    ],
    metadata_columns=["fruit_id", "fruit_name"],
)
loaded_docs = loader.load()
print(f"Loaded Documents: [{loaded_docs}]")
```

### Save document with customized page content & metadata

In order to save langchain document into table with customized metadata fields.
We need first create such a table via `ElCarroEngine.init_document_table()`, and
specify the list of `metadata_columns` we want it to have. In this example, the
created table will have table columns:

- description (type: text): for storing fruit description.
- fruit_name (type text): for storing fruit name.
- organic (type tinyint(1)): to tell if the fruit is organic.
- other_metadata (type: JSON): for storing other metadata information of the
  fruit.

We can use the following parameters
with `elcarro_engine.init_document_table()` to create the table:

1. `table_name`: The name of the table within the Oracle database to store
   langchain documents.
2. `metadata_columns`: A list of `sqlalchemy.Column` indicating the list of
   metadata columns we need.
3. `content_column`: column name to store `page_content` of langchain
   document. Default: `"page_content", "VARCHAR2(4000)"`
4. `metadata_json_column`: column name to store extra
   JSON `metadata` of langchain document.
   Default: `"langchain_metadata", "VARCHAR2(4000)"`.

```python
elcarro_engine.init_document_table(
    table_name=table_name,
    metadata_columns=[
        sqlalchemy.Column("type", sqlalchemy.dialects.oracle.VARCHAR2(200)),
        sqlalchemy.Column("weight", sqlalchemy.INT),
    ],
    content_column="content",
    metadata_json_column="extra_json_metadata"
)
```

Save documents with `ElCarroDocumentSaver.add_documents(<documents>)`. As you
can see in this example,

- `document.page_content` will be saved into `page_content` column.
- `document.metadata.type` will be saved into `type` column.
- `document.metadata.weight` will be saved into `weight` column.
- `document.metadata.organic` will be saved into `extra_json_metadata` column in
  JSON format.

```python
doc = Document(
    page_content="Banana",
    metadata={"type": "fruit", "weight": 100, "organic": 1},
)

print(f"Original Document: [{doc}]")

saver = ElCarroDocumentSaver(
    elcarro_engine=elcarro_engine,
    table_name=table_name,
    content_column="content",
    metadata_json_column="extra_json_metadata",
)
saver.add_documents([doc])
```

### Delete documents with customized page content & metadata

We can also delete documents from table with customized metadata columns
via `ElCarroDocumentSaver.delete(<documents>)`. The deletion criteria is:

A `row` should be deleted if there exists a `document` in the list, such that

- `document.page_content` equals `row[page_content]`
- For every metadata field `k` in `document.metadata`
    - `document.metadata[k]` equals `row[k]` or `document.metadata[k]`
      equals `row[langchain_metadata][k]`
- There is no extra metadata field present in `row` but not
  in `document.metadata`.

```python
saver.delete(loaded_docs)
print(f"Documents left: {len(loader.load())}")
```

## Full example

Please look
at [demo_doc_loader_basic.py](https://github.com/googleapis/langchain-google-el-carro-python/tree/main/samples/demo_doc_loader_basic.py)
and [demo_doc_loader_advanced.py](https://github.com/googleapis/langchain-google-el-carro-python/tree/main/samples/demo_doc_loader_advanced.py)
for
complete code examples.




