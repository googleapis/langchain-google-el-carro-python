# El Carro for Oracle Databases for Langchain

This package contains the [LangChain][langchain] integrations for
the [Google El Carro Oracle Operator](https://github.com/GoogleCloudPlatform/elcarro-oracle-operator).

> **🧪 Preview:** This feature is covered by the Pre-GA Offerings Terms of the
> Google Cloud Terms of Service. Please note that pre-GA products and features
> might have limited support, and changes to pre-GA products and features might
> not be compatible with other pre-GA versions. For more information, see
> the [launch stage descriptions](https://cloud.google.com/products#product-launch-stages)

* [Documentation](https://github.com/googleapis/langchain-google-el-carro-python/tree/main/docs/)

## Known Limitations

* The library supports El Carro Operator for Oracle 18c and higher versions.
* By default the library
  uses [thin mode](https://python-oracledb.readthedocs.io/en/latest/user_guide/appendix_b.html)
  for Oracle connectivity,
  to use thick mode please follow the
  corresponding [section](#oracle-thick-mode-connectivity).
* To use VARCHAR2 datatype of size more than 4000 please
  change the
  parameter [MAX_STRING_SIZE](https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/MAX_STRING_SIZE.html#GUID-D424D23B-0933-425F-BC69-9C0E6724693C)
  in the Oracle instance.

## Getting Started

### Create an El Carro Operator Oracle Instance and a Database (PDB)

In order to use this library, you first need to have an El Carro Operator
software running
with an Instance (CDB) and a Database (PDB).

Please follow the steps for El Carro Oracle Operator to provision a new database
and create a PDB:

* [El Carro Oracle 18c XE quickstart](https://github.com/GoogleCloudPlatform/elcarro-oracle-operator/blob/main/docs/content/quickstart-18c-xe.md)
* [El Carro Oracle 19c EE quickstart](https://github.com/GoogleCloudPlatform/elcarro-oracle-operator/blob/main/docs/content/quickstart-19c-ee.md)

### Installation

Install this library in a [`virtualenv`][venv] using pip. [`virtualenv`][venv]
is a tool to
create isolated Python environments. The basic problem it addresses is one of
dependencies and versions, and indirectly permissions.

With [`virtualenv`][venv], it's possible to install this library without needing
system
install permissions, and without clashing with the installed system
dependencies.

```bash
pip install virtualenv
virtualenv <your-env>
source <your-env>/bin/activate
<your-env>/bin/pip install langchain-google-el-carro-python
```

## Document Loader Usage

Use
a [document loader](https://python.langchain.com/docs/modules/data_connection/document_loaders/)
to load data as LangChain `Document`s.

```python
from langchain_google_el_carro import ElCarroEngine
from langchain_google_el_carro.loader import \
    ElCarroLoader, ElCarroDocumentSaver

elcarro_engine = ElCarroEngine.from_instance(
    "Your El Carro endpoint hostname", # e.g. 127.0.0.1
    "Your El Carro endpoint port", # e.g. 3307
    "Your PDB name",  # e.g. PDB1
    "Your DB user",
    "Your DB password",
)
loader = ElCarroLoader(
    elcarro_engine,
    table_name="my-table-name"
)
docs = loader.lazy_load()
```

See the
full [Document Loader](https://github.com/googleapis/langchain-google-el-carro-python/tree/main/docs/doc_loader.md)
tutorial.

## Chat Message History Usage

Use [ChatMessageHistory](https://python.langchain.com/docs/modules/memory/chat_messages/)
to store messages and provide conversation history to LLMs.

```python
from langchain_google_el_carro import ElCarroEngine
from langchain_google_el_carro.chat_message_history import \
    ElCarroChatMessageHistory

elcarro_engine = ElCarroEngine.from_instance(
    "Your El Carro endpoint hostname", # e.g. 127.0.0.1
    "Your El Carro endpoint port", # e.g. 3307
    "Your PDB name",  # e.g. PDB1
    "Your DB user",
    "Your DB password",
)
history = ElCarroChatMessageHistory(
    elcarro_engine=elcarro_engine, 
    table_name="my-message-store",
    session_id="my-session_id"
)
```

See the
full [Chat Message History](https://github.com/googleapis/langchain-google-el-carro-python/tree/main/docs/chat_message_history.md)
tutorial.

### Oracle Thick Mode Connectivity

Thick mode connectivity requires you to install the Oracle Client libraries and
pass `thick_mode=True` to `ElCarroEngine`. Follow these
sections of the `oracledb` installation guide

* [Oracle Instant Client Zip Files](https://python-oracledb.readthedocs.io/en/latest/user_guide/installation.html#oracle-instant-client-zip-files)
* [Oracle Instant Client RPMs](https://python-oracledb.readthedocs.io/en/latest/user_guide/installation.html#oracle-instant-client-rpms)

Example for Linux x64, glibc 2.14+:

```bash
wget https://download.oracle.com/otn_software/linux/instantclient/2113000/instantclient-basic-linux.x64-21.13.0.0.0dbru.zip -O /tmp/drv.zip
rm -fr /tmp/instantclient_21_13/; unzip /tmp/drv.zip -d /tmp
export LD_LIBRARY_PATH=/tmp/instantclient_21_13/:$LD_LIBRARY_PATH
```

## Contributing

Contributions to this library are always welcome and highly encouraged.

See [CONTRIBUTING](CONTRIBUTING.md) for more information how to get started.

Please note that this project is released with a Contributor Code of Conduct. By
participating in
this project you agree to abide by its terms.
See [Code of Conduct](CODE_OF_CONDUCT.md) for more
information.

## License

Apache 2.0 - See [LICENSE](LICENSE) for more information.

## Disclaimer

This is not an officially supported Google product.

[venv]: https://virtualenv.pypa.io/en/latest/

[langchain]: https://github.com/langchain-ai/langchain