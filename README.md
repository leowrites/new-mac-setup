# Mac Setup Script

Automated setup script for configuring a new Mac with development tools and personal configurations.

## What This Script Installs

### Development Tools
- **Languages**: Python (latest), Node.js
- **Version Control**: Git
- **Package Managers**: Homebrew, npm, pip, wget
- **Build Tools**: GCC, Xcode Command Line Tools

### Applications
- **Code Editor**: VS Code (with command line tool and Settings Sync)
- **Browsers**: Firefox
- **Development**: Docker
- **Communication**: Slack, Zoom
- **Productivity**: Notion, 1Password
- **Window Management**: Aerospace
- **Launcher**: Raycast
- **Terminal**: Ghostty

### System Configuration
- **Shell**: Oh My Zsh with plugins (autosuggestions, syntax highlighting, completions)
- **Key Remapping**: Caps Lock → Escape (persistent)
- **Dock**: Custom setup with VS Code, Slack, and Firefox only
- **Dotfiles**: Copies your personal configurations from `dotfiles/` folder
- **SSH Keys**: Generates new SSH key pair
- **Git Configuration**: Sets up user name and email

## Structure

```
new-mac-setup/
├── setup.py                 # Main Python setup script
├── dotfiles/
│   ├── .zshrc               # Zsh configuration
│   ├── .gitconfig           # Git configuration
│   └── .aerospace.toml      # Aerospace window manager config
└── README.md                # This file
```

## Usage

1. **Clone this repository**:
   ```bash
   git clone https://github.com/leowrites/new-mac-setup.git
   cd new-mac-setup
   ```

2. **Customize your dotfiles** in the `dotfiles/` folder

3. **Run the setup**:
   ```bash
   python3 setup.py
   ```

4. **Follow the prompts** for Git configuration and SSH key setup

## What Happens During Setup

1. **Installs Xcode Command Line Tools** (if not already installed)
2. **Installs Homebrew** package manager
3. **Installs all required tools and applications** via Homebrew
4. **Installs Oh My Zsh** and useful plugins
5. **Copies your dotfiles** from `dotfiles/` to your home directory
6. **Sets up Git configuration** (asks for your name and email)
7. **Generates SSH keys** for GitHub/Git usage
8. **Maps Caps Lock to Escape** (persistent across reboots)
9. **Configures Dock** with only VS Code, Slack, and Firefox
10. **Sets up VS Code with Settings Sync** for extensions and settings
11. **Sets up VS Code command line tools**

## Customization

### Adding More Tools
Edit the `cli_tools` and `cask_apps` lists in the `install_brew_packages()` method.

### Modifying Dotfiles
Edit the files in the `dotfiles/` folder to match your preferences.

## Manual Steps After Setup

1. **Restart Terminal** or run `source ~/.zshrc` to apply Zsh changes
2. **Complete VS Code Settings Sync** by signing into GitHub in VS Code
3. **Add SSH key to GitHub**: The script will display your public key
4. **Sign into applications**: 1Password, Slack, Zoom, Notion, etc.
5. **Configure Raycast and Aerospace** with your preferred shortcuts

## Requirements

- macOS (the script checks for this)
- Internet connection
- Administrator privileges (for some installations)

## License

MIT License - feel free to use and modify as needed.
