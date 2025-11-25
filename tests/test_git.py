import subprocess
import builtins
from src import git


def test_run_command_capture_output_success():
    out = git.run_command('echo hello', capture_output=True)
    assert out.strip() == 'hello'


def test_run_command_no_capture_success():
    res = git.run_command('true')
    assert res is True


def test_run_command_failure_returns_none():
    # `false` returns non-zero
    res = git.run_command('false', quiet=True)
    assert res is None


def test_get_current_branch_when_no_git(monkeypatch):
    monkeypatch.setattr(git, 'run_command', lambda *a, **k: None)
    assert git.get_current_branch() == 'main'


def test_get_git_status_info_parsing(monkeypatch):
    name_status = 'M\tfile1.py\nA\tfile2.txt\n'
    numstat = '10\t2\tfile1.py\n-\t-\tfile2.txt\n'
    def fake_run(cmd, capture_output=False, quiet=False):
        if 'name-status' in cmd:
            return name_status
        if 'numstat' in cmd:
            return numstat
        return ''

    monkeypatch.setattr(git, 'run_command', fake_run)
    info = git.get_git_status_info()
    assert info['total_files'] == 2
    assert info['additions'] == 10
    assert info['deletions'] == 2


def test_create_and_push_branch(monkeypatch, capsys):
    calls = []
    def fake_run(cmd, quiet=False, capture_output=False):
        calls.append(cmd)
        return True

    monkeypatch.setattr(git, 'run_command', fake_run)
    ok = git.create_and_push_branch('mrkt/feature', quiet=True)
    assert ok is True


def test_perform_rebase_and_merge(monkeypatch):
    monkeypatch.setattr(git, 'run_command', lambda *a, **k: True)
    assert git.perform_rebase(quiet=True) is True
    assert git.perform_merge(quiet=True) is True
