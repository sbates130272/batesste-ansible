#!/usr/bin/env python3
"""
Generate GitHub Actions workflow files for each Ansible role with tests.

This script scans the roles directory for roles that have a tests/ subdirectory
and generates individual workflow files for each one.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, List, Optional

# Configuration for role-specific settings
ROLE_CONFIGS = {
    "rocm_setup": {
        "ubuntu_versions": ["24.04"],
        "free_disk_space": True,
        "extra_vars": {
            "rocm_setup_wsl_install": False,
            "rocm_setup_rocm_version": "latest",
            "rocm_setup_amdgpu_version": "latest",
            "rocm_setup_run_checks": False,
            "rocm_setup_install_metrics_exporter": False,
        },
        "verification_commands": [
            "systemctl status amdgpu-dkms || true",
            "dpkg -l | grep rocm || true",
        ],
        "needs_vault": True,
    },
    "grafana_setup": {
        "ubuntu_versions": ["24.04"],
        "free_disk_space": False,
        "extra_vars": {
            "vault_grafana_setup_password": "test_ci_password_123",
            "grafana_setup_discover_node_exporters": False,
            "grafana_setup_discover_amd_gpu_exporters": False,
        },
        "verification_commands": [
            "systemctl status grafana-server || true",
            "systemctl status prometheus || true",
            "systemctl status prometheus-node-exporter || true",
            "curl -s http://localhost:3000/api/health || true",
            "curl -s http://localhost:9090/-/healthy || true",
            "curl -s http://localhost:9100/metrics | head -10 || true",
        ],
        "needs_vault": True,
    },
    "rdma_setup": {
        "ubuntu_versions": ["24.04"],
        "free_disk_space": False,
        "extra_vars": {},
        "verification_commands": [
            "dpkg -l | grep rdma || true",
            "ls -la /usr/bin/*ibv* || true",
        ],
        "needs_vault": False,
    },
    "git_setup": {
        "ubuntu_versions": ["24.04"],
        "free_disk_space": False,
        "extra_vars": {
            "git_setup_enable_gpg_signing": False,
            "git_setup_gh_authenticate": True,
        },
        "verification_commands": [
            "git --version",
            "gh --version",
            "git config --global --list",
            "gh auth status || true",
        ],
        "needs_vault": False,
        "needs_github_token": True,
    },
    "github_runner": {
        "ubuntu_versions": ["24.04"],
        "free_disk_space": False,
        "extra_vars": {
            "github_runner_url": "https://github.com/sbates130272/batesste-ansible",
            "github_runner_token": "",  # Token not available in CI, test will skip
        },
        "verification_commands": [
            "id github-runner || true",
            "ls -la /opt/github-runner || true",
            "systemctl status github-runner || true",
        ],
        "needs_vault": False,
        "needs_github_token": False,
    },
    "mutt_setup": {
        "ubuntu_versions": ["24.04"],
        "free_disk_space": False,
        "extra_vars": {},
        "verification_commands": [
            "mutt -v | head -5",
            "ls -la ~/.mutt/ || true",
            "ls -la ~/.mutt/scripts/mutt_oauth2.py || true",
            "ls -la ~/.mutt/tokens/ || true",
        ],
        "needs_vault": True,
        "needs_github_token": False,
    },
}

# Default configuration for roles without specific config
DEFAULT_CONFIG = {
    "ubuntu_versions": ["24.04"],
    "free_disk_space": False,
    "extra_vars": {},
    "verification_commands": [],
    "needs_vault": False,
}


def find_roles_with_tests(roles_dir: Path) -> List[str]:
    """Find all roles that have a tests directory."""
    roles = []
    for role_path in roles_dir.iterdir():
        if role_path.is_dir() and (role_path / "tests").exists():
            roles.append(role_path.name)
    return sorted(roles)


def generate_workflow_yaml(role_name: str, config: Dict) -> str:
    """Generate a GitHub Actions workflow YAML string for a role."""
    
    ubuntu_versions = config.get("ubuntu_versions", ["24.04"])
    use_matrix = len(ubuntu_versions) > 1
    
    # Header
    lines = [
        f"name: {role_name} CI",
        "'on':",
        "  workflow_dispatch: {}",
        "  pull_request:",
        "    branches:",
        "      - main",
        "    paths:",
        f"      - roles/{role_name}/**",
        "      - .github/workflows/**",
        "      - requirements.txt",
        "      - requirements.yml",
        "  push:",
        "    branches:",
        "      - main",
        "    paths:",
        f"      - roles/{role_name}/**",
        "",
        "jobs:",
        f"  {role_name}-test:",
    ]
    
    # Add matrix or single runner
    if use_matrix:
        lines.append("    strategy:")
        lines.append("      matrix:")
        lines.append("        runs-on:")
        for version in ubuntu_versions:
            lines.append(f"          - ubuntu-{version}")
        lines.append("    runs-on: ${{ matrix.runs-on }}")
    else:
        lines.append(f"    runs-on: ubuntu-{ubuntu_versions[0]}")
    
    lines.append("    steps:")
    
    # Add free disk space step if needed
    if config.get("free_disk_space", False):
        lines.extend([
            "      - name: Free Disk Space (Ubuntu)",
            "        uses: jlumbroso/free-disk-space@v1.3.1",
        ])
    
    # Standard setup steps
    lines.extend([
        "      - name: Checkout code",
        "        uses: actions/checkout@v4.2.2",
        "",
        "      - name: Install pip packages",
        "        run: python3 -m pip install -r requirements.txt",
        "",
        "      - name: Run ansible-galaxy to install collections and roles",
        "        run: ansible-galaxy install -r requirements.yml",
        "",
        "      - name: Create an SSH keypair",
        '        run: mkdir -p .ssh && ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_rsa -q -N ""',
        "",
        "      - name: Create a GNU PGP folder",
        "        run: mkdir -p .gnupg",
        "",
    ])
    
    # Create hosts file
    hosts_content = {
        "all": {
            "hosts": {
                "localhost": {
                    "ansible_connection": "local",
                    "ansible_user": "runner",
                }
            }
        }
    }
    hosts_content["all"]["hosts"]["localhost"].update(config.get("extra_vars", {}))
    hosts_yaml = yaml.dump(hosts_content, default_flow_style=False, sort_keys=False)
    
    lines.extend([
        "      - name: Write hosts-ci file",
        "        uses: DamianReeves/write-file-action@v1.3",
        "        with:",
        f"          path: ./roles/{role_name}/hosts-ci",
        "          write-mode: overwrite",
        "          contents: |",
    ])
    
    # Add hosts content with proper indentation
    for line in hosts_yaml.splitlines():
        lines.append(f"            {line}")
    
    lines.append("")
    
    # Run test playbook
    lines.extend([
        "      - name: Run the test playbook against the local runner",
        "        run: ansible-playbook -v -i hosts-ci ./tests/test.yml",
        f"        working-directory: ./roles/{role_name}",
        "        env:",
        "          ANSIBLE_ROLES_PATH: ${{ github.workspace }}/roles",
    ])
    
    # Add vault password if needed
    if config.get("needs_vault", False):
        lines.extend([
            "          ANSIBLE_VAULT_PASSWORD_FILE: ${{ github.workspace }}/playbooks/vault-env",
            "          ANSIBLE_VAULT_PASSWORD: ${{ secrets.ANSIBLE_VAULT_PASSWORD }}",
        ])
    
    # Add GitHub token if needed
    if config.get("needs_github_token", False):
        lines.append("          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}")
    
    # Add verification commands if any
    if config.get("verification_commands"):
        lines.extend([
            "",
            f"      - name: Verify {role_name} installation",
            "        run: |",
        ])
        for cmd in config["verification_commands"]:
            lines.append(f"          {cmd}")
    
    return "\n".join(lines) + "\n"


def generate_workflow(role_name: str, config: Dict) -> Dict:
    """Generate a GitHub Actions workflow configuration for a role."""
    
    workflow = {
        "name": f"{role_name} CI",
        "on": {
            "workflow_dispatch": None,
            "pull_request": {
                "branches": ["main"],
                "paths": [
                    f"roles/{role_name}/**",
                    ".github/workflows/**",
                    "requirements.txt",
                    "requirements.yml",
                ],
            },
            "push": {
                "branches": ["main"],
                "paths": [
                    f"roles/{role_name}/**",
                ],
            },
        },
        "jobs": {
            f"{role_name}-test": {
                "runs-on": f"ubuntu-{config['ubuntu_versions'][0]}",
                "steps": []
            }
        }
    }
    
    steps = workflow["jobs"][f"{role_name}-test"]["steps"]
    
    # Add free disk space step if needed
    if config.get("free_disk_space", False):
        steps.append({
            "name": "Free Disk Space (Ubuntu)",
            "uses": "jlumbroso/free-disk-space@v1.3.1"
        })
    
    # Standard setup steps
    steps.extend([
        {
            "name": "Checkout code",
            "uses": "actions/checkout@v4.2.2"
        },
        {
            "name": "Install pip packages",
            "run": "python3 -m pip install -r requirements.txt"
        },
        {
            "name": "Run ansible-galaxy to install collections and roles",
            "run": "ansible-galaxy install -r requirements.yml"
        },
        {
            "name": "Create an SSH keypair",
            "run": 'mkdir -p .ssh && ssh-keygen -b 2048 -t rsa -f ~/.ssh/id_rsa -q -N ""'
        },
        {
            "name": "Create a GNU PGP folder",
            "run": "mkdir -p .gnupg"
        },
    ])
    
    # Create hosts file
    hosts_content = {
        "all": {
            "hosts": {
                "localhost": {
                    "ansible_connection": "local",
                    "ansible_user": "runner",
                }
            }
        }
    }
    
    # Add extra vars to localhost
    hosts_content["all"]["hosts"]["localhost"].update(config.get("extra_vars", {}))
    
    steps.append({
        "name": "Write hosts-ci file",
        "uses": "DamianReeves/write-file-action@v1.3",
        "with": {
            "path": f"./roles/{role_name}/hosts-ci",
            "write-mode": "overwrite",
            "contents": yaml.dump(hosts_content, default_flow_style=False)
        }
    })
    
    # Run test playbook
    run_test_step = {
        "name": "Run the test playbook against the local runner",
        "run": "ansible-playbook -v -i hosts-ci ./tests/test.yml",
        "working-directory": f"./roles/{role_name}",
        "env": {
            "ANSIBLE_ROLES_PATH": "${{ github.workspace }}/roles"
        }
    }
    
    # Add vault password if needed
    if config.get("needs_vault", False):
        run_test_step["env"]["ANSIBLE_VAULT_PASSWORD_FILE"] = "${{ github.workspace }}/playbooks/vault-env"
        run_test_step["env"]["ANSIBLE_VAULT_PASSWORD"] = "${{ secrets.ANSIBLE_VAULT_PASSWORD }}"
    
    steps.append(run_test_step)
    
    # Add verification commands if any
    if config.get("verification_commands"):
        steps.append({
            "name": f"Verify {role_name} installation",
            "run": "\\n".join(config["verification_commands"])
        })
    
    # Add matrix strategy if multiple Ubuntu versions
    if len(config.get("ubuntu_versions", [])) > 1:
        workflow["jobs"][f"{role_name}-test"]["strategy"] = {
            "matrix": {
                "runs-on": [f"ubuntu-{v}" for v in config["ubuntu_versions"]]
            }
        }
        workflow["jobs"][f"{role_name}-test"]["runs-on"] = "${{ matrix.runs-on }}"
    
    return workflow


def main():
    """Main function to generate all workflow files."""
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    roles_dir = repo_root / "roles"
    workflows_dir = script_dir / "workflows"
    
    print("Scanning for roles with tests...")
    roles = find_roles_with_tests(roles_dir)
    
    if not roles:
        print("No roles with tests found!")
        return
    
    print(f"Found {len(roles)} roles with tests: {', '.join(roles)}")
    
    for role_name in roles:
        config = ROLE_CONFIGS.get(role_name, DEFAULT_CONFIG)
        workflow_content = generate_workflow_yaml(role_name, config)
        
        # Write workflow file
        workflow_file = workflows_dir / f"{role_name}-ci.yml"
        print(f"Generating {workflow_file}...")
        
        with open(workflow_file, 'w') as f:
            f.write("# AUTO-GENERATED FILE - DO NOT EDIT MANUALLY\n")
            f.write(f"# Generated by generate-workflows.py for role: {role_name}\n")
            f.write("# To regenerate: python3 .github/generate-workflows.py\n\n")
            f.write(workflow_content)
        
        print(f"  ✓ Created {workflow_file}")
    
    print(f"\nGenerated {len(roles)} workflow files successfully!")
    print(f"\nWorkflow files created in: {workflows_dir}")


if __name__ == "__main__":
    main()

