# gs-rest-service-monitor

A lightweight external uptime monitor for the [gs-rest-service](https://github.com/kenze-p/gs-rest-service) project. Runs as an independent Python script that polls the service's health and posts a Slack alert whenever its status changes.

## Why an external monitor

The main project already includes infrastructure-level monitoring (Prometheus, Grafana, Node Exporter) running on the same server as the application. That setup can't report an outage if the whole server goes down — it goes down with it.

This script runs separately (e.g. on a different machine) and checks the service from the outside, the same way a real user would, so it can still alert on total server failure.

## How It Works

- Polls a configured endpoint every 30 seconds
- Sends a Slack message only when the status **changes** (up → down or down → up), not on every check
- Logs every check to both the console and a local `monitor.log` file

```
Monitor script ──(HTTP GET, every 30s)──> gs-rest-service /greeting
      │
      └──(on status change)──> Slack channel
```

## Tech Stack

- Python 3
- `requests` for HTTP checks
- Slack Web API for alerting
- Standard library `logging`

## Configuration

The script is configured via environment variables — no credentials are hardcoded:

| Variable | Required | Description |
|---|---|---|
| `SLACK_BOT_TOKEN` | Yes | Slack bot token used to post alerts |
| `SLACK_CHANNEL_ID` | No (has a default) | Slack channel to post alerts to |

The target URL and check interval are set as constants at the top of the script and can be edited directly.

## Running It

```bash
export SLACK_BOT_TOKEN=xoxb-your-token-here
export SLACK_CHANNEL_ID=your-channel-id
python monitor.py
```

## Project Status

The URL currently in the script points to an EC2 instance that has since been decommissioned as part of the companion `gs-rest-service` project's cost cleanup, so the target is not currently live. The script itself is fully functional against any HTTP endpoint — update `SERVICE_URL` to point it at a running service.
