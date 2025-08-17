# Dotfiles

This folder contains your actual configuration files that will be copied to your home directory during setup.

## Files:

- **`.zshrc`** - Zsh shell configuration with Oh My Zsh, plugins, and PATH settings
- **`.gitconfig`** - Git configuration with common settings
- **`.aerospace.toml`** - AeroSpace window manager configuration

## Usage:

The setup script will copy these files directly to your home directory (`~`). Any existing files will be backed up first.

## Customization:

Modify these files to match your preferred configuration. When you run the setup script on a new machine, these exact configurations will be applied.

## Adding New Dotfiles:

To add more dotfiles, simply create them in this folder and update the setup script to copy them.
