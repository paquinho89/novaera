from storages.backends.gcloud import GoogleCloudStorage
from django.conf import settings


class StaticRootGoogleCloudStorage(GoogleCloudStorage):
    location = "static"
    bucket_name = settings.GS_BUCKET_NAME


class MediaRootGoogleCloudStorage(GoogleCloudStorage):
    location = ""
    bucket_name = settings.GS_BUCKET_NAME
