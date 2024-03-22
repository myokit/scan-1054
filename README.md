# Script to scan models for issue 1054

[This script](https://github.com/myokit/scan-1054/blob/main/scan.py) looks for expressions that could have lead to erroneous simulation output in Myokit versions before 1.36.0.

See https://github.com/myokit/myokit/pull/1055 for details.

## Usage

To scan a model, run this from the command line:

```
python scan.py /path/to/a/model.mmt
```

To scan a directory, use


```
python scan.py /where/i-keep/my-models
```

