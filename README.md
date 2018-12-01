# Ansible Role: bigip_to_ansible

Performs steps needed to convert a BIG-IP QKView into a series of Ansible playbooks that
can reconstruct the BIG-IP configuration.

## Goals of this role

This process will not be perfect, but we’re not aiming for perfect. We want to get “close”,
or put a significant amount of the work behind us by leveraging software.

We realize this cannot realistically be an automated process. There are some things that are
just simply not stored in BIG-IP configs (like passwords and things).

We’re ok with that. We want to turn weeks/months of manual conversion into (at best) a single
day’s worth of conversion.

## Limitations

This role is a bit of art mixed with a bit of science. It is not, and will never be, able
to completely reproduce a BIG-IP configuration perfectly. This is because of the many known
limitations of this process. Including,

* Passwords are not stored in configs
* Some things may be stored in an encrypted form
* Not all configuration is represented as files (such as ASM policies)
* Some settings and parameters are not supported by Ansible
* Depending on the environment, extra tools and apps may be installed that are not
  represented in an F5 config and we would have no way to know what those are
* Data groups may not be available
* iApps are a whole big problem because their deployed configuration is only identifiable
  by custom resource names. It would be nearly impossible to reproduce an iApp and the
  associated config.
* Commands may change across versions (although we can probably handle this case, albeit
  with more logic in the role).
* Inputs in BIG-IP configuration do not always cleanly map to Ansible parameters.


## Requirements

None.

## Role Variables

Available variables are listed below. For their default values, see `defaults/main.yml`:

    bigip_to_ansible_output_path: /tmp/qkview

The directory where you want to write configuration to. If the directory already exists,
it will be used as the destination of created files. Multiple devices in a playbook which
use this role will correctly create separate host vars and hosts in inventory.

    bigip_to_ansible_qkview:

The QKView to parse for configuration. You can provide separate QKViews if you organize
your playbook accordingly. For a reference example, view the Example Playbook example
below.

## Dependencies

* You must have an existing QKView created and located on your Ansible controller.
* Ansible must be able to write to the output location you specify to the role.

## Simple Example Playbook

    - name: Convert a qkview to a set of Ansible playbooks
      hosts: bigip
      roles:
        - role: f5devcentral.bigip_to_ansible
          bigip_to_ansible_qkview: /path/to/localhost.localdomain.qkview

## Download qkviews from many BIG-IPs and write configs to a single location

    - name: Convert a qkview to a set of Ansible playbooks
      hosts: bigips
      
      tasks:
        - name: Download qkview
          bigip_qkview:
            dest: "/tmp/{{ inventory_hostname }}.qkview"
            provider:
              server: "{{ ansible_host }}"
              server_port: 443
              user: admin
              password: secret
              validate_certs: no

        - name: Extract configuration to Ansible playbooks
          import_role:
            name: f5devcentral.bigip_to_ansible
          vars:
              bigip_to_ansible_qkview: "/tmp/{{ inventory_hostname }}.qkview"

## License

Apache

## Author Information

This role was created in 2018 by [Tim Rupp](https://github.com/caphrim007)
