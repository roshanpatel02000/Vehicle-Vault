import os

patterns = {
    'â‚¹': '₹',
    'â€”': '—',
    'â€“': '–',
    'â†’': '→',
    'â† ': '←',
    'â€¦': '…',
    'Â·': '·',
    'â€º': '›',
    'â–¾': '▾',
    'â–¼': '▼',
    'â€™': "'",
    'â€œ': '"',
    'â€ ': '"',
    'âœ•': '✖',
    'âœ”': '✔',
    'â–▶': '▶',
    'â—': '●',
    'â–¸': '▸',
    'âœ✨': '✨',
    'âœ¨': '✨',
    'â•': '═',
    'â•‘': '║',
    'â”€': '──',
    '—': '──',
}

target_dirs = [
    r'vehicle_vault\templates',
    r'static\css'
]

files_to_process = []
for d in target_dirs:
    full_d = os.path.join(os.getcwd(), d)
    if not os.path.exists(full_d):
        continue
    for root, _, files in os.walk(full_d):
        for f in files:
            if f.endswith(('.html', '.css')):
                files_to_process.append(os.path.join(root, f))

for file_path in files_to_process:
    try:
        with open(file_path, 'rb') as f_in:
            content_bytes = f_in.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        continue
    
    original_bytes = content_bytes
    
    # Also handle the specific sequence for â€” that might be showing as —
    # The bytes for — in some mis-encodings are often \xEF\xBF\xBD followed by \xE2\x80\x94
    
    content_str = content_bytes.decode('utf-8', errors='ignore')
    for bad, good in patterns.items():
        content_str = content_str.replace(bad, good)
    
    if content_str.encode('utf-8') != original_bytes:
        try:
            with open(file_path, 'w', encoding='utf-8') as f_out:
                f_out.write(content_str)
            print(f"Fixed encoding in {file_path}")
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
