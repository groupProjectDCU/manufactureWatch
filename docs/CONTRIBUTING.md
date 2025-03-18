# Development Process & Contribution Guide

This document explains how to set up the project, contribute code, and collaborate effectively with the team. **Please read it before you begin working on any task** so that our workflow remains consistent.

---

## Table of Contents
1. [Branching & Workflow](#branching--workflow)
2. [Coding Guidelines](#coding-guidelines)
3. [Code Review & Pull Requests](#code-review--pull-requests)
4. [Testing & QA](#testing--qa)
5. [Documentation](#documentation)
6. [Releases & Deployment](#releases--deployment)
7. [Support & Contact](#support--contact)

---


## Branching & Workflow
We use a simplified **GitHub Flow**:

1. **Master Branch**
    - Always in a stable state
    - Contains the latest production-ready code.
2. **Feature Branches**
    - Branch off from master (or dev if you’re using a separate integration branch).
    - Name your branch descriptively, e.g. feature/fault-case-api or bugfix/dashboard-export.
    - Example: feature/add-user-authentication
3. **Development Steps**
    - Pull the latest master to stay in sync.
	- Create your feature branch.
	- Commit changes locally with clear messages.
	- Push your branch to GitHub.
            - Open a PR from your feature branch into master.
            - Link the PR to an issue if applicable.
            - Tag relevant teammates for review.
            - Resolve feedback, rebase, and merge once approved.
5. **Merging**
    - Merge PRs into master (or dev if you’re using a separate integration branch).
    - Delete your feature branch after merging.

## GitHub Issues & Projects
- Each task or feature corresponds to a GitHub Issue.
- We use GitHub Projects (Kanban board) to track progress: To Do → In Progress → Review → Done.

---

## Coding Guidelines
1. **Python Style**
    - Follow PEP 8 for Python code.
    - Use descriptive variable names and docstrings for functions.
2. **Django Best Practices**
    - Store templates in templates/.
    - Keep static files (CSS, JS, images) in static/.
    - Separate apps (e.g., accounts, machinery, faults) for modularity.
3. **JavaScript/Front-End**
    - Use meaningful IDs/classes.
    - Validate forms before submission.
    - Keep code DRY (Don’t Repeat Yourself).
4. **Commits**
    - Write clear commit messages (use present tense, e.g., “Add user login page”).
    - Make frequent commits to capture meaningful checkpoints.
5. **Documentation**
    - Document new functions and APIs.
    - Update README.md with project details.
    - Add new documentation to the docs/ directory.
6. **Testing**
    - Write unit tests for new functions.
    - Use pytest for testing.

---

## Code Review & Pull Requests
1. **Pull Requests**
    - Provide a short summary of what the PR does.
    - Reference related issues (e.g., “Closes #123”).
    - Include screenshots or test evidence if applicable.
2. **Review Process**
    - At least one teammate should review your PR.
    - Comment on the PR with suggestions, questions, or required changes.
    - The author addresses feedback, updates the PR, and requests a follow-up review.
3. **Merging**
    - The PR can be merged once it’s approved and passes all checks (CI tests, if set up).
    - Use “Squash and merge” to keep the commit history clean.

---

## Testing & QA
1. **Automated Tests**
    - Write unit tests for Django models, views, and APIs (in each app’s tests.py or separate tests/ folder).
    - If using Pytest, place tests in tests/ directories with descriptive names.
2. **Manual Testing**
    - Before opening a PR, manually test your feature or bugfix in the browser.
    - Check different roles (Manager, Technician, Repair) to ensure permissions are correct.
3. **CI Integration (optional)**
    - We may use GitHub Actions or another CI tool to automatically run tests and lint checks.
    - Fix any test failures before merging.

---

## Documentation
1. **Inline Documentation**
    - Add docstrings to Python functions/classes.
    - Comment tricky sections of JavaScript or Django templates.
2. **Project Documentation**
    - Update the README.md or a dedicated docs/ folder if you add major features.
    - For changes to environment variables, Docker usage, or new endpoints, update relevant docs.
3. **Meeting Minutes & Changes**
    - Store meeting summaries or important decisions in docs/meeting-notes.
    - Helps new team members understand why certain decisions were made.    

---

## Releases & Deployment
1. **Staging Environment**
    - We may have a staging environment (e.g., staging.example.com) for final testing.
    - Deploy feature branches here for user acceptance testing (UAT) if needed.
2. **Production Deployment**
    - Merging into master may trigger an automatic deployment (if set up).
    - Ensure migrations run on the production DB.
    - Monitor logs for errors.
3. **Versioning**
    - Tag releases in GitHub, e.g., v1.0, v1.1, etc.
    - Update release notes in GitHub’s “Releases” section.

---

## Support & Contact
- WhatsAPP group
- Weekly Meeting: to be arranged