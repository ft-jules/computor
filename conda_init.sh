#!/usr/bin/env bash
# bootstrap_42.sh — Installe/initialise Miniconda + env de travail, idempotent.
# Usage: ./bootstrap_42.sh [--env NAME] [--py 3.7] [--force] [--purge] [--no-open]
set -Eeuo pipefail

# ------------------------------- Defaults ------------------------------------
MINICONDA_PREFIX="${MINICONDA_PREFIX:-$HOME/goinfre/miniconda3}"
INSTALLER="${INSTALLER:-${TMPDIR:-/tmp}/miniconda.sh}"
ENV_NAME="${ENV_NAME:-${USER}-42}"
PY_VERSION="${PY_VERSION:-3.7}"
PKGS="${PKGS:-jupyter numpy pandas pycodestyle}"
OPEN_SHELL="yes"
FORCE_ENV="no"
DO_PURGE="no"

# conda cache (évite le “No space left” en stockant les archives dans /tmp)
CONDA_PKGS_DIR="${CONDA_PKGS_DIR:-/tmp/conda-pkgs-$USER}"

# ------------------------------- CLI -----------------------------------------
while [ $# -gt 0 ]; do
  case "$1" in
    --env) ENV_NAME="$2"; shift 2;;
    --py) PY_VERSION="$2"; shift 2;;
    --force) FORCE_ENV="yes"; shift;;
    --purge) DO_PURGE="yes"; shift;;
    --no-open) OPEN_SHELL="no"; shift;;
    -h|--help)
      cat <<EOF
Usage: $0 [--env NAME] [--py 3.7] [--force] [--purge] [--no-open]
Defaults:
  MINICONDA_PREFIX=$MINICONDA_PREFIX
  ENV_NAME=$ENV_NAME
  PY_VERSION=$PY_VERSION
  PKGS="$PKGS"
EOF
      exit 0;;
    *) echo "[WARN] Option inconnue: $1" >&2; shift;;
  esac
done

# ------------------------------- Colors/logs ---------------------------------
if command -v tput >/dev/null 2>&1; then
  RED="$(tput setaf 1)"; YEL="$(tput setaf 3)"; GRN="$(tput setaf 2)"; BLD="$(tput bold)"; RST="$(tput sgr0)"
else RED="";YEL="";GRN="";BLD="";RST=""; fi
info(){ printf "%s\n" "${BLD}[INFO]${RST} $*"; }
ok(){ printf "%s\n"   "${GRN}[OK]  ${RST} $*"; }
warn(){ printf "%s\n" "${YEL}[WARN]${RST} $*"; }
die(){ printf "%s\n"  "${RED}[ERR ]${RST} $*" >&2; exit 1; }

# ------------------------------- Utils ---------------------------------------
need_cmd(){ command -v "$1" >/dev/null 2>&1 || die "Commande requise absente: $1"; }
backup_file(){ [ -f "$1" ] && cp -p "$1" "$1.bak.$(date +%Y%m%d-%H%M%S)" && ok "Backup: $1.bak.*" || true; }

# On se base sur $SHELL (hérité) et non sur le processus '$$' (qui est 'bash')
current_shell(){
  case "${SHELL##*/}" in
    zsh) echo "zsh";;
    bash) echo "bash";;
    *) echo "${SHELL##*/}";;
  esac
}

rc_file_for(){
  case "$1" in
    zsh) echo "$HOME/.zshrc";;
    bash) if [ -f "$HOME/.bashrc" ]; then echo "$HOME/.bashrc"; else echo "$HOME/.bash_profile"; fi;;
    *) echo "$HOME/.profile";;
  esac
}

# ------------------------------- Purge ---------------------------------------
purge_all(){
  info "Purge complète Miniconda + env + RC prompts"
  read -r -p "Confirme en tapant 'PURGE': " ans
  [ "$ans" = "PURGE" ] || die "Annulé."

  # 1) RC: retirer conda initialize + conda-prompt block
  local SH="$(current_shell)"; local RC="$(rc_file_for "$SH")"
  for f in "$HOME/.zshrc" "$HOME/.bashrc" "$HOME/.bash_profile" "$HOME/.profile"; do
    [ -f "$f" ] || continue
    backup_file "$f"
    awk '
      BEGIN{skip=0}
      /# >>> conda initialize >>>/{skip=1}
      /# <<< conda initialize <<</{skip=0; next}
      /# >>> conda-prompt \(PyMamouth\) >>>/{skip=1}
      /# <<< conda-prompt \(PyMamouth\) <<</{skip=0; next}
      skip==0{print}
    ' "$f" > "$f.tmp" && mv "$f.tmp" "$f"
    ok "Nettoyé: $f"
  done

  # 2) conda env + miniconda + caches
  if [ -d "$MINICONDA_PREFIX" ]; then
    if [ -x "$MINICONDA_PREFIX/bin/conda" ]; then
      "$MINICONDA_PREFIX/bin/conda" env remove -n "$ENV_NAME" -y >/dev/null 2>&1 || true
    fi
    rm -rf "$MINICONDA_PREFIX"
    ok "Miniconda supprimé"
  else
    info "Miniconda déjà absent"
  fi
  rm -rf "$HOME/.conda" "$CONDA_PKGS_DIR" "$INSTALLER" "$HOME/.condarc" 2>/dev/null || true
  ok "Caches et .condarc nettoyés"
  ok "Purge terminée."
}

# ------------------------------- Installers ----------------------------------
download_miniconda(){
  local url="https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
  if [ -f "$INSTALLER" ]; then
    info "Installeur déjà présent: $INSTALLER"
  else
    info "Téléchargement Miniconda…"
    curl -fsSL "$url" -o "$INSTALLER" || die "Téléchargement échoué"
  fi
  chmod +x "$INSTALLER"
}

install_miniconda(){
  if [ -x "$MINICONDA_PREFIX/bin/conda" ]; then
    ok "Miniconda déjà installé: $MINICONDA_PREFIX"
    return
  fi
  info "Installation Miniconda dans: $MINICONDA_PREFIX"
  bash "$INSTALLER" -b -p "$MINICONDA_PREFIX" || die "Install Miniconda échouée"
  ok "Miniconda prêt"
}

conda_bin(){ echo "$MINICONDA_PREFIX/bin/conda"; }

conda_init(){
  local SH="$(current_shell)"; local RC="$(rc_file_for "$SH")"
  info "Initialisation conda pour $SH (rc: $RC)"
  # Ajouter pkgs_dirs à /tmp via .condarc pour économiser l’espace $HOME
  if [ ! -f "$HOME/.condarc" ]; then
    cat > "$HOME/.condarc" <<EOF
auto_activate_base: false
pkgs_dirs:
  - $CONDA_PKGS_DIR
EOF
    ok "Créé: ~/.condarc (auto_activate_base: false, pkgs_dirs: $CONDA_PKGS_DIR)"
  else
    info "~/.condarc existe (non modifié)"
  fi
  mkdir -p "$CONDA_PKGS_DIR"

  # conda init si pas déjà présent
  if ! grep -q "# >>> conda initialize >>>" "$RC" 2>/dev/null; then
    eval "$("$(conda_bin)" shell.$SH hook)" >/dev/null 2>&1 || true
    "$(conda_bin)" init "$SH" >/dev/null
    ok "Bloc 'conda initialize' ajouté à $RC"
  else
    ok "Bloc 'conda initialize' déjà présent dans $RC"
  fi
}

accept_tos(){
  info "Acceptation des ToS d'Anaconda..."
  # On active le 'hook' pour avoir la commande 'conda' disponible
  eval "$("$(conda_bin)" shell.$(current_shell) hook)"
  
  # On accepte les deux channels requis
  conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
  conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
  ok "ToS acceptées."
}

add_prompt_indicator(){
  local SH="$(current_shell)"; local RC="$(rc_file_for "$SH")"
  if grep -q "# >>> conda-prompt (PyMamouth) >>>" "$RC" 2>/dev/null; then
    ok "Indicateur de prompt déjà présent"
    return
  fi
  info "Ajout d’un indicateur d’environnement dans le prompt"
  backup_file "$RC"
  cat >> "$RC" <<'EOF'
# >>> conda-prompt (PyMamouth) >>>
# Affiche le nom d'env conda en vert quand il est actif, sinon rien
setopt prompt_subst 2>/dev/null || true
PROMPT='${CONDA_DEFAULT_ENV:+(%F{green}$CONDA_DEFAULT_ENV%f) }'"$PROMPT"
# <<< conda-prompt (PyMamouth) <<<
EOF
  ok "Indicateur ajouté à $RC"
}

create_or_update_env(){
  eval "$("$(conda_bin)" shell.$(current_shell) hook)"
  if conda env list | grep -E "^[[:space:]]*$ENV_NAME[[:space:]]" >/dev/null 2>&1; then
    if [ "$FORCE_ENV" = "yes" ]; then
      info "Recréation forcée de l’env: $ENV_NAME"
      conda env remove -n "$ENV_NAME" -y || true
      conda create -n "$ENV_NAME" "python=$PY_VERSION" $PKGS -y
      ok "Environnement recréé: $ENV_NAME"
    else
      ok "Environnement déjà présent: $ENV_NAME"
      info "Mise à jour des paquets essentiels (rapide)…"
      conda install -n "$ENV_NAME" $PKGS -y >/dev/null 2>&1 || true
    fi
  else
    info "Création de l’environnement: $ENV_NAME (python=$PY_VERSION)"
    conda create -n "$ENV_NAME" "python=$PY_VERSION" $PKGS -y
    ok "Environnement créé: $ENV_NAME"
  fi
}

post_checks_and_open(){
  eval "$("$(conda_bin)" shell.$(current_shell) hook)"
  conda activate "$ENV_NAME"
  python - <<'PY'
import sys; print(f"[READY] Python", sys.version.split()[0])
PY
  ok "Env actif: $ENV_NAME"
  if [ "$OPEN_SHELL" = "yes" ]; then
    info "Ouverture d’un shell interactif avec l’env actif (exit pour quitter)…"
    exec "${SHELL:-/bin/zsh}" -l
  fi
}

# --------------------------------- Main --------------------------------------
main(){
  info "Paramètres:"
  info "- MINICONDA_PREFIX: $MINICONDA_PREFIX"
  info "- ENV_NAME        : $ENV_NAME"
  info "- PY_VERSION      : $PY_VERSION"
  info "- PKGS            : $PKGS"
  info "- CONDA_PKGS_DIR  : $CONDA_PKGS_DIR"

  need_cmd curl

  if [ "$DO_PURGE" = "yes" ]; then
    purge_all
    exit 0
  fi

  download_miniconda
  install_miniconda
  conda_init
  accept_tos
  
  # --- MODIFICATION ICI ---
  # On n'appelle plus cette fonction pour éviter les conflits de prompt
  # add_prompt_indicator
  
  create_or_update_env
  post_checks_and_open
}
main "$@"