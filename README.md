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
* Reproducing complicated BIG-IPs is...complicated. The BIG-IP supports thousands of different
  resource types and this role does not cover all possible resources.

## What can be converted

The following resources can all be **partially** recreated with this role.

* LTM pools
* LTM pool members
* LTM virtual servers
* LTM http monitors
* LTM https monitors
* LTM iRules (the rule only, not the content of the rule)
* LTM tcp monitors
* Provisioned modules (GTM, ASM, AFM) and their level
* VLANs

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

## Output files

Once the role has finished, the generated Ansible playbooks can be found, by
default, in ``/tmp/qkview/results``. This path can be changed using the
``bigip_to_ansible_output_path`` role variable.

Output files will consist of a number of Ansible specific files, as well as
a number of temporary files. A snippet of what will be created is shown below.

```bash
qkview/
├── assemble
│   ├── instance-host-vars.yaml
│   ├── instance-ltm-http-monitor.yaml
│   ├── instance-ltm-https-monitor.yaml
│   ├── instance-ltm-irule.yaml
│   ├── instance-ltm-pool-member.yaml
│   ├── instance-ltm-pool.yaml
│   ├── instance-ltm-tcp-monitor.yaml
│   ├── instance-ltm-virtual-server.yaml
│   └── instance-sys-provision.yaml
├── extract
│   ├── HWINFO
    ├── ...lots of files here. Everything that was in qkview
└── result
    ├── files
    │   ├── instance--Common-ASM_Bot_Header-ltm-irule.yaml
    │   ├── instance--Common-ASM_IP_Blacklist-ltm-irule.yaml
    │   ├── instance--Common-ASM_Logger-ltm-irule.yaml
    │   ├── instance--Common-LOG_TEST_IRULE2-ltm-irule.yaml
    │   ├── ... other static files and things
    ├── inventory
    │   ├── host_vars
    │   │   └── instance.yaml
    │   └── hosts
    └── playbook.yaml
```

The items found in the ``result`` directory are most relevant and the entire
``result`` folder can be moved somewhere, or its content relocated to your SCM
of choice.

## About secure/sensitive settings

No cleartext passwords or other sensitive settings are reflected in the generated
Ansible configs. To the extent that any of these items **could** be, is limited by
BIG-IP itself as it does **not** keep sensitive information in a QKView.

## Running the generated output

To reproduce on your BIG-IP the partial configuration that this role creates, do the
following

- Edit the /tmp/qkview/result/inventory/host_vars/HOSTNAME.yaml file where ``HOSTNAME``
  is the hostname (according to ``tmsh show cm device``) of the BIG-IP.
- At the top of this file is a series of ``provider`` information that has been stubbed
  for you.
- It likely includes your BIG-IP's management address specified in the ``server`` param.
  Change this as necessary
- Change the ``user``, ``password``, and ``server_port`` as needed
- Once the above is complete, save the file.

You can now run the playbook that is included in the ``result`` directory

```bash
$> cd /tmp/qkview/result
$> ansible-playbook -i inventory/hosts playbook.yaml
```

As can be done with normal Ansible playbooks, you can additionally limit the execution
of the playbook to the hosts that you are interested in by using the ``--limit-to``
argument to ``ansible-playbook``.

## License

Apache

## Author Information

This role was created in 2018 by [Tim Rupp](https://github.com/caphrim007)
