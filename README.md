# DrawkoOS

My custom Arch Linux distro because why not? 🤷♂️

## What is this?

Basically I got tired of installing Arch the same way over and over, so I made my own installer script and slapped COSMIC desktop on it. It's Arch Linux but with less suffering during setup.

## What you get

- Arch Linux (obviously)
- COSMIC desktop because it looks cool and is written in Rust
- Firefox
- Alacritty terminal (fast and shiny)
- Code OSS for text editing
- Yay for installing random stuff from AUR
- NetworkManager so your wifi actually works
- A user account that can sudo (revolutionary, I know)

## Why COSMIC?

Because GNOME is bloated, KDE breaks when you look at it wrong, and COSMIC is the new shiny thing. Plus it's made by System76 and those guys know what they're doing.

## Installation

1. Boot the thing
2. Run `./install.sh`
3. Answer some questions (timezone, username, password, etc.)
4. Wait for it to do its magic
5. Reboot

The installer will ask you stuff like:
- Which disk to nuke
- What timezone you're in
- Username and password
- Whether you want root access

## What's different from regular Arch?

- You don't have to type 500 commands to get a working desktop
- COSMIC instead of whatever desktop you were gonna install anyway
- Some sensible defaults
- Yay is already there so you can `yay -S github-desktop-bin` immediately after install

## Should you use this?

If you:
- Like Arch but hate the installation process
- Want to try COSMIC without setting it up yourself
- Trust random GitHub repos with your computer
- Don't mind if things occasionally break

Then sure, go for it.

## Requirements

- A computer (x86_64)
- At least 2GB RAM (4GB if you don't want pain)
- 20GB+ storage
- Willingness to debug things when they inevitably break

## Contributing

Found a bug? Cool, open an issue. Want to improve something? PRs welcome.

## Warning

This will completely wipe whatever disk you point it at. I'm not responsible if you accidentally nuke your data. Back up your stuff.

Also, this is a hobby project. I made it for me, but you can use it too if you want. No support guaranteed, but I'll try to help.