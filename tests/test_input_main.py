import os
from src import input as inp, main


def test_create_parser_has_commands():
    parser = inp.create_parser()
    args = parser.parse_args(['start'])
    assert args.command == 'start'
    args2 = parser.parse_args(['save', '--wip'])
    assert args2.command == 'save'


def test_parse_config_file_and_find(tmp_path, monkeypatch):
    cfg = tmp_path / '.meerkatrc'
    cfg.write_text('MRKT_AGENT=codex\nFOO=bar\n')
    # monkeypatch cwd for find_config_file
    monkeypatch.chdir(tmp_path)
    found = main.find_config_file()
    assert found is not None
    parsed = main.parse_config_file(found)
    assert parsed.get('MRKT_AGENT') == 'codex'


def test_is_quiet_mode():
    class A: pass
    args = A()
    args.verbose = False
    args.quiet = True
    cfg = {'MRKT_ALWAYS_QUIET': 'false'}
    assert main.is_quiet_mode(cfg, args) is True
