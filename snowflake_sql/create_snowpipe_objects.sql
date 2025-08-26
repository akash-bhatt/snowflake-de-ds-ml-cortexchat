CREATE STORAGE INTEGRATION SF_POC_S3_INTEGRATION
  TYPE = EXTERNAL_STAGE
  STORAGE_PROVIDER = 'S3'
  ENABLED = TRUE
  STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::892537290433:role/sf-poc-snowpipe-role'
  STORAGE_ALLOWED_LOCATIONS = ('s3://sf-poc-data-2025/sales_data/');
  --[ STORAGE_BLOCKED_LOCATIONS = ('<protocol>://<bucket>/<path>/', '<protocol>://<bucket>/<path>/') ]