# Function-Argparse

## Installation

```shell
pip install .
```

## Usage

```python
from function_argparse import parse_args
from typing import List

@parse_args()
def main(x: int, y: List[int], z: str='hello'):
    pass

if __name__ == '__main__':
    main()
```

Equivalent code:

```python
from typing import List
import argparse

def main(x: int, y: List[int], z: str='hello'):
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--x', type=int)
    parser.add_argument('--z', type=str, default='hello')
    args = parser.parse_args()
    
    main(args.x, args.y, args.z)
```

## Supported Types

- Primitive types: `int`, `float`, `str`, `bool`.
- Generics: `List[T]`, `Tuple[T]`, where `T` is a primitive type.
