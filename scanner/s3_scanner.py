import boto3
from botocore.exceptions import ClientError
import json

def scan_s3_buckets():
    # Initialize the Boto3 S3 client
    s3_client = boto3.client('s3')
    findings = []

    print("Starting S3 Scan...")
    
    try:
        # Step 8: Call the API to list all buckets
        response = s3_client.list_buckets()
        buckets = response.get('Buckets', [])

        # Step 10: Dynamic processing (no hardcoding)
        for bucket in buckets:
            bucket_name = bucket['Name']
            print(f"Scanning bucket: {bucket_name}")

            # Step 9: Check configuration
            try:
                pab_response = s3_client.get_public_access_block(Bucket=bucket_name)
                config = pab_response['PublicAccessBlockConfiguration']

                # If any of the block settings are False, it's a security risk
                if not config.get('BlockPublicAcls') or not config.get('BlockPublicPolicy'):
                    findings.append({
                        "resource": bucket_name,
                        "service": "S3",
                        "severity": "HIGH",
                        "issue": "Public access not fully blocked",
                        "recommendation": "Enable all Block Public Access settings"
                    })
                    
            except ClientError as e:
                # AWS throws a specific error if no Public Access Block exists at all
                if e.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
                    findings.append({
                        "resource": bucket_name,
                        "service": "S3",
                        "severity": "CRITICAL",  # Step 11: Severity logic
                        "issue": "No Public Access Block configured",
                        "recommendation": "Enable Block Public Access"
                    })


                    try:
                        s3_client.get_bucket_encryption(Bucket=bucket_name)
                    except ClientError as e:
                        if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                            findings.append({
                                "resource": bucket_name,
                                "service": "S3",
                                "severity": "MEDIUM",
                                "issue": "No server-side encryption configured",
                                "recommendation": "Enable server-side encryption for the bucket"
                            })

                    try:
                        versioning = s3_client.get_bucket_versioning(Bucket=bucket_name)
                    except ClientError:
                        pass

                if versioning.get('Status') != 'Enabled':
                    findings.append({
                        "resource": bucket_name,
                        "service": "S3",
                        "severity": "LOW",
                        "issue": "Bucket versioning disabled",
                        "recommendation": "Enable versioning to protect against accidental deletion"
                    })
            except ClientError:
                pass

                            

        return findings

    except Exception as e:
        print(f"Error connecting to S3: {e}")
        return []

if __name__ == "__main__":
    results = scan_s3_buckets()
    print("\n--- Scan Results ---")
    print(json.dumps(results, indent=2))