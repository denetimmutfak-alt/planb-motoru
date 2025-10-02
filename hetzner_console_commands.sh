#!/bin/bash
# Hetzner Console'da çalıştırılacak komutlar

echo "=== HETZNER WEB CONSOLE KOMUTLARI ==="
echo
echo "1. Hetzner panelinde Actions > Console'a tıklayın"
echo "2. Web terminal açıldığında şu komutları sırayla çalıştırın:"
echo
echo "# Sistem durumu"
echo "whoami"
echo "uptime"
echo "df -h"
echo
echo "# Planb servis durumu"
echo "systemctl status planb"
echo "systemctl status docker"
echo
echo "# Eğer planb servisi yok ise:"
echo "ls -la /etc/systemd/system/ | grep planb"
echo "find /root -name '*telegram*' -type f"
echo "find /root -name '*planb*' -type f"
echo
echo "# Docker durumu"
echo "docker ps -a"
echo "docker images"
echo
echo "# SSH servis durumu"
echo "systemctl status ssh"
echo "systemctl enable ssh"
echo "systemctl start ssh"
echo
echo "3. Sonuçları bana bildirin!"