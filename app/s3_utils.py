"""
S3 helper: upload any file. If it’s an image (JPEG/PNG),
also create a 300×300 thumbnail and upload that.

Requires:
    boto3
    Pillow
"""

import uuid, io
from pathlib import Path
from typing import Tuple

import boto3
from PIL import Image
import streamlit as st

# ----------------------------------------------------------------------
# AWS credentials (from .streamlit/secrets.toml)
# ----------------------------------------------------------------------
AWS = st.secrets["aws"]
BUCKET = AWS["bucket"]

s3 = boto3.client(
    "s3",
    region_name=AWS["region"],
    aws_access_key_id=AWS["access_key"],
    aws_secret_access_key=AWS["secret_key"],
)

THUMB_SIZE = (300, 300)  # px

# ----------------------------------------------------------------------
# Internal upload helper
# ----------------------------------------------------------------------
def _s3_upload(buf, key, content_type="application/octet-stream"):
    """
    Upload a BytesIO/BufferedReader to S3 with private ACL.
    """
    s3.upload_fileobj(
        Fileobj=buf,
        Bucket=BUCKET,
        Key=key,
        ExtraArgs={"ACL": "private", "ContentType": content_type},
    )

# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def upload_file_with_thumb(file_obj, object_prefix: str) -> Tuple[str, str | None]:
    """
    Uploads `file_obj` to S3 under `object_prefix`.
    If the file is an image (JPEG/PNG), a thumbnail is generated and uploaded.

    Returns (orig_key, thumb_key_or_None)
    """
    ext  = Path(file_obj.name).suffix.lower()
    mime = file_obj.type or "application/octet-stream"

    # ---------- 1) Upload original ----------
    orig_key = f"{object_prefix}/{uuid.uuid4()}{ext}"
    file_obj.seek(0)
    _s3_upload(file_obj, orig_key, content_type=mime)

    # ---------- 2) Thumbnail (only for images) ----------
    if mime.startswith("image/"):
        file_obj.seek(0)
        img = Image.open(file_obj)
        img.thumbnail(THUMB_SIZE)
        thumb_buf = io.BytesIO()
        img.save(thumb_buf, format="JPEG", quality=85)
        thumb_buf.seek(0)

        thumb_key = f"{object_prefix}/{uuid.uuid4()}_thumb.jpg"
        _s3_upload(thumb_buf, thumb_key, content_type="image/jpeg")
        return orig_key, thumb_key

    return orig_key, None

def presigned_url(key: str, expires=3600) -> str:
    """
    Generate a temporary download URL for any S3 object.
    """
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET, "Key": key},
        ExpiresIn=expires,
    )"""
S3 helper: upload any file. If it’s an image (JPEG/PNG),
also create a 300×300 thumbnail and upload that.

Requires:
    boto3
    Pillow
"""

import uuid, io
from pathlib import Path
from typing import Tuple

import boto3
from PIL import Image
import streamlit as st

# ----------------------------------------------------------------------
# AWS credentials (from .streamlit/secrets.toml)
# ----------------------------------------------------------------------
AWS = st.secrets["aws"]
BUCKET = AWS["bucket"]

s3 = boto3.client(
    "s3",
    region_name=AWS["region"],
    aws_access_key_id=AWS["access_key"],
    aws_secret_access_key=AWS["secret_key"],
)

THUMB_SIZE = (300, 300)  # px

# ----------------------------------------------------------------------
# Internal upload helper
# ----------------------------------------------------------------------
def _s3_upload(buf, key, content_type="application/octet-stream"):
    """
    Upload a BytesIO/BufferedReader to S3 with private ACL.
    """
    s3.upload_fileobj(
        Fileobj=buf,
        Bucket=BUCKET,
        Key=key,
        ExtraArgs={"ACL": "private", "ContentType": content_type},
    )

# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def upload_file_with_thumb(file_obj, object_prefix: str) -> Tuple[str, str | None]:
    """
    Uploads `file_obj` to S3 under `object_prefix`.
    If the file is an image (JPEG/PNG), a thumbnail is generated and uploaded.

    Returns (orig_key, thumb_key_or_None)
    """
    ext  = Path(file_obj.name).suffix.lower()
    mime = file_obj.type or "application/octet-stream"

    # ---------- 1) Upload original ----------
    orig_key = f"{object_prefix}/{uuid.uuid4()}{ext}"
    file_obj.seek(0)
    _s3_upload(file_obj, orig_key, content_type=mime)

    # ---------- 2) Thumbnail (only for images) ----------
    if mime.startswith("image/"):
        file_obj.seek(0)
        img = Image.open(file_obj)
        img.thumbnail(THUMB_SIZE)
        thumb_buf = io.BytesIO()
        img.save(thumb_buf, format="JPEG", quality=85)
        thumb_buf.seek(0)

        thumb_key = f"{object_prefix}/{uuid.uuid4()}_thumb.jpg"
        _s3_upload(thumb_buf, thumb_key, content_type="image/jpeg")
        return orig_key, thumb_key

    return orig_key, None

def presigned_url(key: str, expires=3600) -> str:
    """
    Generate a temporary download URL for any S3 object.
    """
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET, "Key": key},
        ExpiresIn=expires,
    )"""
S3 helper: upload any file. If it’s an image (JPEG/PNG),
also create a 300×300 thumbnail and upload that.

Requires:
    boto3
    Pillow
"""

import uuid, io
from pathlib import Path
from typing import Tuple

import boto3
from PIL import Image
import streamlit as st

# ----------------------------------------------------------------------
# AWS credentials (from .streamlit/secrets.toml)
# ----------------------------------------------------------------------
AWS = st.secrets["aws"]
BUCKET = AWS["bucket"]

s3 = boto3.client(
    "s3",
    region_name=AWS["region"],
    aws_access_key_id=AWS["access_key"],
    aws_secret_access_key=AWS["secret_key"],
)

THUMB_SIZE = (300, 300)  # px

# ----------------------------------------------------------------------
# Internal upload helper
# ----------------------------------------------------------------------
def _s3_upload(buf, key, content_type="application/octet-stream"):
    """
    Upload a BytesIO/BufferedReader to S3 with private ACL.
    """
    s3.upload_fileobj(
        Fileobj=buf,
        Bucket=BUCKET,
        Key=key,
        ExtraArgs={"ACL": "private", "ContentType": content_type},
    )

# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def upload_file_with_thumb(file_obj, object_prefix: str) -> Tuple[str, str | None]:
    """
    Uploads `file_obj` to S3 under `object_prefix`.
    If the file is an image (JPEG/PNG), a thumbnail is generated and uploaded.

    Returns (orig_key, thumb_key_or_None)
    """
    ext  = Path(file_obj.name).suffix.lower()
    mime = file_obj.type or "application/octet-stream"

    # ---------- 1) Upload original ----------
    orig_key = f"{object_prefix}/{uuid.uuid4()}{ext}"
    file_obj.seek(0)
    _s3_upload(file_obj, orig_key, content_type=mime)

    # ---------- 2) Thumbnail (only for images) ----------
    if mime.startswith("image/"):
        file_obj.seek(0)
        img = Image.open(file_obj)
        img.thumbnail(THUMB_SIZE)
        thumb_buf = io.BytesIO()
        img.save(thumb_buf, format="JPEG", quality=85)
        thumb_buf.seek(0)

        thumb_key = f"{object_prefix}/{uuid.uuid4()}_thumb.jpg"
        _s3_upload(thumb_buf, thumb_key, content_type="image/jpeg")
        return orig_key, thumb_key

    return orig_key, None

def presigned_url(key: str, expires=3600) -> str:
    """
    Generate a temporary download URL for any S3 object.
    """
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET, "Key": key},
        ExpiresIn=expires,
    )
  Add S3 helper with thumbnail logic
