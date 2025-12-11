#!/bin/bash

# Nom du dossier racine
PROJECT="computorv2"

# Couleurs pour l'affichage
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RESET='\033[0m'

echo -e "${BLUE}=== Initialisation de l'architecture $PROJECT ===${RESET}"

# Création du dossier racine
mkdir -p "$PROJECT"
cd "$PROJECT"

# Fonction pour créer un fichier Python avec une description
create_py() {
    path=$1
    desc=$2
    
    # Création du dossier parent si nécessaire
    mkdir -p "$(dirname "$path")"
    
    # Écriture de l'en-tête
    echo "\"\"\"" > "$path"
    echo "$desc" >> "$path"
    echo "\"\"\"" >> "$path"
    echo "" >> "$path"
    
    echo -e "Creating ${GREEN}$path${RESET}..."
}

# Fonction pour créer un fichier simple (non python)
create_file() {
    path=$1
    content=$2
    mkdir -p "$(dirname "$path")"
    echo -e "$content" > "$path"
    echo -e "Creating ${GREEN}$path${RESET}..."
}

# --- 1. RACINE ---
create_py "main.py" "Point d'entrée du programme. Lance le shell interactif."
create_file "requirements.txt" "# Liste des dépendances (vide pour l'instant car libs interdites)"
create_file "README.md" "# ComputorV2\n\nInterpréteur mathématique (Variables, Fonctions, Matrices, Complexes)."

# Création du Makefile (Obligatoire)
cat <<EOF > Makefile
NAME = computorv2

all:
	@echo "Python project: nothing to compile. Run with 'python3 main.py'"

run:
	python3 main.py

test:
	python3 -m unittest discover tests

clean:
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf src/*/__pycache__

fclean: clean

re: fclean all
EOF
echo -e "Creating ${GREEN}Makefile${RESET}..."

# --- 2. SOURCE (SRC) ---
create_py "src/__init__.py" "Module principal source."
create_py "src/shell.py" "Gère la boucle interactive (REPL), l'historique et la lecture des entrées utilisateur."

# --- LEXER (Découpage) ---
create_py "src/lexer/__init__.py" "Module Lexer."
create_py "src/lexer/lexer.py" "Transforme une chaîne de caractères (input) en une liste de Tokens."
create_py "src/lexer/tokens.py" "Définit les types de Tokens (ID, NUM, PLUS, EQUAL, MATRIX_START, etc.)."

# --- PARSER (Syntaxe) ---
create_py "src/parser/__init__.py" "Module Parser."
create_py "src/parser/parser.py" "Analyse la liste de tokens et construit l'AST (Abstract Syntax Tree)."
create_py "src/parser/ast_nodes.py" "Définit les nœuds de l'arbre (AssignNode, BinOpNode, FuncCallNode, etc.)."

# --- CORE (Types Mathématiques) ---
create_py "src/core/__init__.py" "Module des types mathématiques custom."
create_py "src/core/rational.py" "Classe Rational : Gère les nombres rationnels (numérateur/dénominateur)."
create_py "src/core/complex.py" "Classe Complex : Gère les nombres complexes (partie réelle + imaginaire)."
create_py "src/core/matrix.py" "Classe Matrix : Gère les opérations matricielles."
create_py "src/core/polynomial.py" "Gestion des polynômes (réutilisation améliorée de V1)."
create_py "src/core/function.py" "Classe Function : Stocke la définition d'une fonction utilisateur."

# --- INTERPRETER (Exécution) ---
create_py "src/interpreter/__init__.py" "Module Interpréteur."
create_py "src/interpreter/evaluator.py" "Parcourt l'AST et exécute les opérations mathématiques."
create_py "src/interpreter/simplifier.py" "Logique de simplification symbolique des expressions."
create_py "src/interpreter/solver.py" "Logique de résolution d'équations (le '?')."

# --- UTILS (Outils) ---
create_py "src/utils/__init__.py" "Module utilitaire."
create_py "src/utils/environment.py" "Gère la mémoire du programme (stockage des variables et fonctions)."
create_py "src/utils/errors.py" "Gestion des exceptions personnalisées (SyntaxError, MathError)."

# --- 3. TESTS ---
create_py "tests/__init__.py" "Module de tests."
create_py "tests/test_lexer.py" "Tests unitaires pour le Lexer."
create_py "tests/test_parser.py" "Tests unitaires pour le Parser."
create_py "tests/test_matrix.py" "Tests unitaires pour les opérations matricielles."
create_py "tests/test_complex.py" "Tests unitaires pour les nombres complexes."

echo -e "\n${BLUE}=== Architecture générée avec succès ! 🚀 ===${RESET}"
echo -e "Tu peux maintenant aller dans le dossier : ${GREEN}cd $PROJECT${RESET}"