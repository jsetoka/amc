import os

def format_django_template(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    indent = 0
    output = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith('{% endif') or stripped.startswith('{% endfor') or stripped.startswith('{% endblock') or stripped.startswith('{% elif') or stripped.startswith('{% else %}'):
            indent -= 1

        output.append('  ' * indent + stripped + '\n')

        if (
            stripped.startswith('{% if') and not stripped.startswith('{% elif')
            or stripped.startswith('{% for')
            or stripped.startswith('{% block') and not stripped.startswith('{% end')
            or stripped.startswith('{% else %}')
        ):
            indent += 1

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(output)

    print(f"✅ Template reformatted: {file_path}")


# 🔧 Exemple d'utilisation
# Remplace le chemin par celui de ton fichier
if __name__ == "__main__":
    path = input("Chemin vers le fichier template : ")
    if os.path.exists(path):
        format_django_template(path)
    else:
        print("❌ Fichier introuvable.")
