export PS1='
%F{cyan}%F{153}$(_prompt_help__simple_pwd)%F{magenta}$(_prompt_help__git_status) %B|%f  %U%F{blue}$(_prompt_help__deno_if_available)%U%F{green}$(_prompt_help__python_if_available)%F{black}-- $(date +%H:%M:%S)
%F{254}%F{green}%B>%f '