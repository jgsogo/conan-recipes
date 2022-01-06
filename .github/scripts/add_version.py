import yaml
import os
import hashlib
import requests
from copy import deepcopy


def _version_key(v: str):
    if v.startswith('cci.'):
        return _version_key(f"0.{v[4:]}")
    if v.startswith('v'):
        return _version_key(v[1:])
    tokens = v.split('.')
    try:
        return [int(it) for it in tokens]
    except ValueError:
        return [-1]

def add_version_to_config(name, version):
    config_filename = os.path.join('recipes', name, 'config.yml')
    with open(config_filename, "r") as stream:
        data = yaml.safe_load(stream)
    data_versions = data['versions']

    versions = list(data_versions.keys())
    versions = sorted(versions, key=lambda u: _version_key(u))

    # Will add the new version using the same folder as the latest one
    last_version = versions[-1]

    # Operate on config.yml
    last_version_folder = data_versions.get(last_version).get('folder')
    data_versions[version] = {'folder': data_versions[last_version]['folder']}

    with open(config_filename, "w") as f:
        yaml.dump(data, f)
    print(data)
    return last_version_folder

def add_version_to_conandata(name, version, version_folder):
    conandata_filename = os.path.join('recipes', name, version_folder, 'conandata.yml')
    with open(conandata_filename, "r") as stream:
        data = yaml.safe_load(stream)
    data_versions = data['sources']

    versions = list(data_versions.keys())
    versions = sorted(versions, key=lambda u: _version_key(u))
    last_version = versions[-1]

    # Operate on conandata.yml (sources)
    url = f"https://github.com/jgsogo/{name}/archive/refs/tags/{version}.tar.gz"
    u = requests.get(url)
    hash = hashlib.sha256(u.content).hexdigest();

    data_versions[version] = {
        'url': url, 
        'sha256': hash
    }

    # Operate on conandata.yml (patches)
    data_patches = data.get('patches', {})
    patches = data_patches.get(last_version, [])
    if patches:
        data_patches[version] = deepcopy(data_patches[last_version])

    with open(conandata_filename, "w") as f:
        yaml.dump(data, f)
    print(data)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Add version to library.')
    parser.add_argument('--library', dest='library', help='Name of the library')
    parser.add_argument('--version', dest='version', help='Version to add')
    args = parser.parse_args()

    print(f"Add version '{args.version}' to library '{args.library}'")
    folder = add_version_to_config(args.library, args.version)
    add_version_to_conandata(args.library, args.version, folder)
