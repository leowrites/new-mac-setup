# Oh My Zsh configuration
export ZSH="$HOME/.oh-my-zsh"

# Theme (you can change this to your preferred theme)
# Popular themes: robbyrussell, agnoster, powerlevel10k/powerlevel10k
ZSH_THEME="robbyrussell"

# Plugins
# Add plugins to this list to enable them
plugins=(
    git
    brew
    docker
    node
    npm
    python
    pip
    vscode
    zsh-autosuggestions
    zsh-completions
    fast-syntax-highlighting
    z
)

source $ZSH/oh-my-zsh.sh

# User configuration

# PATH configuration
export PATH="/opt/homebrew/bin:$PATH"
export PATH="/usr/local/bin:$PATH"
export PATH="$HOME/.local/bin:$PATH"

# Python
export PATH="$HOME/Library/Python/3.12/bin:$PATH"

# Node.js
export PATH="$HOME/.npm-global/bin:$PATH"

# Editor preferences
export EDITOR="code --wait"
export VISUAL="code --wait"

# FZF configuration (if you install fzf later)
# export FZF_DEFAULT_COMMAND='rg --files --hidden --glob "!.git/*"'
# export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"

# History configuration
HISTSIZE=10000
SAVEHIST=10000
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_SPACE
setopt HIST_VERIFY
setopt SHARE_HISTORY

# Load custom functions
if [[ -f ~/.zsh_functions ]]; then
    source ~/.zsh_functions
fi

# Load local customizations
if [[ -f ~/.zshrc.local ]]; then
    source ~/.zshrc.local
fi
