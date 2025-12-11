# ComputorV2

Étape 1 : Les Fondations Mathématiques (src/core/)
Le sujet est clair : tu dois créer tes propres types.

Code la classe Rational (gère 1/3 + 2/3).

Code la classe Complex (gère 1+2i * 3i).

Code la classe Matrix (gère multiplication matricielle).

Test : Fais des petits scripts pour vérifier que Matrix * Matrix fonctionne avant de penser au parsing.

Étape 2 : Le Lexer (src/lexer/)
Définir la liste des tokens (+, -, *, /, %, ^, =, ?, [, ], (, ), ;, ,, ID, NUM).

Transformer une string en liste de tokens.

Gérer les cas tordus comme 4i (nombre imaginaire) vs 4*i (multiplication).

Étape 3 : Le Parser Basique (src/parser/)
Construire l'AST pour des opérations simples : 1 + 2 * 3.

Gérer la priorité des opérateurs (la multiplication gagne sur l'addition).

Étape 4 : L'Interpréteur Basique (src/interpreter/)
Parcourir l'AST pour calculer le résultat de 1 + 2 * 3.

Connecter tes classes (Rational/Complex) au résultat.

Étape 5 : Variables et Environnement
Ajouter le support de varA = ....

Créer la classe Environment (un gros dictionnaire) pour stocker les variables.

Gérer la réassignation.

Étape 6 : Fonctions et Résolution (?)
C'est le boss final. Gérer f(x) = x^2 et f(2) = ?.

Gérer la simplification symbolique (2 * x reste 2 * x si x n'est pas défini).
