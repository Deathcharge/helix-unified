#!/usr/bin/env python3
"""
☁️ Helix Collective - Backblaze B2 Storage Client
services/backblaze_client.py

Provides S3-compatible integration with Backblaze B2 for:
- Long-term backup storage
- Archive persistence
- Cold storage for old UCF snapshots
- Disaster recovery backups

Environment Variables:
- B2_KEY_ID: Your Backblaze B2 key ID (application key ID)
- B2_APPLICATION_KEY: Your Backblaze B2 application key
- B2_BUCKET_NAME: Bucket name (e.g., helix-backups)
- B2_ENDPOINT: us-west-000.backblazeb2.com (or your region)

Free Tier: 10GB storage + 1GB/day download
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

try:
    import boto3
    from botocore.exceptions import ClientError
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False
    logger.warning(
        "⚠️ boto3 not installed. Backblaze B2 storage disabled. "
        "To enable, run: pip install boto3"
    )


class HelixBackblazeClient:
    """Backblaze B2 S3-compatible client for Helix Collective storage."""

    def __init__(self):
        """Initialize Backblaze B2 client from environment variables."""
        self.key_id = os.getenv("B2_KEY_ID")
        self.application_key = os.getenv("B2_APPLICATION_KEY")
        self.bucket_name = os.getenv("B2_BUCKET_NAME")
        self.endpoint = os.getenv("B2_ENDPOINT", "s3.us-west-000.backblazeb2.com")

        self.enabled = bool(self.key_id and self.application_key and self.bucket_name)
        self.client = None
        self.s3 = None

        if self.enabled and BOTO3_AVAILABLE:
            try:
                # Configure S3 client for Backblaze B2
                self.s3 = boto3.client(
                    's3',
                    endpoint_url=f'https://{self.endpoint}',
                    aws_access_key_id=self.key_id,
                    aws_secret_access_key=self.application_key
                )

                # Test connection by listing bucket
                self.s3.head_bucket(Bucket=self.bucket_name)

                print(f"✅ Backblaze B2 client initialized: {self.bucket_name}")
            except Exception as e:
                print(f"❌ Backblaze B2 initialization failed: {e}")
                self.enabled = False
        elif not BOTO3_AVAILABLE:
            print("⚠️ Backblaze B2 disabled: boto3 not installed")
            self.enabled = False
        else:
            print("⚠️ Backblaze B2 disabled: missing environment variables")
            print("   Required: B2_KEY_ID, B2_APPLICATION_KEY, B2_BUCKET_NAME")

    def upload_file(self, local_path: Path, remote_key: str = None) -> bool:
        """
        Upload a file to Backblaze B2.

        Args:
            local_path: Local file path
            remote_key: S3 key (if None, uses filename)

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self.s3:
            print("⚠️ Backblaze B2 not enabled")
            return False

        try:
            local_path = Path(local_path)
            if not local_path.exists():
                print(f"❌ File not found: {local_path}")
                return False

            # Determine remote key
            if remote_key is None:
                remote_key = f"helix/{local_path.name}"

            # Upload file
            self.s3.upload_file(
                str(local_path),
                self.bucket_name,
                remote_key
            )

            print(f"✅ Uploaded to Backblaze B2: {remote_key}")
            return True

        except ClientError as e:
            print(f"❌ Backblaze B2 upload failed: {e}")
            return False

    def upload_string(self, content: str, remote_key: str) -> bool:
        """
        Upload string content to Backblaze B2.

        Args:
            content: String content to upload
            remote_key: S3 key

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self.s3:
            return False

        try:
            # Upload string as bytes
            self.s3.put_object(
                Bucket=self.bucket_name,
                Key=remote_key,
                Body=content.encode('utf-8')
            )

            print(f"✅ Uploaded content to Backblaze B2: {remote_key}")
            return True

        except ClientError as e:
            print(f"❌ Backblaze B2 upload failed: {e}")
            return False

    def download_file(self, remote_key: str, local_path: Path) -> bool:
        """
        Download a file from Backblaze B2.

        Args:
            remote_key: S3 key
            local_path: Local destination path

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self.s3:
            return False

        try:
            # Ensure local directory exists
            local_path = Path(local_path)
            local_path.parent.mkdir(parents=True, exist_ok=True)

            # Download file
            self.s3.download_file(
                self.bucket_name,
                remote_key,
                str(local_path)
            )

            print(f"✅ Downloaded from Backblaze B2: {remote_key} → {local_path}")
            return True

        except ClientError as e:
            print(f"❌ Backblaze B2 download failed: {e}")
            return False

    def list_files(self, prefix: str = "helix/") -> List[Dict]:
        """
        List files in Backblaze B2 bucket.

        Args:
            prefix: Key prefix to filter by

        Returns:
            List of file info dicts
        """
        if not self.enabled or not self.s3:
            return []

        try:
            response = self.s3.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )

            files = []
            for obj in response.get('Contents', []):
                files.append({
                    'key': obj['Key'],
                    'size': obj['Size'],
                    'modified': obj['LastModified'].isoformat(),
                    'etag': obj['ETag'].strip('"')
                })

            return files

        except ClientError as e:
            print(f"❌ Backblaze B2 list failed: {e}")
            return []

    def delete_file(self, remote_key: str) -> bool:
        """
        Delete a file from Backblaze B2.

        Args:
            remote_key: S3 key

        Returns:
            True if successful, False otherwise
        """
        if not self.enabled or not self.s3:
            return False

        try:
            self.s3.delete_object(
                Bucket=self.bucket_name,
                Key=remote_key
            )

            print(f"🗑️ Deleted from Backblaze B2: {remote_key}")
            return True

        except ClientError as e:
            print(f"❌ Backblaze B2 delete failed: {e}")
            return False

    def sync_directory(self, local_dir: Path, remote_prefix: str = "helix/") -> Dict:
        """
        Sync entire local directory to Backblaze B2.

        Args:
            local_dir: Local directory path
            remote_prefix: S3 key prefix

        Returns:
            Dict with sync statistics
        """
        if not self.enabled or not self.s3:
            return {"error": "Backblaze B2 not enabled"}

        local_dir = Path(local_dir)
        if not local_dir.exists():
            return {"error": f"Directory not found: {local_dir}"}

        stats = {
            'uploaded': 0,
            'failed': 0,
            'total_size': 0
        }

        try:
            # Upload all files
            for file_path in local_dir.rglob('*'):
                if file_path.is_file():
                    # Calculate relative path
                    rel_path = file_path.relative_to(local_dir)
                    remote_key = f"{remote_prefix}{rel_path}".replace('\\', '/')

                    # Upload file
                    if self.upload_file(file_path, remote_key):
                        stats['uploaded'] += 1
                        stats['total_size'] += file_path.stat().st_size
                    else:
                        stats['failed'] += 1

            print(f"✅ Synced {stats['uploaded']} files to Backblaze B2")
            return stats

        except Exception as e:
            print(f"❌ Directory sync failed: {e}")
            stats['error'] = str(e)
            return stats

    def get_bucket_size(self) -> Dict:
        """
        Get bucket size and file count.

        Returns:
            Dict with bucket statistics
        """
        if not self.enabled or not self.s3:
            return {"error": "Backblaze B2 not enabled"}

        try:
            total_size = 0
            file_count = 0

            # List all objects
            paginator = self.s3.get_paginator('list_objects_v2')
            for page in paginator.paginate(Bucket=self.bucket_name):
                for obj in page.get('Contents', []):
                    total_size += obj['Size']
                    file_count += 1

            return {
                'total_size': total_size,
                'total_size_gb': round(total_size / (1024**3), 2),
                'file_count': file_count
            }

        except ClientError as e:
            print(f"❌ Failed to get bucket size: {e}")
            return {"error": str(e)}


# Global instance
_backblaze_client: Optional[HelixBackblazeClient] = None


def get_backblaze_client() -> Optional[HelixBackblazeClient]:
    """Get or create global Backblaze B2 client instance."""
    global _backblaze_client
    if _backblaze_client is None:
        _backblaze_client = HelixBackblazeClient()
    return _backblaze_client if _backblaze_client.enabled else None


# Quick test function
if __name__ == "__main__":
    print("🧪 Testing Backblaze B2 client...")
    client = HelixBackblazeClient()

    if client.enabled:
        print("\n✅ Backblaze B2 connection successful!")

        # Test bucket size
        size_info = client.get_bucket_size()
        if 'error' not in size_info:
            print(f"📊 Bucket: {size_info['file_count']} files, {size_info['total_size_gb']} GB")

        # Test list files
        files = client.list_files()
        print(f"📁 Files in bucket: {len(files)}")
        for file in files[:5]:  # Show first 5
            print(f"   - {file['key']} ({file['size']} bytes)")
    else:
        print("❌ Backblaze B2 not configured")
        print("Set: B2_KEY_ID, B2_APPLICATION_KEY, B2_BUCKET_NAME")
