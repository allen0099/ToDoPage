from .base_config import Config
from .develope import Development
from .test import Testing

config: dict = {
    "development": Development,
    "testing": Testing,
}
