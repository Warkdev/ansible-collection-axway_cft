# Axway Transfer CFT Collection

This repo contains the `warkdev.axway_cft` Ansible Collection. The collection includes many modules and plugins to work with Axway Transfer CFT.

Please note that currently, only the [API version 1.1](https://apidocs.axway.com/swagger-ui-NEW/index.html?productname=transfercft&productversion=3.3.2&filename=transfercft-swagger-api.json#/) (Axway CFT v3.3.2) is supported. Later release will add newer versions of the API.

## Tested with Ansible

Tested with the current ansible-core 2.13.

## External requirements

N/A

## Included content

* httpapi plugins:
  - warkdev.axway_cft.axway_cft: use Axway Transfer CFT as remote using httpapi plugin to connect
* Modules:
  - warkdev.axway_cft.axway_cft_about_info: retrieves info about the current Transfer CFT product
  - warkdev.axway_cft.axway_cft_logs: retrieves logs about the current Transfer CFT product
  - warkdev.axway_cft.axway_transfer_info: retrieves info about a given transfer
  - warkdev.axway_cft.axway_transfer: manages transfer lifecycle (create, update, delete)
  - warkdev.axway_cft.axway_transfers_info: retrieves info about several transfers based on input
  - warkdev.axway_cft.axway_flow_info: retrieves info about flows (cftsend, cftpart, cftrecv, cftdest)

## Using this collection

Before using the collection, you need to install the collection with the `ansible-galaxy` CLI:

    ansible-galaxy collection install warkdev.axway_cft

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml` using the format:

```yaml
collections:
- name: warkdev.axway_cft
```

See [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Getting Started

In order to start writing your first playbook, simply add a target in your inventory leveraging the httpapi connector:

```yaml
all:
    children:
        axway_cft:
        hosts:
            axway_cft_v332:
                ansible_host: localhost # Not necessary if your host matches the inventory_hostname
                ansible_connection: httpapi
                ansible_http_api_port: 443 # Port of the Copilot Rest API
                ansible_network_os: warkdev.axway_cft.axway_cft # HttpApi plugin to use
                ansible_user: admin # User of the Copilot Rest API
                ansible_password: Passw0rd
                ansible_httpapi_use_ssl: "yes"
                ansible_httpapi_validate_certs: "yes"
```

You can then target freely this host inside any playbook of your choice.

## Contributing to this collection

If you want to develop new content for this collection or improve what is already here, the easiest way to work on the collection is to clone it into one of the configured [`COLLECTIONS_PATH`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#collections-paths), and work on it there.

You can find more information in the [developer guide for collections](https://docs.ansible.com/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections), and in the [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html).

## Release notes

See the [changelog](https://github.com/Warkdev/ansible-collection-axway_cft/tree/main/CHANGELOG.rst).

## More information

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Collections Checklist](https://github.com/ansible-collections/overview/blob/master/collection_requirements.rst)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)
- [The Bullhorn (the Ansible Contributor newsletter)](https://us19.campaign-archive.com/home/?u=56d874e027110e35dea0e03c1&id=d6635f5420)
- [Changes impacting Contributors](https://github.com/ansible-collections/overview/issues/45)

## Licensing

This collection is primarily licensed and distributed as a whole under the GNU General Public License v3.0 or later.

See [LICENSES/GPL-3.0-or-later.txt](https://github.com/Warkdev/ansible-collection-axway_cft/blob/main/COPYING) for the full text.

Parts of the collection are licensed under the [Apache 2.0 license](https://github.com/Warkdev/ansible-collection-axway_cft/blob/main/LICENSES/Apache-2.0.txt). This mostly applies to files vendored from the [Docker SDK for Python](https://github.com/docker/docker-py/).

All files have a machine readable `SDPX-License-Identifier:` comment denoting its respective license(s) or an equivalent entry in an accompanying `.license` file. Only changelog fragments (which will not be part of a release) are covered by a blanket statement in `.reuse/dep5`. This conforms to the [REUSE specification](https://reuse.software/spec/).