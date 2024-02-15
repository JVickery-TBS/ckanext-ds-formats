[![Tests](https://github.com/JVickery-TBS/ckanext-ds-formats/workflows/Tests/badge.svg?branch=main)](https://github.com/JVickery-TBS/ckanext-ds-formats/actions)

# ckanext-ds-formats

CKAN plugin to add more DataStore dump formats


## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.6 and earlier | Not tested    |
| 2.7             | Not tested    |
| 2.8             | No    |
| 2.9             | Yes    |
| 2.10             | Not tested    |

| Python version    | Compatible?   |
| --------------- | ------------- |
| 2.9 and earlier | Not tested    |
| 3.0 and later             | Yes    |

## Installation

To install ckanext-ds-formats:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    git clone --branch master --single-branch https://github.com/JVickery-TBS/ckanext-ds-formats.git
    cd ckanext-ds-formats
    pip install -e .
    pip install -r requirements.txt

3. Add `ds_formats` to the `ckan.plugins` setting in your CKAN
   config file. Make sure that it comes before `datastore`

7. Restart CKAN

## Config settings

```
N/A
```

## License

[GPL3](https://raw.githubusercontent.com/JVickery-TBS/ckanext-ds-formats/main/LICENSE)
