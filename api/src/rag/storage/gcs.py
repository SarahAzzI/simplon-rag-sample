from google.api_core.client_options import ClientOptions
from google.cloud import storage

from rag.config.settings import get_settings


def get_storage_client() -> storage.Client:
    settings = get_settings()
    if settings.gcs_endpoint:
        # Local → Fake GCS
        client_options = ClientOptions(api_endpoint=settings.gcs_endpoint)
        return storage.Client(client_options=client_options)
    # Prod → vrai GCS
    return storage.Client()

async def upload_to_gcs(filename: str, content: bytes) -> str:
    settings = get_settings()
    client = get_storage_client()
    bucket = client.bucket(settings.gcs_bucket)
    blob = bucket.blob(filename)
    blob.upload_from_string(content, content_type="application/pdf")
    return f"gs://{settings.gcs_bucket}/{filename}"

async def download_from_gcs(filename: str) -> bytes:
    settings = get_settings()
    client = get_storage_client()
    bucket = client.bucket(settings.gcs_bucket)
    blob = bucket.blob(filename)
    return blob.download_as_bytes()