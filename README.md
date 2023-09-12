# GCP AI OPS

## Variety of GCP related OPS services powered by VertexAI

### See it in action [here](https://gcpaiops.cloud/)

### Supported Operations
* Improve prompt.
* Inspect a prompt for security issues.
* Create a gCloud CLI 
* Create a terraform template

### How to use
* Modify app.py:
  * Replace project_id with your project ID. 
* Modify deploy.sh:
    * Replace SERVICE_ACCOUNT_EMAIL with your own service account. 
      * The service account should have _Cloud Run Invoker_ and _Vertex AI User_ permissions.
    * Replace ARTIFACT_REGISTRY_NAME with your own.
    * Replace GOOGLE_CLOUD_PROJECT with your own.
    * Replace SERVICE_NAME with your own.
* Execute run-venv.sh to run the code locally.
* Execute deploy.sh to deploy the code to Cloud Run.
* When the service is running, modify values in the side bar for model name, max token output etc.

#### To-Do
