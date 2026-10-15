#!/bin/bash

CHROMIUM_DIR="$HOME/chromium"
CRED_FILE="$CHROMIUM_DIR/credentials.txt"

print_banner() {
  echo -e '\e[0;32m'
  echo " ▄████████  ▄██████▄     ▄████████    ▄████████     ███▄▄▄▄    ▄██████▄  ████████▄     ▄████████ "
  echo "███    ███ ███    ███   ███    ███   ███    ███     ███▀▀▀██▄ ███    ███ ███   ▀███   ███    ███ "
  echo "███    █▀  ███    ███   ███    ███   ███    █▀      ███   ███ ███    ███ ███    ███   ███    █▀  "
  echo "███        ███    ███  ▄███▄▄▄▄██▀  ▄███▄▄▄         ███   ███ ███    ███ ███    ███  ▄███▄▄▄     "
  echo "███        ███    ███ ▀▀███▀▀▀▀▀   ▀▀███▀▀▀         ███   ███ ███    ███ ███    ███ ▀▀███▀▀▀     "
  echo "███    █▄  ███    ███ ▀███████████   ███    █▄      ███   ███ ███    ███ ███    ███   ███    █▄  "
  echo "███    ███ ███    ███   ███    ███   ███    ███     ███   ███ ███    ███ ███   ▄███   ███    ███ "
  echo "████████▀   ▀██████▀    ███    ███   ██████████      ▀█   █▀   ▀██████▀  ████████▀    ██████████ "
  echo "                        ███    ███                                                               "
  echo ""
  echo -e '\e[0m'
}

# docker compose komutunu belirle (v1 veya plugin)
compose() {
  if command -v docker-compose &>/dev/null; then
    docker-compose "$@"
  else
    docker compose "$@"
  fi
}

install_docker() {
  if command -v docker &>/dev/null; then
    echo "Docker zaten kurulu."
  else
    echo "Docker kuruluyor..."
    wget -q -O docker.sh https://raw.githubusercontent.com/molla202/molla202/refs/heads/main/docker.sh \
      && chmod +x docker.sh && sudo /bin/bash docker.sh
    rm -f docker.sh
  fi
}

install_chromium() {
  if ! command -v docker &>/dev/null; then
    echo "Docker kurulu değil, önce kuruluyor..."
    install_docker
  fi

  TIMEZONE=$(timedatectl | grep "Time zone" | awk '{print $3}')
  [ -z "$TIMEZONE" ] && TIMEZONE="Asia/Jakarta"
  echo "Sunucu saat dilimi: $TIMEZONE"

  mkdir -p "$CHROMIUM_DIR" && cd "$CHROMIUM_DIR" || exit 1

  # Kayıtlı bilgi varsa tekrar kullan
  if [ -f "$CRED_FILE" ]; then
    CUSTOM_USER=$(grep '^Username:' "$CRED_FILE" | awk '{print $2}')
    PASSWORD=$(grep '^Password:' "$CRED_FILE" | awk '{print $2}')
    echo "Kayıtlı kullanıcı bilgileri kullanılıyor."
  else
    CUSTOM_USER=$(openssl rand -hex 4)
    PASSWORD=$(openssl rand -hex 12)
  fi

  cat <<EOF >docker-compose.yaml
---
services:
  chromium:
    image: lscr.io/linuxserver/chromium:latest
    container_name: chromium
    security_opt:
      - seccomp:unconfined
    environment:
      - CUSTOM_USER=$CUSTOM_USER
      - PASSWORD=$PASSWORD
      - PUID=1000
      - PGID=1000
      - TZ=$TIMEZONE
      - LANG=en_US.UTF-8
      - CHROME_CLI=https://google.com/
    volumes:
      - $CHROMIUM_DIR/config:/config
    ports:
      - 3010:3000
      - 3011:3001
    shm_size: "1gb"
    restart: unless-stopped
EOF

  echo "Chromium container başlatılıyor..."
  compose up -d || { echo "Başlatılamadı!"; return 1; }

  IPVPS=$(curl -s ifconfig.me)

  # Bilgileri dosyaya kaydet
  cat <<EOF >"$CRED_FILE"
URL (http):  http://$IPVPS:3010/
URL (https): https://$IPVPS:3011/
Username: $CUSTOM_USER
Password: $PASSWORD
EOF
  chmod 600 "$CRED_FILE"

  echo ""
  show_credentials
  echo "Bilgiler kaydedildi: $CRED_FILE"
  docker system prune -f >/dev/null
}

show_credentials() {
  if [ -f "$CRED_FILE" ]; then
    echo "------ Chromium Giriş Bilgileri ------"
    cat "$CRED_FILE"
    echo "--------------------------------------"
  else
    echo "Kayıtlı bilgi bulunamadı. Önce Chromium kur (2)."
  fi
}

remove_chromium() {
  read -rp "Chromium kaldırılsın mı? (y/N): " ans
  if [[ "$ans" =~ ^[Yy]$ ]]; then
    cd "$CHROMIUM_DIR" 2>/dev/null && compose down
    echo "Kaldırıldı. (Config ve credentials dosyası silinmedi: $CHROMIUM_DIR)"
  fi
}

while true; do
  clear
  print_banner
  echo "========== CoreNode HQ Kurulum Menüsü =========="
  echo "1) Docker kur"
  echo "2) Chromium kur"
  echo "3) Kayıtlı Chromium bilgilerini göster"
  echo "4) Chromium'u kaldır"
  echo "0) Çıkış"
  echo "================================================"
  read -rp "Seçim: " choice

  case $choice in
    1) install_docker ;;
    2) install_chromium ;;
    3) show_credentials ;;
    4) remove_chromium ;;
    0) echo "Subscribe: https://corenodehq.com"; exit 0 ;;
    *) echo "Geçersiz seçim." ;;
  esac

  echo ""
  read -rp "Menüye dönmek için Enter'a bas..."
done
