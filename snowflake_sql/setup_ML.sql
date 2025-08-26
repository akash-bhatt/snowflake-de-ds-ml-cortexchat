-- Using ACCOUNTADMIN, create a new role for this exercise 
USE ROLE ACCOUNTADMIN;
SET USERNAME = (SELECT CURRENT_USER());
SELECT $USERNAME;
CREATE OR REPLACE ROLE CC_DMND_FCAST_RL;

-- Grant necessary permissions to create databases, compute pools, and service endpoints to new role
GRANT CREATE DATABASE on ACCOUNT to ROLE CC_DMND_FCAST_RL; 
--GRANT CREATE COMPUTE POOL on ACCOUNT to ROLE CC_DMND_FCAST_RL;
GRANT BIND SERVICE ENDPOINT on ACCOUNT to ROLE CC_DMND_FCAST_RL;

GRANT CREATE WAREHOUSE on ACCOUNT to ROLE CC_DMND_FCAST_RL;

-- grant new role to user and switch to that role
GRANT ROLE CC_DMND_FCAST_RL to USER identifier($USERNAME);
USE ROLE CC_DMND_FCAST_RL;

-- Create warehouse
CREATE OR REPLACE WAREHOUSE CC_DMND_FCAST_WH WITH WAREHOUSE_SIZE='MEDIUM';

-- Create Database 
CREATE OR REPLACE DATABASE CC_DMND_FCAST_ML_DB;

-- Create Schema
CREATE OR REPLACE SCHEMA MLOPS_SCHEMA;

-- Create compute pool
-- CREATE COMPUTE POOL IF NOT EXISTS MLOPS_COMPUTE_POOL 
--  MIN_NODES = 1
--  MAX_NODES = 1
--  INSTANCE_FAMILY = CPU_X64_M;

-- Using accountadmin, grant privilege to create network rules and integrations on newly created db
USE ROLE ACCOUNTADMIN;
GRANT CREATE NETWORK RULE on SCHEMA MLOPS_SCHEMA to ROLE CC_DMND_FCAST_RL;
GRANT CREATE INTEGRATION on ACCOUNT to ROLE CC_DMND_FCAST_RL;
USE ROLE CC_DMND_FCAST_RL;


 --Create network rule and api integration to install packages from pypi
-- CREATE OR REPLACE NETWORK RULE  
--  MODE = EGRESS
--  TYPE = HOST_PORT
--  VALUE_LIST = ('pypi.org', 'pypi.python.org', 'pythonhosted.org',  'files.pythonhosted.org');

 -- Create external access integration on top of network rule for pypi access
-- CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION mlops_pypi_access_integration
--  ALLOWED_NETWORK_RULES = (mlops_pypi_network_rule)
--  ENABLED = true;

-- Create an API integration with Github
CREATE OR REPLACE API INTEGRATION GITHUB_INTEGRATION_CC_DMND_FCAST_ML
   api_provider = git_https_api
   api_allowed_prefixes = ('https://github.com/Snowflake-Labs','https://github.com/akash-bhatt')
   enabled = true
   comment='Git integration with Snowflake Demo Github Repository.';

-- Create the integration with the Github demo repository
CREATE OR REPLACE GIT REPOSITORY GITHUB_REPO_DMND_FCAST_ML
   ORIGIN = 'https://github.com/akash-bhatt/snowflake-de-ds-ml-cortexchat.git' 
   API_INTEGRATION = 'GITHUB_INTEGRATION_CC_DMND_FCAST_ML' 
   COMMENT = 'Github Repository ';

-- Fetch most recent files from Github repository
ALTER GIT REPOSITORY GITHUB_REPO_DMND_FCAST_ML FETCH;

-- Copy notebook into snowflake configure runtime settings
CREATE OR REPLACE NOTEBOOK CC_DMND_FCAST_ML_DB.MLOPS_SCHEMA.TRAIN_DEPLOY_MONITOR_ML
FROM '@CC_DMND_FCAST_ML_DB.MLOPS_SCHEMA.GITHUB_REPO_DMND_FCAST_ML/branches/master/' 
MAIN_FILE = 'demand_forecasting_ML.ipynb' QUERY_WAREHOUSE = CC_DMND_FCAST_WH;

--alter NOTEBOOK CC_DMND_FCAST_ML_DB.MLOPS_SCHEMA.TRAIN_DEPLOY_MONITOR_ML set EXTERNAL_ACCESS_INTEGRATIONS = ( 'mlops_pypi_access_integration' )

--DONE! Now you can access your newly created notebook with your CC_DMND_FCAST_RL and run through the end-to-end workflow!

GRANT USAGE ON DATABASE CC_DMND_FCAST_ML_DB to ROLE ACCOUNTADMIN;
GRANT USAGE ON SCHEMA MLOPS_SCHEMA to ROLE ACCOUNTADMIN;