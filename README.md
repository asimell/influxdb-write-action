# influxdb-write-action

GitHub Action to write data from your GitHub workflows into a preconfigured InfluxDB instance.

## Exaple usage

The `GITHUB_TOKEN` must have permissions for `actions: read`. If your token doesn't already have
this, you can add it to the `permissions` section of your workflow.

```yaml
permissions:
  actions: read

jobs:
  build:
    name: Send Data
    runs-on: ubuntu-latest
    steps:
      - name: Write data to InfluxDB
        uses: asimell/influxdb-write-action@main
        with:
          github_access_token: ${{ secrets.GITHUB_TOKEN }}
          influxdb_url: my.endpoint.com
          influxdb_bucket: my-bucket
          influxdb_org: my-org
          influxdb_token: ${{ secrets.influxdb_token }}
```

## Available Settings

| Name | Default | Description |
| :--- | :--- | :--- |
| github_access_token | | Token to access Github API. `GITHUB_TOKEN` should be sufficient if you're sending data from the same workflow. |
| repository | `${{ github.repository }}` | Repository where the data will be retrieved |
| workflow_run_id | `${{ github.run_id }}` | Workflow run ID of the data you want to write |
| influxdb_url | | InfluxDB instance URL |
| influxdb_bucket | | InfluxDB instance bucket |
| influxdb_org | | InfluxDB instance organization |
| influxdb_token | | InfluxDB access token |
| influxdb_timeout | 10000 | InfluxDB connection timeout in milliseconds |
| influxdb_verify_ssl | "true" | Set this to false to skip verifying SSL certificate when calling API from https server |
| influxdb_ssl_ca_cert | | Set this to customize the certificate file to verify the peer |
| influxdb_cert_file | | Path to the certificate that will be used for mTLS authentication |
| influxdb_cert_key_file | | Path to the file contains private key for mTLS certificate |
| influxdb_cert_key_password | | String or function which returns password for decrypting the mTLS private key |
| influxdb_connection_pool_maxsize | 10000 | Set the number of connections to save that can be reused by urllib3 |
| influxdb_auth_basic | | Enable http basic authentication when talking to a InfluxDB 1.8.x without authentication but is accessed via reverse proxy with basic authentication (defaults to false) |
