# Ansible Role: bigip_gslb

Performs steps needed to create and manage a Global Services Load Balancing (GSLB) object
on a BIG-IP DNS platform.

GSLB is also known in F5 lingo as a "Wide IP". Regardless of your terminology of choice,
this role can be used to manage different sets of GSLB configuration.

Note that the "typical" way that GSLB is deployed involves at least two serves; one running
GTM/DNS and N more running LTM (or some other supported platform). This role specifically
handles the GTM/DNS side of this configuration.

It is not necessary to have the LTM portion pre-configured, however, to make use of this
role.

## Requirements

None.

## Role Variables

Available variables are listed below. For their default values, see `defaults/main.yml`:

    provider_server: localhost
    provider_server_port: 443
    provider_user: admin
    provider_password: secret
    provider_validate_certs: no
    provider_transport: rest
    provider_timeout: 120

Establishes initial connection to your BIG-IQ. These values are substituted into
your ``provider`` module parameter.

    bigip_glsb_app_name: localhost

The name of the GSLB app being created.

    bigip_glsb_app_domain: gslb.local.com

The domain of the app being created.

    bigip_glsb_pool_lb_method: round-robin


## Dependencies

* You must have an existing QKView created and located on your Ansible controller.
* Ansible must be able to write to the output location you specify to the role.

## Example Playbook

    - name: Convert a qkview to a set of Ansible playbooks
      hosts: bigip
      roles:
        - role: f5devcentral.bigip_to_ansible
          qkview: /path/to/localhost.localdomain.qkview

## License

Apache

## Author Information

This role was created in 2018 by [Tim Rupp](https://github.com/caphrim007)
