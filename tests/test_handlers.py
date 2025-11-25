from types import SimpleNamespace
from src import handle_start, handle_save, handle_update


def test_build_branch_name_and_prefix():
    cfg = {'MRKT_PREFIX': 'mrkt', 'MRKT_PREFIX_SEPARATOR': '/'}
    assert handle_start.build_branch_name(cfg, 'feat', 'name', None, False) == 'feat/name'
    assert handle_start.build_branch_name(cfg, None, 'name', 'custom', False) == 'custom/name'
    assert handle_start.build_branch_name(cfg, None, 'name', None, True) == 'name'


def test_build_commit_and_push_command():
    cfg = {'MRKT_NO_VERIFY': 'true'}
    cmd = handle_save.build_commit_command(cfg, 'msg', wip=False)
    assert '--no-verify' in cmd
    cmd2 = handle_save.build_commit_command({}, 'm', wip=True)
    assert 'WIP:' in cmd2
    p = handle_update.build_push_command({'MRKT_NO_VERIFY_PUSH': 'false', 'MRKT_NO_VERIFY': 'false'}, 'branch')
    assert 'git push origin branch' in p


def test_handle_save_and_update_flow(monkeypatch):
    # monkeypatch run_command and get_ai_commit_message to simulate full flow
    monkeypatch.setattr('src.handle_save.run_command', lambda *a, **k: True)
    monkeypatch.setattr('src.handle_save.get_git_status_info', lambda *a, **k: None)
    monkeypatch.setattr('src.handle_save.perform_rebase', lambda *a, **k: True)
    monkeypatch.setattr('src.handle_save.perform_merge', lambda *a, **k: True)
    monkeypatch.setattr('src.handle_save.get_ai_commit_message', lambda *a, **k: 'feat: ok')
    args = SimpleNamespace(rebase=False, merge=False, wip=False, story=None)
    res = handle_save.handle_save_command(args, {}, quiet=True)
    assert res == 0

    # update: use same monkeypatch for run_command
    monkeypatch.setattr('src.handle_update.run_command', lambda *a, **k: True)
    monkeypatch.setattr('src.handle_update.get_current_branch', lambda *a, **k: 'branch')
    args2 = SimpleNamespace(close=False, rebase=False, merge=False, wip=False, story=None)
    res2 = handle_update.handle_update_command(args2, {}, quiet=True)
    assert res2 == 0
