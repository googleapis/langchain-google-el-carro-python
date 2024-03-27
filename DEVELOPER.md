# DEVELOPER.md

## Versioning

This library follows [Semantic Versioning](http://semver.org/).

## Processes

### Conventional Commit messages

This repository uses tool [Release Please](https://github.com/googleapis/release-please) to create GitHub and PyPi releases. It does so by parsing your
git history, looking for [Conventional Commit messages](https://www.conventionalcommits.org/),
and creating release PRs.

Learn more by reading [How should I write my commits?](https://github.com/googleapis/release-please?tab=readme-ov-file#how-should-i-write-my-commits)

## Testing

### Run tests locally

1. Set env vars: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`

1. Run pytest to automatically run all tests:

    ```bash
    pytest
    ```

### CI Platform Setup

Cloud Build is used to run tests against Google Cloud resources in test project: prow-build-graybox.
Each test has a corresponding Cloud Build trigger, see [all triggers][triggers].
These tests are registered as required tests in `.github/sync-repo-settings.yaml`.

#### Trigger Setup

Cloud Build triggers (for Python versions 3.8 to 3.11) were created with the following specs:

```YAML
name: integration-test-pr-py38
description: Run integration tests on PR for Python 3.8
filename: integration.cloudbuild.yaml
github:
  name: langchain-google-firestore-python
  owner: googleapis
  pullRequest:
    branch: .*
    commentControl: COMMENTS_ENABLED_FOR_EXTERNAL_CONTRIBUTORS_ONLY
ignoredFiles:
  - docs/**
  - .kokoro/**
  - .github/**
  - "*.md"
substitutions:
  _VERSION: "3.8"
  _DB_HOST: <>
  _DB_PORT: <>
  _DB_NAME: <>
  _DB_USER: <>
```

Use `gcloud builds triggers import --source=trigger.yaml` create triggers via the command line

#### Project Setup

1. Create an GKE Cluster with El Carro database
1. Setup Cloud Build triggers (above)

#### Run tests with Cloud Build

* Run integration test:

    ```bash
    gcloud builds submit --config integration.cloudbuild.yaml --substitutions=,_DB_HOST=$DB_HOST,_DB_PORT=$DB_PORT,_DB_NAME=$DB_NAME,_DB_USER=$DB_USER,_DB_PASSWORD=$DB_PASSWORD
    ```

#### Trigger

To run Cloud Build tests on GitHub from external contributors, ie RenovateBot, comment: `/gcbrun`.


[triggers]: https://console.cloud.google.com/cloud-build/triggers?e=13802955&project=prow-build-graybox
