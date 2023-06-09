{ pkgs ? import <nixpkgs> { } }:

let
  my-python = pkgs.python311;
  python-with-my-packages = my-python.withPackages(p: with p; [
    urwid
  ]);
in pkgs.mkShell {
  buildInputs = [
    python-with-my-packages
  ];

  shellHook = ''
    echo "Starting pytest-beeprint shell"
    export PATH="$PWD/.venv/bin:$PWD/.direnv/bin:$PATH";
    export PYTHONWARNINGS="ignore"
    export PYTHONPATH="${python-with-my-packages}/${python-with-my-packages.sitePackages}:$PYTHONPATH";
    export PYTHONPATH="$PWD/.venv/lib/python3.11/site-packages:$PYTHONPATH";

    if [ ! -f .direnv/installed ]; then
      touch .direnv/installed

      echo "Bootstrapping Environment"
      python -m venv .direnv
      .direnv/bin/pip install -U pip
      .direnv/bin/python setup.py develop
    fi
  '';
}
