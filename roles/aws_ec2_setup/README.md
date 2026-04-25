# AWS EC2 Setup

Generate reusable AWS EC2 launch templates and matching Ansible
inventory templates for multiple instance profiles.

## Overview

This role renders per-profile files so you can quickly launch a chosen
instance type with AWS CLI and then run Ansible against that host.

Generated files per profile:

- `<name>-instance.yaml` for:
  `aws ec2 run-instances --cli-input-yaml ...`
- `hosts-<name>.yml` inventory template with placeholders for host IP

## Requirements

- Ubuntu noble (24.04) or resolute (26.04)
- Ansible 2.15+
- AWS CLI installed where you plan to run launch commands

## Role Variables

Defaults come from `defaults/main.yml`.

```yaml
aws_ec2_setup_output_dir: "{{ ansible_env.HOME }}/Projects/aws-ec2-templates"

aws_ec2_setup_default_region: us-east-1
aws_ec2_setup_default_ami_id: ami-REPLACE_WITH_UBUNTU_NOBLE_AMI
aws_ec2_setup_default_key_name: REPLACE_WITH_KEYPAIR_NAME
aws_ec2_setup_default_security_group_ids:
  - sg-REPLACE_WITH_SSH_SECURITY_GROUP
aws_ec2_setup_default_subnet_id: subnet-REPLACE_WITH_SUBNET_ID
aws_ec2_setup_default_iam_instance_profile_name: >-
  REPLACE_WITH_OPTIONAL_INSTANCE_PROFILE
aws_ec2_setup_default_root_volume_size: 200
aws_ec2_setup_default_root_volume_type: gp3
aws_ec2_setup_default_owner_tag: REPLACE_WITH_OWNER
aws_ec2_setup_default_availability_zone: ""

aws_ec2_setup_instance_profiles:
  - name: g4ad-rocm-xio
    instance_type: g4ad.xlarge
    project_tag: rocm-xio
    inventory_group: aws_g4
    ansible_user: ubuntu
    username: ubuntu
```

Each profile can override defaults with optional keys:

- `region`
- `ami_id`
- `key_name`
- `security_group_ids`
- `subnet_id`
- `iam_instance_profile_name`
- `root_volume_size`
- `root_volume_type`
- `owner_tag`
- `availability_zone`

## Example Playbook

```yaml
---
- name: Generate EC2 template files
  hosts: local
  gather_facts: true
  roles:
    - role: sbates130272.batesste.aws_ec2_setup
```

## Generated Output Example

After running the role, launch one profile:

```bash
aws ec2 run-instances \
  --region us-east-1 \
  --cli-input-yaml \
  file://~/Projects/aws-ec2-templates/g4ad-rocm-xio-instance.yaml
```

Then update generated inventory:

```yaml
# ~/Projects/aws-ec2-templates/hosts-g4ad-rocm-xio.yml
all:
  children:
    aws_g4:
      hosts:
        g4ad-rocm-xio:
          ansible_host: REPLACE_WITH_PUBLIC_IP_OR_DNS
          ansible_user: ubuntu
      vars:
        username: ubuntu
```

## Testing

From this role directory:

```bash
ANSIBLE_ROLES_PATH=../ ansible-playbook \
  -i ./hosts-aws-ec2-setup \
  ./tests/test.yml
```
