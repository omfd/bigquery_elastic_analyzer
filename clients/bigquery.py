"""Simple application that performs a query with BigQuery."""
from google.cloud import bigquery
import uuid


def explicit():
    from google.cloud import bigquery

    # Explicitly use service account credentials by specifying the private key
    # file. All clients in google-cloud-python have this helper, see
    # https://google-cloud-python.readthedocs.io/en/latest/core/modules.html
    #   #google.cloud.client.Client.from_service_account_json
    bigquery_client = bigquery.Client.from_service_account_json(
        'service_account.json')

    # Make an authenticated API request
    buckets = list(bigquery_client.list_datasets())
    print(len(buckets))
    tables = list(bigquery_client.__dict__)
    print tables
    for bucket in buckets:
        print bucket.__dict__

    query_job = bigquery_client.run_async_query(str(uuid.uuid4()), """
        #standardSQL
        SELECT corpus AS title, COUNT(*) AS unique_words
        FROM `publicdata.samples.shakespeare`
        GROUP BY title
        ORDER BY unique_words DESC
        LIMIT 10""")

    query_job.begin()
    query_job.result()  # Wait for job to complete.
    # [END run_query]

    # [START print_results]
    destination_table = query_job.destination
    destination_table.reload()
    for row in destination_table.fetch_data():
        print(row)
        # [END print_results]


class BigQueryClient:
    """
    Big Query Client with connection string and method for querying
    """

    def __init__(self):
        """
        Constructor
        """
        self.bq = bigquery.Client.from_service_account_json(
            'service_account.json')
