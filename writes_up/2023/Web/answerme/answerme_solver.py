#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import argparse
import sys
from urllib.parse import urljoin

def get_http_status_codes(base_url, max_number=144):
    """
    Exécute des requêtes HTTP vers l'URL de base avec des nombres de 1 à max_number
    et récupère les codes de réponse HTTP.
    
    Args:
        base_url (str): L'URL de base du challenge
        max_number (int): Le nombre maximum à tester (par défaut 144)
    
    Returns:
        list: Liste des codes de réponse HTTP
    """
    status_codes = []
    
    print(f"Récupération des codes de réponse HTTP pour les nombres de 1 à {max_number}...")
    
    for i in range(1, max_number + 1):
        try:
            # Construire l'URL avec le nombre
            url = urljoin(base_url, str(i))
            
            # Effectuer la requête HEAD pour obtenir uniquement les en-têtes
            response = requests.head(url, timeout=5)
            status_codes.append(response.status_code)
            
            # Afficher la progression
            if i % 10 == 0:
                print(f"Progression: {i}/{max_number}")
                
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête pour le nombre {i}: {e}")
            # Ajouter un code par défaut en cas d'erreur
            status_codes.append(0)
    
    return status_codes

def remove_digit_two(status_codes):
    """
    Supprime le chiffre '2' de chaque code de réponse HTTP.
    
    Args:
        status_codes (list): Liste des codes de réponse HTTP
    
    Returns:
        list: Liste des codes avec le chiffre '2' supprimé
    """
    cleaned_codes = []
    
    for code in status_codes:
        # Convertir le code en chaîne et supprimer tous les '2'
        cleaned_code = str(code).replace('2', '')
        cleaned_codes.append(cleaned_code)
    
    return cleaned_codes

def create_binary_string(cleaned_codes):
    """
    Concatène les codes nettoyés pour former une chaîne binaire.
    
    Args:
        cleaned_codes (list): Liste des codes avec le chiffre '2' supprimé
    
    Returns:
        str: Chaîne binaire résultante
    """
    binary_string = ''.join(cleaned_codes)
    return binary_string

def binary_to_text(binary_string):
    """
    Convertit une chaîne binaire en texte.
    
    Args:
        binary_string (str): Chaîne binaire à convertir
    
    Returns:
        str: Texte résultant de la conversion
    """
    # Vérifier que la longueur est un multiple de 8
    if len(binary_string) % 8 != 0:
        print(f"Attention: La longueur de la chaîne binaire ({len(binary_string)}) n'est pas un multiple de 8")
        # Compléter avec des zéros si nécessaire
        padding = 8 - (len(binary_string) % 8)
        binary_string += '0' * padding
        print(f"Chaîne complétée avec {padding} zéros: {binary_string}")
    
    # Convertir la chaîne binaire en texte
    text = ''
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i+8]
        if len(byte) == 8:  # Vérifier que c'est un octet complet
            try:
                text += chr(int(byte, 2))
            except ValueError:
                print(f"Erreur de conversion pour l'octet: {byte}")
    
    return text

def main():
    parser = argparse.ArgumentParser(description="Résoudre le challenge AnswerMe")
    parser.add_argument("url", help="URL de base du challenge (ex: http://ctf2023challs.hackagou.nc:5002/)")
    parser.add_argument("--max", type=int, default=144, help="Nombre maximum à tester (par défaut: 144)")
    
    args = parser.parse_args()
    
    # Vérifier que l'URL se termine par un slash
    base_url = args.url if args.url.endswith('/') else args.url + '/'
    
    print(f"URL de base: {base_url}")
    print(f"Nombre maximum: {args.max}")
    
    # Étape 1: Récupérer les codes de réponse HTTP
    status_codes = get_http_status_codes(base_url, args.max)
    print(f"\nCodes de réponse récupérés: {status_codes}")
    
    # Étape 2: Supprimer le chiffre '2' de chaque code
    cleaned_codes = remove_digit_two(status_codes)
    print(f"\nCodes après suppression du chiffre '2': {cleaned_codes}")
    
    # Étape 3: Créer la chaîne binaire
    binary_string = create_binary_string(cleaned_codes)
    print(f"\nChaîne binaire obtenue: {binary_string}")
    print(f"Longueur de la chaîne binaire: {len(binary_string)}")
    
    # Étape 4: Convertir la chaîne binaire en texte
    flag = binary_to_text(binary_string)
    print(f"\nFlag trouvé: {flag}")

if __name__ == "__main__":
    main()