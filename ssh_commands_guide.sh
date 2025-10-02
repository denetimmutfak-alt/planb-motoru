#!/bin/bash
# SSH bağlantısı kurulduktan sonra çalıştırılacak komutlar

echo "=== HETZNER SUNUCU ANALİZİ ==="
echo
echo "1. SSH bağlantısı kuruldu mu? (Git Bash'te ssh root@116.203.57.250)"
echo "2. Bağlandıktan sonra şu komutları çalıştırın:"
echo
echo "# Temel sistem durumu"
echo "whoami"
echo "uptime" 
echo "df -h"
echo "free -h"
echo
echo "# PlanB servis durumu"
echo "systemctl status planb"
echo "systemctl list-unit-files | grep planb"
echo
echo "# Docker durumu"
echo "systemctl status docker"
echo "docker ps -a"
echo "docker images"
echo
echo "# Telegram bot dosyalarını bulalım"
echo "find /root -name '*telegram*' -type f 2>/dev/null"
echo "find /home -name '*telegram*' -type f 2>/dev/null"
echo "find /opt -name '*telegram*' -type f 2>/dev/null"
echo
echo "# Python process'leri"
echo "ps aux | grep python"
echo "ps aux | grep telegram"
echo
echo "# Sistemd servisleri"
echo "ls -la /etc/systemd/system/ | grep -E '(planb|telegram)'"
echo
echo "# Aktif network bağlantıları"
echo "netstat -tlnp | grep -E '(8000|5000|8080)'"
echo
echo "3. Her komutun çıktısını paylaşın!"