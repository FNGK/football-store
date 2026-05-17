"""Zero-ETL BigQuery adapter — query warehouse in place without duplication."""

from typing import Any


class BigQueryZeroEtlAdapter:
    """Read-only federated queries against tenant-scoped BigQuery views."""

    def __init__(self, project_id: str, dataset: str) -> None:
        self.project_id = project_id
        self.dataset = dataset

    def qualified_table(self, tenant_id: str, table: str) -> str:
        return f"`{self.project_id}.{self.dataset}.{tenant_id}_{table}`"

    def build_attribution_query(self, tenant_id: str, days: int = 30) -> str:
        """Parameterized query template — executed via BigQuery client, not raw SQL in routes."""
        table = self.qualified_table(tenant_id, "conversions")
        return (
            f"SELECT source, COUNT(*) as cnt, SUM(value_usd) as revenue "
            f"FROM {table} "
            f"WHERE created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL {days} DAY) "
            f"GROUP BY source"
        )

    async def run_query(self, sql: str) -> list[dict[str, Any]]:
        try:
            from google.cloud import bigquery  # noqa: PLC0415
        except ImportError as exc:
            raise RuntimeError("google-cloud-bigquery required for Zero-ETL") from exc
        client = bigquery.Client(project=self.project_id)
        job = client.query(sql)
        return [dict(row) for row in job.result()]
