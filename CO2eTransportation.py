import inspect



def _knownFunctionNames() ->list:
    """

    :rtype: List of Strings
    """
    return [calculateWithDistanceAndTransportationmode,
     co2_patients,
     co2_employees_per_year,
     co2_employees_per_year_single_mode]

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

def _emissionFactor(mode):
    """
    Factor of Carbon Emissions per kg/km

    Args:
        mode (str): The mode of transportation.

    Returns:
        float: The emission factor for the given mode.

    Raises:
        ValueError: If the given mode of transportation is not recognized.
    """
    if (mode in ModesOfTransport.modeFactor):
        return ModesOfTransport.modeFactor[mode]
    else:
        raise ValueError("Unknown mode of transportation: " + mode)


def _mean_distance_estimate_patients() -> float:
    """
    Mean distance estimate for patients.

    Returns:
        float: The estimated mean distance in kilometers.
    """
    return _mean_distance_estimate()


def _mean_distance_estimate_employees() -> float:
    """
    Mean distance estimate for employees.

    Returns:
        float: The estimated mean distance in kilometers.
    """
    return _mean_distance_estimate()


def _mean_distance_estimate() -> float:
    """
    Estimate of mean distance traveled based on statistical data.

    Returns:
        float: The estimated mean distance in kilometers.
    """
    mean_distance_estimate_employees = (2.5 * 0.266 + 7.5 * 0.218 + 17.5 * 0.291 + 37.5 * 0.141 + 75 * 0.05) / 0.98
    return mean_distance_estimate_employees


class ModesOfTransport:
    bus = "bus"
    subway_cableCar = "subway_cableCar"
    train = "train"
    car = "car"
    motorcycle = "motorcycle"
    bicycle = "bicycle"
    walking = "walking"
    modeFactor = {bus: 0.03, subway_cableCar: 0.01, train: 0.01, bicycle: 0, walking: 0, car: 0.2}


def _distribution_of_modes_estimate() -> dict:
    """
    Estimate of distribution of transportation modes.

    Returns:
        dict: A dictionary containing the percentage distribution of different transportation modes.
    """
    return {ModesOfTransport.bus: 4.2,
            ModesOfTransport.subway_cableCar: 4.9,
            ModesOfTransport.train: 4.6,
            ModesOfTransport.car: 68.0,
            ModesOfTransport.motorcycle: 0.6,
            ModesOfTransport.bicycle: 10.5}


def calculateWithDistanceAndTransportationmode(distance, mode=ModesOfTransport.car):
    """
    Calculates carbon emissions based on distance and transportation mode.

    Args:
        distance (float): The distance traveled in kilometers.
        mode (str): The mode of transportation. Defaults to ModesOfTransport.car.
        modes are  "bus"
    subway_cableCar = "subway_cableCar"
    train = "train"
    car = "car"
    motorcycle = "motorcycle"
    bicycle = "bicycle"
    walking = "walking"
    Returns:
        float or None: The calculated carbon emissions or None if the mode is not recognized.
    """
    try:
        return _emissionFactor(mode) * distance
    except ValueError:
        return None


def _norm(modes: dict) -> dict:
    """
    Normalize a dictionary of mode distribution percentages.

    Args:
        modes (dict): A dictionary containing mode distribution percentages.



    Returns:
        dict: A normalized dictionary of mode distribution percentages.
    """
    summe = sum([modes[key] for key in modes])
    for key in modes:
        modes[key] = modes[key] / summe
    return modes


def co2_patients(number_of_visits: int, mean_distance: float = _mean_distance_estimate_patients(),
                 distribution_of_modes=0) -> float:
    """
    Calculate CO2 equivalents for patient visits.

    Args:
        number_of_visits (int): Number of patient visits.
        mean_distance (float): Mean distance traveled in kilometers.
        distribution_of_modes (dict): Distribution of transportation modes. Defaults to None.

    Returns:
        float: The calculated CO2 equivalents.
    """
    if distribution_of_modes == 0:
        distribution_of_modes = _distribution_of_modes_estimate()
    co2equivalent: int = 0
    for mode in distribution_of_modes:
        mode_amount = distribution_of_modes[mode]
        co2equivalent += number_of_visits * mean_distance * (mode_amount * _emissionFactor(mode))
    return co2equivalent


def co2_employees_per_year(fulltimequivalents: int, mean_distance: float = _mean_distance_estimate_employees(),
                           distribution_of_modes=None) -> float:
    """
    Calculate CO2 equivalents for employee travel per year.

    Args:
        fulltimequivalents (int): Number of full-time equivalents.
        mean_distance (float): Mean distance traveled in kilometers.
        distribution_of_modes (dict): Distribution of transportation modes. Defaults to None.

    Returns:
        float: The calculated CO2 equivalents.
    """
    if distribution_of_modes is None:
        distribution_of_modes = _distribution_of_modes_estimate()
    no_of_workdays = 230
    return co2_patients(number_of_visits=fulltimequivalents * no_of_workdays,
                        mean_distance=mean_distance,
                        distribution_of_modes=distribution_of_modes)


def co2_employees_per_year_single_mode(fulltimequivalents: int, distance: float = _mean_distance_estimate_employees(),
                                       mode: str = ModesOfTransport.car) -> float:
    """
    Calculate CO2 equivalents for employee travel per year with a single mode of transportation.

    Args:
        fulltimequivalents (int): Number of full-time equivalents.
        distance (float): Distance traveled in kilometers. Defaults to _mean_distance_estimate_employees().
        mode (str): The mode of transportation. Defaults to ModesOfTransport.car.

    Returns:
        float: The calculated CO2 equivalents.
    """
    no_of_workdays = 230
    return co2_patients(number_of_visits=fulltimequivalents * no_of_workdays,
                        mean_distance=distance,
                        distribution_of_modes={mode: 1})


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

if __name__ == '__main__':
    print("Testing CO2eTransportation")
    function_to_inspect = co2_employees_per_year_single_mode
    args_info = get_function_args(function_to_inspect)

    for arg, info in args_info.items():
        optional_text = ' (optional)' if info['optional'] else '0'
        default_text = f', default: {info["default_value"]}' if info['optional'] else '0'
        print(f"{arg}: {info['type']}{optional_text}{default_text}")

    print ("Testing external function jsonResultForPathWithParams")
    path = "help"
    params = ""
    print(jsonResultForPathWithParams(path))