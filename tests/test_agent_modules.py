import subprocess
from types import SimpleNamespace
from src import agent_copilot, agent_codex, prompt


class FakeResult:
    def __init__(self, stdout, returncode=0):
        self.stdout = stdout
        self.returncode = returncode


def test_parse_output_message():
    out = 'some intro\nfeat(core): Add feature\nDetails here'
    parsed = prompt.parse_output_message(out)
    assert parsed.startswith('feat(core):')


def test_agent_copilot_parses(monkeypatch):
    fake = FakeResult('feat(scope): title\nmore', 0)
    monkeypatch.setattr(subprocess, 'run', lambda *a, **k: fake)
    res = agent_copilot.generate_commit_message_with_copilot()
    assert res is not None
    assert res.startswith('feat(scope):')


def test_agent_codex_parses(monkeypatch):
    fake = FakeResult('feat(scope): codex\nmore', 0)
    monkeypatch.setattr(subprocess, 'run', lambda *a, **k: fake)
    res = agent_codex.generate_commit_message_with_codex()
    assert res is not None
    assert res.startswith('feat(scope):')
