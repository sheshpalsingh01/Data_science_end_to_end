# Student Performance Prediction

A Flask web app that predicts a student's math score from their demographic and
reading/writing information. The app uses the trained model and preprocessor in
`artifacts/`.

## Run locally with Docker

From this directory, build and start the app:

```sh
docker build -t student-performance .
docker run --rm -p 8080:8080 student-performance
```

Open [http://localhost:8080](http://localhost:8080).

The image requires both trained artifacts:

- `artifacts/model.pkl`
- `artifacts/preprocessor.pkl`

## CI and deployment

GitHub Actions runs CI on pushes and pull requests. CI builds the Docker image
and checks the app and prediction form. After CI succeeds, pushes to `main`
also publish the image to Google Artifact Registry and deploy it to Google
Cloud Run.

The Cloud Run service is configured for public access. Anyone with its URL can
submit predictions.

### 1. Prepare Google Cloud

Install and authenticate the [Google Cloud CLI](https://cloud.google.com/sdk/docs/install).
Select a Google Cloud project with billing enabled, and set these values:

```sh
PROJECT_ID=your-project-id
REGION=us-central1

gcloud config set project "$PROJECT_ID"
gcloud services enable \
  artifactregistry.googleapis.com \
  run.googleapis.com \
  iamcredentials.googleapis.com \
  sts.googleapis.com
gcloud artifacts repositories create student-performance \
  --repository-format=docker \
  --location="$REGION"
```

Create separate identities for GitHub Actions and the running service:

```sh
DEPLOYER_SA=github-deployer
RUNTIME_SA=student-performance-runtime

gcloud iam service-accounts create "$DEPLOYER_SA"
gcloud iam service-accounts create "$RUNTIME_SA"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${DEPLOYER_SA}@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role=roles/run.admin
gcloud artifacts repositories add-iam-policy-binding student-performance \
  --location="$REGION" \
  --member="serviceAccount:${DEPLOYER_SA}@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role=roles/artifactregistry.writer
gcloud iam service-accounts add-iam-policy-binding \
  "${RUNTIME_SA}@${PROJECT_ID}.iam.gserviceaccount.com" \
  --member="serviceAccount:${DEPLOYER_SA}@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role=roles/iam.serviceAccountUser
```

### 2. Configure GitHub Workload Identity Federation

Replace the example GitHub values with the account or organization and
repository containing this project:

```sh
PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" \
  --format='value(projectNumber)')
GITHUB_OWNER=your-github-owner
GITHUB_REPOSITORY=your-repository-name
POOL_ID=github-actions
PROVIDER_ID=github

gcloud iam workload-identity-pools create "$POOL_ID" \
  --location=global \
  --display-name="GitHub Actions"
gcloud iam workload-identity-pools providers create-oidc "$PROVIDER_ID" \
  --location=global \
  --workload-identity-pool="$POOL_ID" \
  --display-name="GitHub main branch" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
  --attribute-condition="assertion.repository == '${GITHUB_OWNER}/${GITHUB_REPOSITORY}' && assertion.ref == 'refs/heads/main'"
gcloud iam service-accounts add-iam-policy-binding \
  "github-deployer@${PROJECT_ID}.iam.gserviceaccount.com" \
  --role=roles/iam.workloadIdentityUser \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL_ID}/attribute.repository/${GITHUB_OWNER}/${GITHUB_REPOSITORY}"
```

In the GitHub repository, open **Settings → Secrets and variables → Actions →
Variables** and add:

| Variable | Value |
| --- | --- |
| `GCP_PROJECT_ID` | Your Google Cloud project ID |
| `GCP_REGION` | The Artifact Registry region, for example `us-central1` |
| `GCP_ARTIFACT_REGISTRY_REPOSITORY` | `student-performance` |
| `GCP_WIF_PROVIDER` | `projects/PROJECT_NUMBER/locations/global/workloadIdentityPools/github-actions/providers/github` |
| `GCP_WIF_SERVICE_ACCOUNT` | `github-deployer@PROJECT_ID.iam.gserviceaccount.com` |
| `GCP_CLOUD_RUN_RUNTIME_SERVICE_ACCOUNT` | `student-performance-runtime@PROJECT_ID.iam.gserviceaccount.com` |

Replace `PROJECT_NUMBER` and `PROJECT_ID` in the variable values with your
actual values. No service-account key or other long-lived Google credential is
needed.

### 3. Push the model files and deploy

Make sure the model artifacts are committed; they are required by the CI build:

```sh
git add artifacts/model.pkl artifacts/preprocessor.pkl
git commit -m "Add trained model artifacts"
git push origin main
```

The workflow deploys after CI passes. Find the Cloud Run service URL in the
deployment step's logs.
