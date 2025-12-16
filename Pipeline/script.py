import os
import re
import uuid
import time
import requests
import sys
from tqdm import tqdm
from dotenv import load_dotenv
load_dotenv()

# NEW IMPORTS
import psycopg2
from psycopg2.extras import DictCursor
import cloudinary
import cloudinary.uploader
import cloudinary.api

# ========================================================================
# CONFIGURATION (FILL THESE IN)
# ========================================================================


NEON_DB_URL = os.getenv("DATABASE_URL")
CLOUD_NAME = os.getenv("CLOUD_NAME")
CLOUD_API_KEY = os.getenv("CLOUD_API_KEY")
CLOUD_API_SECRET = os.getenv("CLOUD_API_SECRET")

# 2. CLOUDINARY CONFIGURATION
cloudinary.config( 
  cloud_name = CLOUD_NAME, 
  api_key = CLOUD_API_KEY, 
  api_secret = CLOUD_API_SECRET,
  secure = True
)

# ========================================================================
# ANSI COLORS
# ========================================================================
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"
LIGHT_RED = "\033[91;1m"
ORANGE = "\033[38;2;255;165;0m"
CYAN = "\033[96m"

# ========================================================================
# UTILS
# ========================================================================

print("Please read it carefully before proceeding:")
print(f"{ORANGE}Root Directory is the folder where all project files will be stored and processed.{RESET}")
print(f"{ORANGE}Books Directory is the folder where your markdown (.md) files are currently located.{RESET}")

def ask_yn(prompt):
    """Ask the user for y/n and force valid input."""
    while True:
        ans = input(prompt).strip().lower()
        if ans in ("y", "n"):
            return ans
        print(f"{RED}Invalid input. Enter only 'y' or 'n'.{RESET}")

def ask_choice(prompt, choices):
    """Ask the user to choose from a list of choices."""
    while True:
        ans = input(prompt).strip()
        if ans.isdigit() and int(ans) >= 0 and int(ans) <= len(choices):
            return ans
        print(f"{RED}Invalid choice. Choose from {choices}.{RESET}")

def spinner(message, duration=1.2):
    """Simple animated spinner."""
    frames = ["-", "\\", "|", "/"]
    t = time.time()
    i = 0
    while time.time() - t < duration:
        print(f"\r{message} {frames[i % len(frames)]}", end="")
        time.sleep(0.08)
        i += 1
    print("\r" + " " * 40, end="\r")

# ========================================================================
# GLOBAL VARIABLES & DIRECTORY SETUP
# ========================================================================

curr_dir = os.getcwd()
root_dir = ""

# Placeholders (will be set in Section 1)
Books = ""
CleanedBooks = ""

print("\n────────────────────────────────────────")
print(f"{CYAN}ROOT DIRECTORY CONFIGURATION{RESET}")
print("────────────────────────────────────────\n")

confirm = "n"
while confirm.lower() == "n":
    is_same = ask_yn("Use current directory as root? (y/n): ")
    if is_same.lower() == "y":
        root_dir = curr_dir
    else:
        root_dir = input("Enter root directory path: ").strip()
    
    print(f"Root directory → {root_dir}")
    confirm = ask_yn("Confirm? (y/n): ")

print(f"{GREEN}\nFinal Root Directory → {root_dir}{RESET}")

# We don't need 'Images' or 'Tables' folders anymore since we use Cloud/Neon
Books = os.path.join(root_dir, "Books")
CleanedBooks = os.path.join(root_dir, "Cleaned")

print(f"{GREEN}\nCreating folders...{RESET}\n")
for folder in [Books, CleanedBooks]:
    os.makedirs(folder, exist_ok=True)

# ========================================================================
# BOOK DIRECTORY SETUP
# ========================================================================

print("\n────────────────────────────────────────")
print(f"{CYAN}BOOK DIRECTORY CONFIGURATION{RESET}")
print("────────────────────────────────────────\n")

confirm_books = "n"
user_books = ""

while confirm_books == "n":
    is_same = ask_yn("Is your books folder same as root directory? (y/n): ")
    if is_same == "y":
        user_books = root_dir
    else:
        user_books = input("Enter books directory path: ").strip()
    
    print(f"Books directory → {user_books}")
    confirm_books = ask_yn("Confirm? (y/n): ")

print(f"{GREEN}\nMoving .md files to project folder...{RESET}\n")

def move_books(user_books):
    if user_books == Books:
        return # Skip if source is same as dest
        
    if not os.path.exists(user_books):
        print(f"{RED}Source folder does not exist.{RESET}")
        return

    files = [f for f in os.listdir(user_books) if f.endswith(".md")]
    for file in tqdm(files, desc="Copying .md files", ncols=80):
        src = os.path.join(user_books, file)
        dest = os.path.join(Books, file)
        # Avoid overwriting if same file
        if src != dest:
            os.rename(src, dest)

move_books(user_books)

# ========================================================================
# NEON DATABASE SETUP
# ========================================================================

print("\n────────────────────────────────────────")
print("NEON DB SETUP")
print("────────────────────────────────────────\n")

def get_db_connection():
    """Establishes connection to Neon Postgres."""
    try:
        conn = psycopg2.connect(NEON_DB_URL)
        return conn
    except Exception as e:
        print(f"{RED}Error connecting to Neon DB: {e}{RESET}")
        sys.exit(1)

def setup_database():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Using UUID as PRIMARY KEY
    cur.execute("""
        CREATE TABLE IF NOT EXISTS images (
            id UUID PRIMARY KEY,
            image_url TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
    print(f"{GREEN}Connected to Neon and verified table schema.{RESET}")

setup_database()

# ========================================================================
# CLEANING + CLOUDINARY UPLOAD logic
# ========================================================================

def clean_markdown(text):
    """
    1. Remove unwanted HTML tags/attributes.
    2. Convert $$ to $ for LaTeX.
    3. Remove page numbers (isolated numbers on their own lines).
    """
    # --- HTML Cleaning ---
    text = re.sub(r'\s*style="[^"]*"', '', text)
    text = re.sub(r"\s*style='[^']*'", '', text)
    text = re.sub(r'\s*width="[^"]*"', '', text)
    text = re.sub(r"\s*width='[^']*'", '', text)
    text = re.sub(r'\s*alt="[^"]*"', '', text)
    text = re.sub(r"\s*alt='[^']*'", '', text)
    text = re.sub(r'<div[^>]*>', '', text)
    text = re.sub(r'</div>', '', text)

    text = text.replace("$$", "$")# Replaces double dollar signs with single ones
    text = text.replace("\n#\n" , "\n") # Fix isolated headers
    text = text.replace("\n\d+\n" , "\n") # Fix isolated page numbers

    # --- Remove Page Numbers ---
    # This Regex matches:
    # \n       -> A new line
    # \s* -> Optional whitespace
    # \d+      -> One or more digits (the page number)
    # \s* -> Optional whitespace
    # (?=\n)   -> Lookahead for another newline (ensures it's a standalone line)
    text = re.sub(r'\n\s*\d+\s*(?=\n)', '', text)

    return text

def extract_image_urls(text):
    """Return all image src URLs."""
    return re.findall(r'<img[^>]*src="([^"]+)"[^>]*>', text)

def fix_markdown_headers(text):
    """Ensure every Markdown header (#, ##...) starts with a blank line."""
    text = re.sub(r"(?<!\n)\n?(#{1,6}\s+)", r"\n\n\1", text)
    return text

def upload_to_cloudinary_and_db(url):
    """
    1. Downloads image from Source URL.
    2. Uploads to Cloudinary.
    3. Saves record to Neon DB.
    4. Returns the UUID (for the text replacement).
    """
    # Generate UUID for Primary Key
    img_uuid = str(uuid.uuid4())
    
    try:
        # 1. Download Content
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return None
        
        image_data = r.content

        # 2. Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(
            image_data, 
            public_id=img_uuid, 
            folder="ncert_images"
        )
        
        cloudinary_url = upload_result.get("secure_url")

        # 3. Save to Neon DB
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute(
            "INSERT INTO images (id, image_url, description) VALUES (%s, %s, %s)", 
            (img_uuid, cloudinary_url, "")
        )
        conn.commit()
        cur.close()
        conn.close()

        # RETURN THE UUID (Important for your <img = uuid> requirement)
        return img_uuid

    except Exception as e:
        # print(f"{RED}Failed to process {url}: {e}{RESET}") 
        return None

def replace_urls(text, mapping):
    for old, new in mapping.items():
        text = text.replace(old, new)
    return text

def process_book(book_filename):
    input_path = os.path.join(Books, book_filename)
    book_base = os.path.splitext(book_filename)[0].split(".pdf")[0]
    output_path = os.path.join(CleanedBooks, f"{book_base}_cleaned.md")

    if os.path.exists(output_path):
        print("\nAlready processed. Skipping.\n")
        return

    # Load file
    with open(input_path, "r", encoding="utf-8") as f:
        raw = f.read()

    spinner("Cleaning markdown")
    cleaned = clean_markdown(raw)
    urls = extract_image_urls(cleaned)

    # 1. Build a Map of { URL : UUID }
    url_to_uuid = {}
    
    if urls:
        # Deduplicate list to avoid re-uploading the same image twice
        unique_urls = list(set(urls))
        
        for url in tqdm(unique_urls, desc="Processing Images", ncols=80):
            uuid_str = upload_to_cloudinary_and_db(url)
            
            if uuid_str:
                url_to_uuid[url] = uuid_str

    # 2. Replace the WHOLE tag with <img = uuid>
    def replace_tag_with_token(match):
        # match.group(1) is the URL captured by extract_image_urls regex
        url = match.group(1)
        
        if url in url_to_uuid:
            # The Magic: Replace whole tag with your custom format
            return f"<img = {url_to_uuid[url]}>"
        else:
            # If upload failed, keep original tag
            return match.group(0)

    # Re-run regex substitution on the whole text
    # This finds <img ... src="URL" ...> and runs the function above
    final_md = re.sub(r'<img[^>]*src="([^"]+)"[^>]*>', replace_tag_with_token, cleaned)

    # Fix header formatting
    final_md = fix_markdown_headers(final_md)

    # Save file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_md)

    print(f"\nOutput → {output_path}\n")

# ========================================================================
# MENU SYSTEM
# ========================================================================

def list_books():
    md_files = [f for f in os.listdir(Books) if f.endswith(".md")]
    if not md_files:
        print("No books found.")
        return None

    print("\n────────────────────────────────────────")
    print("AVAILABLE BOOKS")
    print("────────────────────────────────────────\n")
    return md_files

books = list_books()

if books:
    while True:
        for idx, b in enumerate(books):
            print(f"{YELLOW}{idx + 1}. {b}{RESET}")
        print(f"{LIGHT_RED}0. Exit{RESET}")

        choice = int(ask_choice("\nSelect book: ", [str(i) for i in range(len(books) + 1)]))

        if choice == 0:
            break

        print(f"{GREEN}\nProcessing...{RESET}\n")
        process_book(books[choice - 1])
        print(f"{GREEN}{books[choice - 1]} processed.{RESET}\n")