import os
import subprocess
from src import message


def test_print_message_and_error(capsys):
    message.print_message('hi', quiet=False)
    captured = capsys.readouterr()
    assert 'hi' in captured.out
    message.print_error('boom')
    captured = capsys.readouterr()
    assert 'Error: boom' in captured.err


def test_save_reference_to_file(tmp_path):
    cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        message.save_reference_to_file('content')
        with open('temp_git_message_reference.md', 'r') as f:
            assert f.read() == 'content'
    finally:
        os.chdir(cwd)


def test_generate_simple_commit_message_single():
    diff = 'diff --git a/foo b/foo\n'
    assert message.generate_simple_commit_message(diff) == 'Update foo'


def test_generate_simple_commit_message_multiple():
    diff = 'diff --git a/foo b/foo\ndiff --git a/bar b/bar\n'
    assert message.generate_simple_commit_message(diff) == 'Update 2 files'


def test_get_ai_commit_message_fallback(monkeypatch, tmp_path):
    # Simulate no staged diff
    monkeypatch.setattr(message, 'save_reference_to_file', lambda *a, **k: None)
    monkeypatch.setattr(message, 'run_command', lambda *a, **k: '')
    cfg = {}
    res = message.get_ai_commit_message(cfg, None, quiet=True)
    assert res is None or isinstance(res, str)
