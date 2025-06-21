#!/bin/bash
set -e

echo "=== Available Disks ==="
lsblk
echo "Enter the disk to install to (e.g., /dev/sda):"
read -r DISK

if [[ ! -b "$DISK" ]]; then
    echo "Invalid disk: $DISK"
    exit 1
fi

echo "WARNING: This will erase all data on $DISK. Type 'yes' to continue:"
read -r CONFIRM
if [[ "$CONFIRM" != "yes" ]]; then
    echo "Aborted."
    exit 1
fi

# Partitioning (MBR for BIOS/legacy boot)
echo "Partitioning $DISK..."
parted "$DISK" --script mklabel msdos
parted "$DISK" --script mkpart primary ext4 1MiB 100%
parted "$DISK" --script set 1 boot on

# Format and mount
PART="${DISK}1"
mkfs.ext4 "$PART"
mount "$PART" /mnt

echo "Installing keys..."
pacman -Sy
pacman-key --init

# Install base system
echo "Installing base system..."
pacstrap /mnt base linux linux-firmware sudo

# fstab
genfstab -U /mnt >> /mnt/etc/fstab

# Ask for timezone
echo
echo "=== Timezone Configuration ==="
echo "Choose timezone selection method:"
echo "1) List common timezones"
echo "2) Browse by region"
echo "3) Enter timezone manually"
echo "4) Use UTC (default)"
read -r TZ_METHOD

case $TZ_METHOD in
    1)
        echo "Common timezones:"
        echo "1) America/New_York (EST/EDT)"
        echo "2) America/Chicago (CST/CDT)"
        echo "3) America/Denver (MST/MDT)"
        echo "4) America/Los_Angeles (PST/PDT)"
        echo "5) Europe/London"
        echo "6) Europe/Paris"
        echo "7) Europe/Berlin"
        echo "8) Asia/Tokyo"
        echo "9) Australia/Sydney"
        echo "Enter choice (1-9):"
        read -r TZ_CHOICE
        case $TZ_CHOICE in
            1) TIMEZONE="America/New_York" ;;
            2) TIMEZONE="America/Chicago" ;;
            3) TIMEZONE="America/Denver" ;;
            4) TIMEZONE="America/Los_Angeles" ;;
            5) TIMEZONE="Europe/London" ;;
            6) TIMEZONE="Europe/Paris" ;;
            7) TIMEZONE="Europe/Berlin" ;;
            8) TIMEZONE="Asia/Tokyo" ;;
            9) TIMEZONE="Australia/Sydney" ;;
            *) TIMEZONE="UTC" ;;
        esac
        ;;
    2)
        echo "Enter region (e.g., America, Europe, Asia):"
        read -r REGION
        if [[ -d "/usr/share/zoneinfo/$REGION" ]]; then
            echo "Available cities in $REGION:"
            ls "/usr/share/zoneinfo/$REGION" | grep -v '+' | head -20
            echo "Enter city:"
            read -r CITY
            if [[ -f "/usr/share/zoneinfo/$REGION/$CITY" ]]; then
                TIMEZONE="$REGION/$CITY"
            else
                echo "Invalid city, using UTC"
                TIMEZONE="UTC"
            fi
        else
            echo "Invalid region, using UTC"
            TIMEZONE="UTC"
        fi
        ;;
    3)
        echo "Enter timezone (e.g., America/New_York, Europe/London):"
        read -r TIMEZONE
        if [[ ! -f "/usr/share/zoneinfo/$TIMEZONE" ]]; then
            echo "Invalid timezone, using UTC"
            TIMEZONE="UTC"
        fi
        ;;
    *)
        TIMEZONE="UTC"
        ;;
esac

echo "Selected timezone: $TIMEZONE"

# Ask for username and password
echo "Enter name for default user:"
read -r USERNAME
echo "Enter password for $USERNAME:"
read -rs USERPASS

# Ask whether to enable root user
echo
echo "Do you want to enable the root user? (yes/no)"
read -r ENABLE_ROOT
if [[ "$ENABLE_ROOT" == "yes" ]]; then
    echo "Enter root password:"
    read -rs ROOTPASS
fi

# System config in chroot
arch-chroot /mnt /bin/bash <<EOF
ln -sf /usr/share/zoneinfo/$TIMEZONE /etc/localtime
hwclock --systohc
echo drawsko > /etc/hostname

# Install GRUB
pacman -Sy --noconfirm grub
grub-install --target=i386-pc --recheck "$DISK"
grub-mkconfig -o /boot/grub/grub.cfg

# Create user with sudo access
useradd -m -s /bin/bash "$USERNAME"
echo "$USERNAME:$USERPASS" | chpasswd
usermod -aG wheel "$USERNAME"

# Enable wheel group for sudo
echo '%wheel ALL=(ALL:ALL) ALL' >> /etc/sudoers

# Optionally set root password
if [[ "$ENABLE_ROOT" == "yes" ]]; then
    echo "root:$ROOTPASS" | chpasswd
fi

# Install networking and DE
pacman -Sy --noconfirm networkmanager cosmic alacritty packagekit git go firefox base-devel code
pacman -R --noconfirm cosmic-terminal cosmic-text-editor

# Enable services manually (since we're in chroot)
mkdir -p /etc/systemd/system/multi-user.target.wants/
mkdir -p /etc/systemd/system/display-manager.service.wants/

# Enable NetworkManager
ln -sf /usr/lib/systemd/system/NetworkManager.service \
       /etc/systemd/system/multi-user.target.wants/NetworkManager.service

# Enable cosmic-greeter
ln -sf /usr/lib/systemd/system/cosmic-greeter.service \
       /etc/systemd/system/display-manager.service.wants/cosmic-greeter.service

# Install yay as the user (not root)
sudo -u "$USERNAME" bash << 'EOFUSER'
cd /home/$USERNAME
git clone https://aur.archlinux.org/yay-bin.git
cd yay-bin
makepkg -si --noconfirm
cd ..
rm -rf yay-bin
EOFUSER

EOF

echo "=== Installation Complete! ==="
echo "User '$USERNAME' has been created with sudo access."
echo "NetworkManager and COSMIC desktop environment enabled."
echo "You can now reboot and remove the installation media."
