# Wifi Analyzer Exporter


## Setup python virtual environment

```bash
python -m venv --prompt virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


## Start application

```
python wifianalyzer_exporter.py
```

The following arguments can be passed to the exporter application:

 * `--listen-address`: Listen IP address, defaults to `0.0.0.0`.
 * `--port`: Listen port, defaults to `9106`.
 * `--interval`: Time interval between wifi scans, defaults to `30`.
