import argparse
import functools
import inspect
import typing
from inspect import Parameter
from typing import Callable, List, Type, Tuple, Union, Dict, Any


def match_parameter_type(type: Union[Type, Tuple[Type, Type]]) -> dict:
    if type in {int, float, str}:
        return {'type': type}
    elif type == bool:
        return {'action': 'store_true'}
    elif type[0] in {list, tuple}:
        return {'nargs': '*', 'type': type[1]}
    else:
        assert False, 'ERROR: `{}` is not matched'.format(type)


def purify_type(type) -> Union[Type, Tuple[Type, Type]]:
    if type in {str, int, float, bool}:
        return type
    elif type in {list, List}:
        return list, str
    elif type in {tuple, Tuple}:
        return tuple, str
    elif type == Parameter.empty:
        return str
    else:
        origin_type = typing.get_origin(type)
        args_type = typing.get_args(type)
        if origin_type in {list, tuple} \
                and len(args_type) == 1 \
                and args_type[0] in {str, int, float, bool}:
            return origin_type, args_type[0]
        else:
            raise Exception('Type `{}` is not supported.'.format(type))

def post_process(args: Dict[str, Any], types: Dict[str, Union[Type, Tuple[Type, Type]]]) -> Dict[str, Any]:
    return {
        name: tuple(value)
            if isinstance(types[name], tuple) and types[name][0] == tuple
            else value
        for name, value in args.items()
    }

def parse_args(*argument_parser_args, **argument_parser_kwargs):
    def parse(func: Callable):
        signature = inspect.signature(func)
        parameters: List[Parameter] = [param for name, param in signature.parameters.items()]
        types = {param.name: purify_type(param.annotation) for param in parameters}
        arguments_kwargs = {
            param.name: {
                'default': param.default if param.default != Parameter.empty else None,
                **match_parameter_type(types[param.name])
            }
            for param in parameters
        }
        #
        parser = argparse.ArgumentParser(*argument_parser_args, **argument_parser_kwargs)
        for name, kwargs in arguments_kwargs.items():
            parser.add_argument('--{}'.format(name), **kwargs)
        args = vars(parser.parse_args())
        #
        args = post_process(args, types)
        func = functools.partial(func, **args)
        return func
    return parse

