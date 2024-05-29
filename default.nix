{ pkgs ? import <nixpkgs> {} }:
with pkgs;
pkgs.mkShell {
  buildInputs = [
    python311
    python311Packages.requests
    python311Packages.ansible
    python311Packages.ansible-core
  ];
 
  shellHook = ''
    python3 -m venv .venv
    source .venv/bin/activate
  '';
}
