{
    description = "json_fix";
    inputs = {
        nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
        home-manager.url = "github:nix-community/home-manager/release-25.05";
        home-manager.inputs.nixpkgs.follows = "nixpkgs";
        xome.url = "github:jeff-hykin/xome";
        xome.inputs.home-manager.follows = "home-manager";
    };
    outputs = { self, nixpkgs, xome, ... }:
        xome.superSimpleMakeHome { inherit nixpkgs; pure = true; } ({pkgs, system, ...}:
            let
                isMacOs = (builtins.match ".*darwin.*" system) != null;
                stdenvLibs = (builtins.filter
                    (eachPkg: eachPkg != null)
                    [
                        pkgs.stdenv.cc.cc
                        (if !isMacOs then pkgs.glibc else null)
                        pkgs.zlib
                        pkgs.freetype
                        pkgs.libjpeg
                        pkgs.libpng
                    ]
                );
            in
                {
                    # for home-manager examples, see: https://deepwiki.com/nix-community/home-manager/5-configuration-examples
                    # all home-manager options: https://nix-community.github.io/home-manager/options.xhtml
                    home.homeDirectory = "/tmp/virtual_homes/json_fix";
                    home.stateVersion = "25.05";
                    home.packages = stdenvLibs ++ [
                        (pkgs.python3.withPackages (ps: [
                            # ps.requests
                            # ps.numpy
                            # ps.pymupdf
                            # sqlite3 is part of stdlib, but python3Full includes CLI too
                            # (pythonPkgs.buildPythonPackage {
                            #     pname = "kittentts";
                            #     version = "0.1.0";
                            #     src = ./subrepos/KittenTTS;
                            # 
                            #     # Optional: if you have pyproject.toml, use `buildPythonPackage` with `pyproject` support
                            #     format = "pyproject";
                            #     nativeBuildInputs = [ pythonPkgs.setuptools ];
                            # })
                        ]))
                        pkgs.python3Packages.venvShellHook
                        pkgs.sqlite
                        pkgs.deno
                        
                        # vital stuff
                        pkgs.coreutils-full
                        pkgs.dash # needed to make "sh"
                        
                        # optional stuff (things you probably want)
                        pkgs.gnugrep
                        pkgs.findutils
                        pkgs.wget
                        pkgs.curl
                        pkgs.unixtools.locale
                        pkgs.unixtools.more
                        pkgs.unixtools.ps
                        pkgs.unixtools.getopt
                        pkgs.unixtools.ifconfig
                        pkgs.unixtools.hostname
                        pkgs.unixtools.ping
                        pkgs.unixtools.hexdump
                        pkgs.unixtools.killall
                        pkgs.unixtools.mount
                        pkgs.unixtools.sysctl
                        pkgs.unixtools.top
                        pkgs.unixtools.umount
                        pkgs.git
                        pkgs.htop
                        pkgs.ripgrep
                    ];
                    
                    programs = {
                        home-manager = {
                            enable = true;
                        };
                        zsh = {
                            enable = true;
                            enableCompletion = true;
                            autosuggestion.enable = true;
                            syntaxHighlighting.enable = true;
                            shellAliases.ll = "ls -la";
                            history.size = 100000;
                            # this is kinda like .zshrc
                            initContent = ''
                                # lots of things need "sh"
                                ln -s "$(which dash)" "$HOME/.local/bin/sh" 2>/dev/null
                                
                                # check for .pypirc for publishing to pypi
                                if [ -f "$XOME_REAL_HOME/.pypirc" ]
                                then
                                    rm -f "$HOME/.pypirc"
                                    ln -s "$XOME_REAL_HOME/.pypirc" "$HOME/.pypirc"
                                fi
                                
                                setopt interactivecomments
                                
                                #
                                # venv
                                #
                                export VENV_DIR=.venv
                                
                                # Include libstdc++ and others in linker path
                                export LD_LIBRARY_PATH="${pkgs.lib.makeLibraryPath stdenvLibs}:$LD_LIBRARY_PATH"
                                if [ ! -d "$VENV_DIR" ]; then
                                    python3 -m venv $VENV_DIR
                                    source "$VENV_DIR/bin/activate"
                                    pip install --upgrade pip
                                    # check if file exists
                                    if [ -f "./requirements.txt" ]
                                    then
                                        pip install -r ./requirements.txt
                                    fi
                                else
                                    source "$VENV_DIR/bin/activate"
                                fi
                                
                                # this enables some impure stuff like sudo, comment it out to get FULL purity
                                export PATH="$PATH:/usr/bin/"
                            '';
                        };
                        # fancy prompt
                        starship = {
                            enable = true;
                            enableZshIntegration = true;
                        };
                    };
                }
        );
}