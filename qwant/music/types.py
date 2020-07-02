from typing import List, Mapping, Union

APIData = Mapping[
    str, Union[int, str, List[Mapping[str, Union[int, str]]]]
]  # Type alias
