# GCP AI OPS

## A variety of GCP related OPS services powered by VertexAI

### See it in action [here](https://gcpaiops.xyz/)

### Supported Operations
* Run the prompt.
* Create a gCloud CLI command.
* Create a terraform template.
* Inspect existing IaC code for security issues.
* Convert AWS TF to GCP equivalent.

### How to use
* Execute run-venv.sh to run the code locally.
    * Once the UI is running, enter your project id in the side bar
* Deploy to Cloud Run
    * Modify deploy.sh:
        * Replace SERVICE_ACCOUNT_EMAIL with your own service account. 
            * The service account should have _Cloud Run Invoker_ and _Vertex AI User_ permissions.
        * Replace ARTIFACT_REGISTRY_NAME with your own. (The repository should already exist.)
        * Replace GOOGLE_CLOUD_PROJECT with your own.
        * Note the allow-unauthenticated and ingress settings.
    * Execute deploy.sh to deploy the code to Cloud Run.
