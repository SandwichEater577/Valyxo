import os
import tempfile
import shutil

import pytest

from src import Novahub as nh


@pytest.fixture
def temp_root(tmp_path):
    # Setup a temp workspace and override module-level constants
    root = tmp_path / "NovaHubDocuments"
    projects = root / "Projects"
    system = root / "System"
    config = root / "Config"
    main = projects / "Main"
    man = system / "man"

    # Create structure
    man.mkdir(parents=True, exist_ok=True)
    main.mkdir(parents=True, exist_ok=True)

    # Monkeypatch module-level paths so path_within_root works
    nh.ROOT_DIR = str(root)
    nh.PROJECTS_DIR = str(projects)
    nh.SYSTEM_DIR = str(system)
    nh.CONFIG_DIR = str(config)
    nh.MAIN_PROJECT = str(main)
    nh.MAN_DIR = str(man)

    # Ensure directories exist
    shell = nh.NovaHubShell()
    shell.fs.ensure_dirs()

    yield str(root)

    # cleanup
    try:
        shutil.rmtree(str(root))
    except Exception:
        pass


def test_mkdir_file_with_lang(temp_root):
    shell = nh.NovaHubShell()
    shell.initialize()
    shell.cwd = nh.MAIN_PROJECT
    # create file with quoted name and --py
    shell.handle_input_line('mkdir "test-123" --py')
    created = os.path.join(shell.cwd, 'test-123.py')
    assert os.path.isfile(created)


def test_mkdir_dir(temp_root):
    shell = nh.NovaHubShell()
    shell.initialize()
    shell.cwd = nh.MAIN_PROJECT
    shell.handle_input_line('mkdir test-123')
    created_dir = os.path.join(shell.cwd, 'test-123')
    assert os.path.isdir(created_dir)


def test_mkdir_quoted_with_spaces_and_lang(temp_root):
    shell = nh.NovaHubShell()
    shell.initialize()
    shell.cwd = nh.MAIN_PROJECT
    shell.handle_input_line('mkdir "file with spaces" --py')
    created = os.path.join(shell.cwd, 'file with spaces.py')
    assert os.path.isfile(created)
