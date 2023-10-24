#!/bin/bash

# Répertoire où se trouvent les fichiers de test
TEST_DIR="./Test"

# Parcourir tous les fichiers .txt dans le répertoire de test
for txt_file in $TEST_DIR/*.txt; do
    # Retirer le chemin et l'extension pour obtenir seulement le nom du fichier
    base_name=$(basename -- "$txt_file")
    name_no_ext="${base_name%.*}"

    # Générer les noms de fichiers pour .moncode et .resultat
    moncode_file="$TEST_DIR/$name_no_ext.moncode"
    resultat_file="$TEST_DIR/$name_no_ext.resultat"
    out_file="$TEST_DIR/$name_no_ext.out"

    # Compiler le fichier .txt en .moncode avec Compilation.py
    python3 Compilation.py "$txt_file" > "$moncode_file"

    # Exécuter le fichier .moncode avec votre machine à états (ici, j'ai utilisé "msm" comme nom)
    ./msm/msm "$moncode_file" > "$resultat_file"

    # Comparer le résultat avec le fichier .out attendu
    if ! cmp -s "$resultat_file" "$out_file"; then
        echo "ERROR: Test failed for $name_no_ext"
    else
        echo "Test passed for $name_no_ext"
    fi
done
