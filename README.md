# criteria-scripts

Here is our own python scripts

# Requirements

### Supported operating systems

Ubuntu 18.04+
macOS 10.15+
Windows 10 (64-bit)

### Supported Python versions

3.6
3.7
3.8
3.9

### Supported Pip version

version >=20.3

### Installation

```bash
pip install open3d
```

## error_test

Compute between 2 .ply point clouds:

- maximum distance
- minimum distance
- mean distance
- distance variance

### Use

```python
python3 error_test 'input_original_pcd' 'input_noised_pcd'
```

### Output

Console display

## label_comparator

Compute between two plane coloured .ply point clouds difference between planes

```python
python3 label_comparator.py 'original_ply' 'new_ply'
```

### Output

Console display

## label_comparator_autorun

Execute label_comparator on a original .ply file and a whole folder of other ply files

```python
python3 label_comparator_autorun.py 'original_ply' 'folder_path'
```

### Output

There is an example of logs in log/logs
