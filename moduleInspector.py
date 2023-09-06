import inspect

from CO2eTransportation import _knownFunctionNames


def get_function_args(func):
    argspec = inspect.getfullargspec(func)
    args_with_type = {}

    for arg in argspec.args:
        annotation = argspec.annotations.get(arg, None)
        default_value = ""
        if(len(argspec.args)-argspec.args.index(arg) <= len(argspec.defaults)):
            default_value = argspec.defaults[argspec.args.index(arg) - len(argspec.args)] if argspec.defaults else None
            is_optional = 1
        else:
            is_optional = 0

        args_with_type[arg] = {
            'type': annotation.__name__ if annotation else 'Any',
            'optional': is_optional,
            'default_value': default_value
        }

    return args_with_type


def jsonResultForPathWithParams(path: str, params: dict = None)-> str:
    return_dict = {}
    if path in _knownFunctionNames():
        mode = path;
        distance = float(params.get('distance', ['0'])[0])
        return_dict[mode] =0
    elif path == "help":
        functionsAndParams = {}
        for function_name in _knownFunctionNames():
            functionsAndParams[function_name.__name__] = get_function_args(function_name)
        return_dict = functionsAndParams

    return _remove_empty_strings(return_dict)


def _remove_empty_strings(d):
    if isinstance(d, dict):
        keys_to_remove = [key for key, value in d.items() if value == ""]
        for key in keys_to_remove:
            del d[key]
        for key, value in d.items():
            _remove_empty_strings(value)
    elif isinstance(d, list):
        d[:] = [item for item in d if not (isinstance(item, str) and item == "")]
    return d
