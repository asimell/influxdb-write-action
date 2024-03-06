FROM python:3.12

COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt

COPY write_action.py .

ENTRYPOINT [ "python", "write_action.py" ]