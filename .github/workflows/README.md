# GitHub Actions CI/CD Workflows

This directory contains the CI/CD workflows for the To-Do application.

## Workflows

### 1. CI - Tests (`ci.yml`)

**Triggers:**
- Pull requests to `main` or `dev` branches
- Pushes to `main`, `dev`, or `feature/**` branches

**Jobs:**
- **Test**: Runs all unit tests with coverage reporting
  - Installs Python dependencies
  - Runs pytest with coverage
  - Uploads coverage to Codecov (optional)
- **Lint**: Checks code quality
  - Runs flake8 for syntax and style issues
  - Checks code formatting with black

### 2. CD - Build and Deploy (`cd.yml`)

**Triggers:**
- Pushes to `main` branch
- Version tags (`v*`)
- Manual workflow dispatch

**Jobs:**
- **Build**: Builds and tests Docker image
  - Sets up Docker Buildx
  - Builds the Docker image
  - Tests the image by running a container
  - Pushes to Docker Hub (if secrets are configured)
- **Deploy**: Deployment notification
  - Confirms successful build and deployment

## Setup

### Required Secrets

To enable full CI/CD functionality, add the following secrets in your GitHub repository settings:

1. **For Docker Hub (CD workflow):**
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub password or access token

2. **For Codecov (CI workflow - optional):**
   - `CODECOV_TOKEN`: Your Codecov repository token

### Adding Secrets

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret with its corresponding value

## Workflow Status

You can view the status of workflows:
- In the **Actions** tab of your repository
- As status checks on pull requests
- In commit status badges

## Local Testing

Before pushing, you can test locally:

```bash
# Run tests
cd app
pip install -r requirements.txt
pip install pytest pytest-cov flake8 black
pytest

# Check code quality
flake8 .
black --check .

# Build Docker image
docker build -t todo-app:test -f Dockerfile .
docker run -p 5000:5000 todo-app:test
```

## Customization

To customize the workflows:
- Edit the YAML files in `.github/workflows/`
- Modify the triggers, jobs, or steps as needed
- Add additional checks or deployment targets

## Troubleshooting

### Tests Failing
- Check the test output in the Actions tab
- Run tests locally to debug
- Ensure all dependencies are in requirements.txt

### Docker Build Failing
- Verify Dockerfile syntax
- Check that all required files are present
- Test Docker build locally

### Secrets Not Working
- Verify secrets are added in repository settings
- Check secret names match exactly in workflow files
- Ensure you have necessary permissions
