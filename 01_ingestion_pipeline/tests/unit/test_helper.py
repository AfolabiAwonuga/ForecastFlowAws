import os
import json
from get_data import get_data
from dotenv import load_dotenv

load_dotenv()


def test_flatten_helper():
    keys = ['wind', 'precipitation']
    data = {
        'wind': {
            'speed': 10,
            'direction': 'N'
        },
        'precipitation': {
            'type': 'rain',
            'amount': 5
        }
    }
    expected_result = {
        'wind_speed': 10,
        'wind_direction': 'N',
        'precipitation_type': 'rain',
        'precipitation_amount': 5
    }

    result = get_data.flatten_helper(keys, data)
    assert result == expected_result