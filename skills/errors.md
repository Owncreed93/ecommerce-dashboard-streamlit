2026-04-26 15:54:30.511 Uncaught app execution
Traceback (most recent call last):
  File "/home/owncreed93/Development/dataset/.venv/lib/python3.13/site-packages/streamlit/runtime/scriptrunner/exec_code.py", line 129, in exec_func_with_error_handling
    result = func()
  File "/home/owncreed93/Development/dataset/.venv/lib/python3.13/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 689, in code_to_exec
    exec(code, module.__dict__)  # noqa: S102
    ~~~~^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/owncreed93/Development/dataset/main.py", line 158, in <module>
    main()
    ~~~~^^
  File "/home/owncreed93/Development/dataset/main.py", line 29, in main
    filters_data = service.get_filters_data()
  File "/home/owncreed93/Development/dataset/src/application/kpi_service.py", line 64, in get_filters_data
    "countries": self.repository.get_unique_countries(),
                 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/owncreed93/Development/dataset/src/infrastructure/polars_repository.py", line 89, in get_unique_countries
    self._get_lazy_frame()
    ~~~~~~~~~~~~~~~~~~~~^^
  File "/home/owncreed93/Development/dataset/src/infrastructure/polars_repository.py", line 32, in _get_lazy_frame
    source = self.data_provider.ensure_data_is_available()
  File "/home/owncreed93/Development/dataset/src/infrastructure/hybrid_data_provider.py", line 43, in ensure_data_is_available
    url = st.secrets.get(OCI_PAR_URL_KEY)
  File "<frozen _collections_abc>", line 811, in get
  File "/home/owncreed93/Development/dataset/.venv/lib/python3.13/site-packages/streamlit/runtime/secrets.py", line 467, in __getitem__
    value = self._parse()[key]
            ~~~~~~~~~~~^^
  File "/home/owncreed93/Development/dataset/.venv/lib/python3.13/site-packages/streamlit/runtime/secrets.py", line 369, in _parse
    raise StreamlitSecretNotFoundError(error_msg)
streamlit.errors.StreamlitSecretNotFoundError: No secrets found. Valid paths for a secrets.toml file or secret directories are: /home/owncreed93/.streamlit/secrets.toml, /home/owncreed93/Development/dataset/.streamlit/secrets.toml
