# Contributing to Ansible Splunk Enterprise

Thank you for your interest in contributing to this project. This document
provides guidelines and information for contributors.

## Development Setup

### Prerequisites

- [Nix](https://nixos.org/) with flakes enabled
- [direnv](https://direnv.net/) (recommended — activates the dev shell automatically)
- Docker (for molecule tests)
- Access to Doppler secrets (for integration testing)

### Local Environment Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/JacobPEvans/ansible-splunk.git
   cd ansible-splunk
   ```

2. Activate the nix dev shell (provides `ansible-playbook`, `ansible-lint`, `molecule`, etc.):

   ```bash
   direnv allow   # if using direnv (recommended) — activates nix-devenv#ansible-apps automatically
   # or: nix develop github:JacobPEvans/nix-devenv#ansible-apps
   ```

3. Install pre-commit hooks:

   ```bash
   pre-commit install
   ```

4. Install Ansible collections:

   ```bash
   ansible-galaxy collection install -r requirements.yml
   ```

## Testing

### Syntax Validation

```bash
ansible-playbook playbooks/deploy.yml --syntax-check
ansible-playbook playbooks/configure_indexes.yml --syntax-check
ansible-playbook playbooks/validate.yml --syntax-check
```

### Linting

```bash
yamllint .
ansible-lint playbooks/ roles/
```

### Molecule Tests

Run the full molecule test suite:

```bash
molecule test
```

Run individual test stages:

```bash
molecule converge  # Create container and run role
molecule verify    # Run verification tests
molecule destroy   # Clean up test container
```

### Integration Testing

For testing against a real Proxmox VM:

1. Sync Terraform inventory:

   ```bash
   ./scripts/sync-terraform-inventory.sh
   ```

2. Run playbooks with Doppler:

   ```bash
   doppler run -- ansible-playbook playbooks/deploy.yml
   doppler run -- ansible-playbook playbooks/configure_indexes.yml
   doppler run -- ansible-playbook playbooks/validate.yml
   ```

## Code Style

### YAML Files

- Use 2-space indentation
- Use FQCN (Fully Qualified Collection Names) for all modules
- Add `---` document start marker to all YAML files
- Keep lines under 120 characters

### Task Naming

- Use descriptive task names that explain what the task does
- Start task names with a verb (e.g., "Install", "Configure", "Create")
- Use sentence case (capitalize first word only)

### Example

```yaml
- name: Install required packages
  ansible.builtin.apt:
    name: "{{ item }}"
    state: present
  loop:
    - curl
    - gnupg
```

## Making Changes

### Branch Naming

Use conventional branch naming:

- `feature/<description>` - New functionality
- `bugfix/<description>` - Resolve identified issues
- `hotfix/<description>` - Critical or urgent patches
- `release/<description>` - Prepare version releases
- `chore/<description>` - Maintenance tasks (build process, dependencies, tooling)

### Commit Messages

Follow conventional commit format:

```text
type: short description

Longer description if needed.

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

### Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Run all tests locally (lint, molecule)
4. Push to your fork
5. Create a pull request with a clear description

## Adding New Indexes

To add a new index to the default configuration:

1. Edit `roles/splunk_docker/defaults/main.yml`
2. Add the index to the `splunk_docker_indexes` list
3. Test with molecule
4. Update documentation if significant

## Adding Technology Add-ons

To add a new TA:

1. Place the `.tar` or `.tgz` file in `roles/splunk_docker/files/`
2. Add the entry to `splunk_docker_addons` in `defaults/main.yml`
3. Re-run the playbook

## Questions?

If you have questions about contributing, please open a GitHub issue.
