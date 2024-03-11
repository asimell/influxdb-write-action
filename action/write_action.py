from datetime import datetime
from influxdb_client import InfluxDBClient, Point

import os
import requests
import json

def parse_workflow_data() -> Point:
    p = Point("workflow_data")
    run_id = os.getenv("WORKFLOW_RUN_ID")
    repo = os.getenv("REPO")
    owner = os.getenv("OWNER")
    token = os.getenv("GH_TOKEN")

    assert run_id != None
    assert repo != None
    assert owner != None
    assert token != None
    assert token != ""

    resp = requests.get(f"https://api.github.com/repos/{owner}/{repo}/actions/runs/{run_id}",
                       headers={"Accept": "application/vnd.github+json",
                                "Authorization": f"Bearer {token}",
                                "X-GitHub-Api-Version": "2022-11-28"})
    data = json.loads(resp.text)

    if resp.status_code != 200:
        raise RuntimeError(resp.text)

    p.tag("name", data["name"])
    p.tag("path", data["path"])
    p.tag("repository", f"{owner}/{repo}")
    p.field("name", data["name"])
    p.field("path", data["path"])
    p.field("repository", f"{owner}/{repo}")
    p.field("head_branch", data["head_branch"])
    p.field("run_number", data["run_number"])
    p.field("result", data["conclusion"])

    start_time = data["run_started_at"]
    end_time = data["updated_at"]
    elapsed_time = (datetime.fromisoformat(end_time) - datetime.fromisoformat(start_time)).total_seconds()

    p.field("start_time", start_time)
    p.field("duration", elapsed_time)
    p.field("user", data["triggering_actor"]["login"])
    p.field("cause", data["event"])

    return p


def main():
    p = parse_workflow_data()

    client = InfluxDBClient.from_env_properties()

    bucket = os.getenv("INFLUXDB_V2_BUCKET")
    with client.write_api() as write_api:
        write_api.write(bucket=bucket, record=p)


if __name__ == "__main__":
    main()