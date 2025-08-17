#!/usr/bin/env python3
"""
Mac Setup Script
Automates the setup of a new Mac with development tools and personal configurations.
"""

import os
import subprocess
import sys
import json
import shutil
from pathlib import Path
from typing import List, Dict, Any


class Colors:
    """ANSI color codes for terminal output."""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


class MacSetup:
    """Main setup class for Mac configuration."""
    
    def __init__(self):
        self.home = Path.home()
        
    def print_step(self, message: str) -> None:
        """Print a step message in blue."""
        print(f"\n{Colors.BLUE}==> {message}{Colors.NC}")
        
    def print_success(self, message: str) -> None:
        """Print a success message in green."""
        print(f"{Colors.GREEN}✓ {message}{Colors.NC}")
        
    def print_warning(self, message: str) -> None:
        """Print a warning message in yellow."""
        print(f"{Colors.YELLOW}⚠ {message}{Colors.NC}")
        
    def print_error(self, message: str) -> None:
        """Print an error message in red."""
        print(f"{Colors.RED}✗ {message}{Colors.NC}")
        
    def run_command(self, command: List[str], check: bool = True, shell: bool = False) -> subprocess.CompletedProcess:
        """Run a shell command and return the result."""
        try:
            if shell:
                result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
            else:
                result = subprocess.run(command, check=check, capture_output=True, text=True)
            return result
        except subprocess.CalledProcessError as e:
            self.print_error(f"Command failed: {' '.join(command) if isinstance(command, list) else command}")
            self.print_error(f"Error: {e.stderr}")
            if check:
                raise
            return e
            
    def command_exists(self, command: str) -> bool:
        """Check if a command exists in the system."""
        try:
            self.run_command(['which', command])
            return True
        except subprocess.CalledProcessError:
            return False
            
    def install_xcode_tools(self) -> None:
        """Install Xcode Command Line Tools."""
        self.print_step("Installing Xcode Command Line Tools")
        
        try:
            self.run_command(['xcode-select', '-p'])
            self.print_success("Xcode Command Line Tools already installed")
        except subprocess.CalledProcessError:
            self.print_warning("Installing Xcode Command Line Tools...")
            self.run_command(['xcode-select', '--install'])
            self.print_warning("Please complete the installation and run this script again")
            sys.exit(1)
            
    def install_homebrew(self) -> None:
        """Install Homebrew package manager."""
        self.print_step("Installing Homebrew")
        
        if self.command_exists('brew'):
            self.print_success("Homebrew already installed")
            return
            
        self.print_warning("Installing Homebrew...")
        install_script = '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        self.run_command(install_script, shell=True)
        
        # Add Homebrew to PATH for Apple Silicon Macs
        if os.path.exists("/opt/homebrew/bin/brew"):
            os.environ["PATH"] = f"/opt/homebrew/bin:{os.environ.get('PATH', '')}"
            
        self.print_success("Homebrew installed")
        
    def install_brew_packages(self) -> None:
        """Install packages via Homebrew."""
        self.print_step("Installing Homebrew packages")
        
        # CLI tools
        cli_tools = [
            'git', 'wget', 'gcc', 'python@3.12', 'node', 'npm'
        ]
        
        # Applications
        cask_apps = [
            'visual-studio-code', 'firefox', 'ghostty', 'notion', 
            'slack', '1password', 'docker', 'zoom',
            'raycast', 'nikitabobko/tap/aerospace'
        ]
        
        self.print_warning("Installing CLI tools...")
        for tool in cli_tools:
            if self._is_brew_package_installed(tool):
                self.print_success(f"{tool} already installed")
            else:
                self.print_warning(f"Installing {tool}...")
                try:
                    self.run_command(['brew', 'install', tool])
                    self.print_success(f"{tool} installed")
                except subprocess.CalledProcessError:
                    self.print_error(f"Failed to install {tool}")
                    
        self.print_warning("Installing applications...")
        for app in cask_apps:
            app_name = app.split('/')[-1]  # Get the actual app name
            if self._is_brew_cask_installed(app_name):
                self.print_success(f"{app_name} already installed")
            else:
                self.print_warning(f"Installing {app_name}...")
                try:
                    if '/' in app:  # It's a tap
                        self.run_command(['brew', 'install', app])
                    else:
                        self.run_command(['brew', 'install', '--cask', app])
                    self.print_success(f"{app_name} installed")
                except subprocess.CalledProcessError:
                    self.print_error(f"Failed to install {app}")
                    
    def _is_brew_package_installed(self, package: str) -> bool:
        """Check if a Homebrew package is installed."""
        try:
            self.run_command(['brew', 'list', package])
            return True
        except subprocess.CalledProcessError:
            return False
            
    def _is_brew_cask_installed(self, cask: str) -> bool:
        """Check if a Homebrew cask is installed."""
        try:
            self.run_command(['brew', 'list', '--cask', cask])
            return True
        except subprocess.CalledProcessError:
            return False
            
    def install_oh_my_zsh(self) -> None:
        """Install Oh My Zsh."""
        self.print_step("Installing Oh My Zsh")
        
        oh_my_zsh_path = self.home / '.oh-my-zsh'
        if oh_my_zsh_path.exists():
            self.print_success("Oh My Zsh already installed")
            return
            
        self.print_warning("Installing Oh My Zsh...")
        install_script = 'sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended'
        self.run_command(install_script, shell=True)
        self.print_success("Oh My Zsh installed")
        
    def install_zsh_plugins(self) -> None:
        """Install Zsh plugins."""
        self.print_step("Installing Zsh plugins")
        
        plugins_dir = self.home / '.oh-my-zsh' / 'custom' / 'plugins'
        plugins_dir.mkdir(parents=True, exist_ok=True)
        
        plugins = {
            'zsh-autosuggestions': 'https://github.com/zsh-users/zsh-autosuggestions',
            'zsh-syntax-highlighting': 'https://github.com/zsh-users/zsh-syntax-highlighting',
            'zsh-completions': 'https://github.com/zsh-users/zsh-completions'
        }
        
        for plugin_name, plugin_url in plugins.items():
            plugin_path = plugins_dir / plugin_name
            if plugin_path.exists():
                self.print_success(f"{plugin_name} already installed")
            else:
                self.print_warning(f"Installing {plugin_name}...")
                self.run_command(['git', 'clone', plugin_url, str(plugin_path)])
                self.print_success(f"{plugin_name} installed")
                
    def setup_git_config(self) -> None:
        """Setup Git configuration."""
        self.print_step("Setting up Git configuration")
        
        git_name = input("Git user name: ").strip()
        git_email = input("Git user email: ").strip()
        
        if git_name:
            self.run_command(['git', 'config', '--global', 'user.name', git_name])
            
        if git_email:
            self.run_command(['git', 'config', '--global', 'user.email', git_email])
            
        # Set useful defaults
        git_configs = [
            ['init.defaultBranch', 'main'],
            ['pull.rebase', 'false'],
            ['core.autocrlf', 'input'],
            ['core.editor', 'code --wait']
        ]
        
        for config_key, config_value in git_configs:
            self.run_command(['git', 'config', '--global', config_key, config_value])
            
        self.print_success("Git configuration completed")
        
    def setup_ssh_keys(self) -> None:
        """Setup SSH keys."""
        self.print_step("Setting up SSH keys")
        
        ssh_key_path = self.home / '.ssh' / 'id_ed25519'
        if ssh_key_path.exists():
            self.print_success("SSH key already exists")
            print("Public key:")
            with open(f"{ssh_key_path}.pub", 'r') as f:
                print(f.read().strip())
        else:
            ssh_email = input("Enter email for SSH key: ").strip()
            if ssh_email:
                self.run_command([
                    'ssh-keygen', '-t', 'ed25519', '-C', ssh_email,
                    '-f', str(ssh_key_path), '-N', ''
                ])
                
                # Add to ssh-agent
                self.run_command('eval "$(ssh-agent -s)"', shell=True)
                self.run_command(['ssh-add', str(ssh_key_path)])
                
                self.print_success("SSH key generated")
                print("Public key:")
                with open(f"{ssh_key_path}.pub", 'r') as f:
                    print(f.read().strip())
                    
    def setup_caps_lock_to_escape(self) -> None:
        """Map Caps Lock to Escape."""
        self.print_step("Mapping Caps Lock to Escape")
        
        # Set the mapping
        hidutil_command = 'hidutil property --set \'{"UserKeyMapping":[{"HIDKeyboardModifierMappingSrc":0x700000039,"HIDKeyboardModifierMappingDst":0x700000029}]}\''
        self.run_command(hidutil_command, shell=True)
        
        # Make it persistent
        launch_agents_dir = self.home / 'Library' / 'LaunchAgents'
        launch_agents_dir.mkdir(parents=True, exist_ok=True)
        
        plist_content = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.local.KeyRemapping</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/hidutil</string>
        <string>property</string>
        <string>--set</string>
        <string>{"UserKeyMapping":[{"HIDKeyboardModifierMappingSrc":0x700000039,"HIDKeyboardModifierMappingDst":0x700000029}]}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>'''
        
        plist_path = launch_agents_dir / 'com.local.KeyRemapping.plist'
        with open(plist_path, 'w') as f:
            f.write(plist_content)
            
        self.run_command(['launchctl', 'load', str(plist_path)])
        self.print_success("Caps Lock mapped to Escape (persistent)")
        
    def setup_dock(self) -> None:
        """Configure the macOS Dock with specific applications."""
        self.print_step("Configuring macOS Dock")
        
        # Clear the Dock first
        self.print_warning("Clearing current Dock...")
        self.run_command(['defaults', 'write', 'com.apple.dock', 'persistent-apps', '-array'])
        
        # Applications to add to Dock (in order)
        dock_apps = [
            '/Applications/Visual Studio Code.app',
            '/Applications/Slack.app', 
            '/Applications/Firefox.app'
        ]
        
        self.print_warning("Adding applications to Dock...")
        for app_path in dock_apps:
            if Path(app_path).exists():
                # Add app to Dock
                self.run_command([
                    'defaults', 'write', 'com.apple.dock', 'persistent-apps', '-array-add',
                    f'<dict><key>tile-data</key><dict><key>file-data</key><dict><key>_CFURLString</key><string>{app_path}</string><key>_CFURLStringType</key><integer>0</integer></dict></dict></dict>'
                ])
                self.print_success(f"Added {Path(app_path).stem} to Dock")
            else:
                self.print_warning(f"{Path(app_path).stem} not found at {app_path}")
        
        # Configure Dock settings
        dock_settings = [
            ('autohide', 'false'),  # Don't auto-hide dock
            ('magnification', 'false'),  # Disable magnification
            ('tilesize', '48'),  # Set icon size
            ('show-recents', 'false'),  # Don't show recent apps
            ('mineffect', 'scale')  # Minimize effect
        ]
        
        self.print_warning("Configuring Dock settings...")
        for setting, value in dock_settings:
            self.run_command(['defaults', 'write', 'com.apple.dock', setting, value])
            
        # Restart Dock to apply changes
        self.run_command(['killall', 'Dock'])
        self.print_success("Dock configured with VS Code, Slack, and Firefox")
        
    def copy_dotfiles(self) -> None:
        """Copy dotfiles from the dotfiles directory to home directory."""
        self.print_step("Copying dotfiles")
        
        script_dir = Path(__file__).parent
        dotfiles_dir = script_dir / 'dotfiles'
        
        if not dotfiles_dir.exists():
            self.print_error("dotfiles directory not found")
            return
            
        dotfiles = ['.zshrc', '.gitconfig', '.aerospace.toml']
        
        for dotfile in dotfiles:
            source = dotfiles_dir / dotfile
            target = self.home / dotfile
            
            if source.exists():
                # Backup existing file
                if target.exists():
                    backup = self.home / f"{dotfile}.backup"
                    target.rename(backup)
                    self.print_warning(f"Backed up existing {dotfile} to {dotfile}.backup")
                
                # Copy the dotfile
                shutil.copy2(source, target)
                self.print_success(f"Copied {dotfile}")
            else:
                self.print_warning(f"{dotfile} not found in dotfiles directory")
                
    def setup_vscode_settings_sync(self) -> None:
        """Setup VS Code and prompt for Settings Sync."""
        self.print_step("Setting up VS Code Settings Sync")
        
        if not self.command_exists('code'):
            self.print_warning("VS Code CLI not available. VS Code should be installed first.")
            return
            
        self.print_warning("Opening VS Code to set up Settings Sync...")
        
        # Open VS Code and show the settings sync command
        try:
            # Open VS Code
            self.run_command(['code'], check=False)
            
            self.print_success("VS Code opened")
            print()
            print("📋 Manual steps to complete:")
            print("1. In VS Code, press Cmd+Shift+P to open Command Palette")
            print("2. Type 'Settings Sync: Turn On' and select it")
            print("3. Choose 'Sign in with GitHub'")
            print("4. Complete the GitHub authentication")
            print("5. Your extensions and settings will sync automatically!")
            print()
            print("🔄 On future machines, just sign into GitHub in VS Code")
            print("   and your extensions/settings will sync automatically.")
            
        except subprocess.CalledProcessError:
            self.print_error("Failed to open VS Code")
            
    def install_vscode_extensions(self) -> None:
        """Recommend VS Code Settings Sync instead of manual extension installation."""
        self.print_step("VS Code Extensions")
        
        print("💡 Using VS Code Settings Sync for extensions and settings:")
        print("   • Sign into GitHub in VS Code")
        print("   • Enable Settings Sync") 
        print("   • All your extensions and settings will sync automatically!")
        print("   • Works across all your machines")
        
        self.print_success("VS Code extension management via Settings Sync recommended")
                    
    def setup_vscode_command_line(self) -> None:
        """Setup VS Code command line tools."""
        self.print_step("Setting up VS Code command line tools")
        
        if self.command_exists('code'):
            self.print_success("VS Code command line tools already available")
        else:
            self.print_warning("Please open VS Code and run 'Shell Command: Install code command in PATH'")
            self.print_warning("Or add VS Code to your PATH manually")
            
    def run_setup(self) -> None:
        """Run the complete setup process."""
        print(f"{Colors.BLUE}")
        print("🚀 Mac Setup Script")
        print("==================")
        print(f"{Colors.NC}")
        
        print("This script will set up your Mac with development tools and configurations.")
        response = input("Continue? (y/N): ").strip().lower()
        
        if response not in ['y', 'yes']:
            print("Setup cancelled.")
            return
            
        try:
            # Run setup steps
            self.install_xcode_tools()
            self.install_homebrew()
            self.install_brew_packages()
            self.install_oh_my_zsh()
            self.install_zsh_plugins()
            self.copy_dotfiles()
            self.setup_git_config()
            self.setup_ssh_keys()
            self.setup_caps_lock_to_escape()
            self.setup_dock()
            self.setup_vscode_command_line()
            self.setup_vscode_settings_sync()
            self.install_vscode_extensions()
            
            print(f"\n{Colors.GREEN}🎉 Setup completed successfully!{Colors.NC}")
            print()
            print("Next steps:")
            print("1. Restart your terminal or run: source ~/.zshrc")
            print("2. Complete VS Code Settings Sync setup if prompted")
            print("3. Configure Raycast and Aerospace with your preferences")
            print("4. Sign in to your applications (1Password, Slack, etc.)")
            print("5. Add your SSH key to GitHub (displayed above)")
            
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Setup interrupted by user{Colors.NC}")
        except Exception as e:
            print(f"\n{Colors.RED}Setup failed: {e}{Colors.NC}")
            raise


def main():
    """Main function."""
    if sys.platform != 'darwin':
        print("This script is designed for macOS only.")
        sys.exit(1)
        
    setup = MacSetup()
    setup.run_setup()


if __name__ == '__main__':
    main()