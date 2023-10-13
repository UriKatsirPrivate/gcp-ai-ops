# GCP AI OPS

## A variety of GCP related OPS services powered by VertexAI

### See it in action [here](https://gcpaiops.xyz/)

### Supported Operations
* Improve prompt.
* Inspect a prompt for security issues.
* Run the prompt.
* Create a gCloud CLI command.
* Create a terraform template.
* Inspect existing IaC code for security issues.
* Convert AWS TF to GCP equivalent.
* Image Generation.

### How to use
* Modify app.py:
  * Replace _PROJECT_ID_ with your project ID. 
* Modify deploy.sh:
    * Replace SERVICE_ACCOUNT_EMAIL with your own service account. 
      * The service account should have _Cloud Run Invoker_ and _Vertex AI User_ permissions.
    * Replace ARTIFACT_REGISTRY_NAME with your own.
    * Replace GOOGLE_CLOUD_PROJECT with your own.
    * Replace SERVICE_NAME with your own.
* Execute _run-venv.sh_ to run the code locally.
* Execute _deploy.sh_ to deploy the code to Cloud Run.
* When the service is running, modify values in the side bar for model name, max token output etc.

#### To-Do
