virtualenv /tmp/v1 && \
source /tmp/v1/bin/activate && \
pip install --require-hashes -r requirements.txt && \
export PYTHONPATH=".:src/" && \
black --check . && \
isort --check --profile black . && \
python -m pytest