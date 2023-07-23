import os
import tempfile
import pytest
from pyfrag_plotter.plotter.file_func import get_pyfrag_files


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files
        os.makedirs(os.path.join(temp_dir, 'dir1', 'dir2'))
        with open(os.path.join(temp_dir, 'file1.in'), 'w') as f:
            f.write('test')
        with open(os.path.join(temp_dir, 'pyfrag_file1.txt'), 'w') as f:
            f.write('test')
        with open(os.path.join(temp_dir, 'dir1', 'file2.in'), 'w') as f:
            f.write('test')
        with open(os.path.join(temp_dir, 'dir1', 'pyfrag_file2.txt'), 'w') as f:
            f.write('test')
        with open(os.path.join(temp_dir, 'dir1', 'dir2', 'file3.in'), 'w') as f:
            f.write('test')
        with open(os.path.join(temp_dir, 'dir1', 'dir2', 'pyfrag_file3.txt'), 'w') as f:
            f.write('test')
        yield temp_dir


def test_get_pyfrag_files_with_valid_inputfiles(temp_dir: str):
    pyfrag_files = get_pyfrag_files(temp_dir)
    assert len(pyfrag_files) == 3
    assert (os.path.join(temp_dir, 'file1.in'), os.path.join(temp_dir, 'pyfrag_file1.txt')) in pyfrag_files
    assert (os.path.join(temp_dir, 'dir1', 'file2.in'), os.path.join(temp_dir, 'dir1', 'pyfrag_file2.txt')) in pyfrag_files
    assert (os.path.join(temp_dir, 'dir1', 'dir2', 'file3.in'), os.path.join(temp_dir, 'dir1', 'dir2', 'pyfrag_file3.txt')) in pyfrag_files


def test_get_pyfrag_files_empty_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        with pytest.raises(FileNotFoundError):
            get_pyfrag_files(temp_dir)


def test_get_pyfrag_files_non_empty_with_invalid_inputfiles_dir():
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test files
        with open(os.path.join(temp_dir, "valid_file.in"), 'w') as f:
            f.write('test')
        with open(os.path.join(temp_dir, "non_valid_file.txt"), 'w') as f:
            f.write('test')
        with pytest.raises(FileNotFoundError):
            get_pyfrag_files(temp_dir)
