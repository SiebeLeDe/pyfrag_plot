import pytest
import os
from configparser import ConfigParser
from pyfrag_plotter.config.config_handler import Config, config_key_to_function_mapping

current_dir = os.path.abspath(os.path.dirname(__file__))
package_path = os.path.abspath(os.path.join(current_dir, os.pardir))
path_to_config = os.path.join(package_path, "pyfrag_plotter", "config", "config.ini")
path_to_extra_config = os.path.join(current_dir, "fixtures", "extra_config.ini")
print(path_to_config)


def test_load_config():
    config_parser = ConfigParser()
    config_parser.read(path_to_config)
    config_inst = Config(config_parser)
    assert config_inst.get('EDA', 'EDA_keys') == ['Int', 'Elstat', 'OI', 'Pauli', 'Disp']


def test_load_extra_config():
    config_parser = ConfigParser()
    config_parser.read(path_to_extra_config)
    config_inst = Config(config_parser)
    assert config_inst.get('EDA', 'EDA_keys') == ['Int', 'Elstat', 'OI', 'Pauli']


@pytest.fixture
def config():
    config_parser = ConfigParser()
    config_parser.read(path_to_config)
    return Config(config_parser)


def test_default_section_exists(config):
    # The default section must always present in the config file
    assert 'DEFAULT' in config.config_parser.default_section


def test_default_section_right_keys(config):
    # For debugging: error if the default section does not contain all the keys
    default_section = config.config_parser.defaults()
    required_keys = [key.lower() for key in config_key_to_function_mapping.keys()]
    for key in default_section:
        assert key in required_keys


def test_get_shared(config):
    assert config.get('SHARED', 'line_styles') == ["solid", "dashed", "dotted", "dashdot", "dashed"]


def test_get_asm(config):
    assert config.get('ASM', 'ASM_strain_keys') == ['StrainTotal', 'frag1Strain', 'frag2Strain']


def test_get_matplotlib(config):
    assert config.get('MATPLOTLIB', 'font') == 'arial'


def test_get_extra_config():
    config_parser = ConfigParser()
    config_parser.read(path_to_config)
    config_parser.read(path_to_extra_config)
    config = Config(config_parser)
    assert config.get('SHARED', 'y_lim') == [-30, 30]


def test_get_extra_config_override():
    config_parser = ConfigParser()
    config_parser.read(path_to_config)
    config_parser.read(path_to_extra_config)
    config = Config(config_parser)
    assert config.get('SHARED', 'y_lim') == [-30, 30]


def test_get_extra_config_missing_key():
    config_parser = ConfigParser()
    config_parser.read(path_to_config)
    config_parser.read(path_to_extra_config)
    config = Config(config_parser)
    with pytest.raises(ValueError):
        config.get('EDA', 'missing_key')


def test_get_extra_config_missing_section():
    config_parser = ConfigParser()
    config_parser.read(path_to_config)
    config_parser.read(path_to_extra_config)
    config = Config(config_parser)
    with pytest.raises(ValueError):
        config.get('MISSING_SECTION', 'missing_key')
