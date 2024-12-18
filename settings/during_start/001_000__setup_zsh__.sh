# 
# import paths from nix
# 
zsh_syntax_highlighting__path="$("$__FORNIX_NIX_COMMANDS/package_path_for" zsh-syntax-highlighting)"
zsh_auto_suggest__path="$("$__FORNIX_NIX_COMMANDS/package_path_for" zsh-autosuggestions)"
oh_my_zsh__path="$("$__FORNIX_NIX_COMMANDS/package_path_for" oh-my-zsh)"
zsh__path="$("$__FORNIX_NIX_COMMANDS/package_path_for" zsh)"

# 
# set fpath for zsh
# 
local_zsh="$FORNIX_FOLDER/settings/.cache/zsh.do_not_sync/site-functions/"
mkdir -p "$local_zsh"

export fpath=("$local_zsh" $fpath)
export fpath=("$oh_my_zsh__path"/share/oh-my-zsh/functions $fpath)
export fpath=("$oh_my_zsh__path"/share/oh-my-zsh/completions $fpath)
export fpath=("$zsh__path"/share/zsh/site-functions $fpath)
export fpath=("$zsh__path"/share/zsh/site-functions $fpath)
export fpath=("$zsh__path"/share/zsh/**/functions $fpath)

# See https://github.com/ohmyzsh/ohmyzsh/wiki/Themes
# ZSH_THEME="robbyrussell" # default

export ZSH="$oh_my_zsh__path/share/oh-my-zsh"
. "$ZSH/oh-my-zsh.sh"

autoload -Uz compinit
compinit

# 
# enable syntax highlighing
# 
export ZSH_HIGHLIGHT_HIGHLIGHTERS_DIR="$zsh_syntax_highlighting__path/share/zsh-syntax-highlighting/highlighters"
. "$ZSH_HIGHLIGHT_HIGHLIGHTERS_DIR/../zsh-syntax-highlighting.zsh"

# 
# enable auto suggestions
# 
. "$zsh_auto_suggest__path/share/zsh-autosuggestions/zsh-autosuggestions.zsh"

# SPACESHIP_CHAR_SYMBOL="∫ " # ☣ ⁂ ⌘ ∴ ∮ ֎ Ͽ ♫ ⛬ ⚿ ♦ ♢ ⛶ ✾ ❒ ⟩ ⟡ ⟜ ⟦ ⦊ ⦒ ⪢ ⪾ ∫ ∬ ∭

# Custom prompt (other prompts cause problems for some reason)
autoload -U promptinit; promptinit
_prompt_help__simple_pwd() {
    local maybe_relative_to_home="${PWD/#"$HOME"/"~"}"
    if [ -d ".git" ]
    then
        local path_to_file=""
        local dir_name=".git"
        local folder_to_look_in="$PWD"
        while :
        do
            # check if file exists
            if [ -d "$folder_to_look_in/$dir_name" ]
            then
                path_to_file="$folder_to_look_in"
                break
            else
                if [ "$folder_to_look_in" = "/" ]
                then
                    break
                else
                    folder_to_look_in="$(dirname "$folder_to_look_in")"
                fi
            fi
        done
        if [ -z "$path_to_file" ]
        then
            # fallback
            echo "$maybe_relative_to_home"
        else
            # git path
            echo "$(basename "$path_to_file")"
        fi
        # basename "$PWD"
    else
        echo "$maybe_relative_to_home"
    fi
}
_prompt_help__git_status() {
    # if git exists
    if [ -n "$(command -v "git")" ]
    then
        echo "  $(git rev-parse --abbrev-ref HEAD) "
    fi
}
_prompt_help__python_if_available() {
    if [ -n "$(command -v "python")" ]
    then
        local version_string="$(python --version)"
        echo "Python:${version_string/#Python /}%u  "
    fi
}
_prompt_help__deno_if_available() {
    if [ -n "$(command -v "deno")" ]
    then
        local version_string="$(deno --version)"
        echo "Deno:$(deno --version | sed -E 's/deno ([0-9]+\.[0-9]+\.[0-9]+).+/\1/' | head -n1)%u  "
    fi
}

autoload bashcompinit
bashcompinit

unalias -m '*' # remove all default aliases