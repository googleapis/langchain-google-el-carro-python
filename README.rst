El Carro for Oracle Databases for LangChain
==================================================

|preview| |pypi| |versions|

- `Client Library Documentation`_
- `Product Documentation`_

.. |preview| image:: https://img.shields.io/badge/support-preview-orange.svg
   :target: https://github.com/googleapis/google-cloud-python/blob/main/README.rst#stability-levels
.. |pypi| image:: https://img.shields.io/pypi/v/langchain-google-el-carro.svg  
   :target: https://pypi.org/project/langchain-google-el-carro/
.. |versions| image:: https://img.shields.io/pypi/pyversions/langchain-google-el-carro.svg
   :target: https://pypi.org/project/langchain-google-el-carro/
.. _Client Library Documentation: https://cloud.google.com/python/docs/reference/langchain-google-el-carro/latest
.. _Product Documentation: https://github.com/GoogleCloudPlatform/elcarro-oracle-operator

Known Limitations
-----------------

- The library supports El Carro Operator for Oracle 18c and higher versions.

- By default the library uses `thin mode.`_ for Oracle connectivity,
  to use thick mode please follow the corresponding `section.`_.

- To use VARCHAR2 datatype of size more than 4000 please change the parameter `MAX_STRING_SIZE.`_
  in the Oracle instance.

.. _thin mode.: https://python-oracledb.readthedocs.io/en/latest/user_guide/appendix_b.html
.. _section.: #oracle-thick-mode-connectivity
.. _MAX_STRING_SIZE.: https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/MAX_STRING_SIZE.html#GUID-D424D23B-0933-425F-BC69-9C0E6724693C

Quick Start
-----------

Create an El Carro Operator Oracle Instance and a Database (PDB)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to use this library, you first need to have an El Carro Operator
software running with an Instance (CDB) and a Database (PDB).

Please follow the steps for El Carro Oracle Operator to provision a new database
and create a PDB:

- `El Carro Oracle 18c XE quickstart`_
- `El Carro Oracle 19c EE quickstart`_

.. _El Carro Oracle 18c XE quickstart: https://github.com/GoogleCloudPlatform/elcarro-oracle-operator/blob/main/docs/content/quickstart-18c-xe.md
.. _El Carro Oracle 19c EE quickstart: https://github.com/GoogleCloudPlatform/elcarro-oracle-operator/blob/main/docs/content/quickstart-19c-ee.md


Installation
~~~~~~~~~~~~

Install this library in a `virtualenv`_ using pip. `virtualenv`_ is a tool to create isolated Python environments. The basic problem it addresses is
one of dependencies and versions, and indirectly permissions.

With `virtualenv`_, it’s
possible to install this library without needing system install
permissions, and without clashing with the installed system
dependencies.

.. _`virtualenv`: https://virtualenv.pypa.io/en/latest/

Supported Python Versions
^^^^^^^^^^^^^^^^^^^^^^^^^

Python >= 3.8

Mac/Linux
^^^^^^^^^

.. code-block:: console

   pip install virtualenv
   virtualenv <your-env>
   source <your-env>/bin/activate
   <your-env>/bin/pip install langchain-google-el-carro

Windows
^^^^^^^

.. code-block:: console

    pip install virtualenv
    virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install langchain-google-el-carro


Document Loader Usage
~~~~~~~~~~~~~~~~~~~~~

Use a document loader to load data as LangChain ``Document``\ s.

.. code-block:: python

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

See the full `Document Loader`_ tutorial.

.. _`Document Loader`: https://github.com/googleapis/langchain-google-el-carro-python/blob/main/docs/document_loader.ipynb

Chat Message History Usage
~~~~~~~~~~~~~~~~~~~~~~~~~~

Use ``ChatMessageHistory`` to store messages and provide conversation
history to LLMs.

.. code:: python

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

See the full `Chat Message History`_ tutorial.

.. _`Chat Message History`: https://github.com/googleapis/langchain-google-el-carro-python/blob/main/docs/chat_message_history.ipynb


Oracle Thick Mode Connectivity
------------------------------

Thick mode connectivity requires you to install the Oracle Client libraries and pass ``thick_mode=True`` to ``ElCarroEngine``. Follow these sections of the `oracledb` installation guide:

- `Oracle Instant Client Zip Files`_
- `Oracle Instant Client RPMs`_

Example for Linux x64, glibc 2.14+::

    wget https://download.oracle.com/otn_software/linux/instantclient/2113000/instantclient-basic-linux.x64-21.13.0.0.0dbru.zip -O /tmp/drv.zip
    rm -fr /tmp/instantclient_21_13/; unzip /tmp/drv.zip -d /tmp
    export LD_LIBRARY_PATH=/tmp/instantclient_21_13/:$LD_LIBRARY_PATH

.. _Oracle Instant Client Zip Files: https://python-oracledb.readthedocs.io/en/latest/user_guide/installation.html#oracle-instant-client-zip-files
.. _Oracle Instant Client RPMs: https://python-oracledb.readthedocs.io/en/latest/user_guide/installation.html#oracle-instant-client-rpms


Contributions
~~~~~~~~~~~~~

Contributions to this library are always welcome and highly encouraged.

See `CONTRIBUTING`_ for more information how to get started.

Please note that this project is released with a Contributor Code of Conduct. By participating in
this project you agree to abide by its terms. See `Code of Conduct`_ for more
information.

.. _`CONTRIBUTING`: https://github.com/googleapis/langchain-google-el-carro-python/blob/main/CONTRIBUTING.md
.. _`Code of Conduct`: https://github.com/googleapis/langchain-google-el-carro-python/blob/main/CODE_OF_CONDUCT.md

License
-------

Apache 2.0 - See
`LICENSE <https://github.com/googleapis/langchain-google-el-carro-python/tree/main/LICENSE>`_
for more information.

Disclaimer
----------

This is not an officially supported Google product.
