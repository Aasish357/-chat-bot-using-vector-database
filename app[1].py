import os
import re
import tempfile
import requests
from dotenv import load_dotenv
from tools.pdf_agent import create_pdf_agent

load_dotenv()

def main():
    print("AI Agent with Gemini 1.5 Flash is ready (file QA mode).")
    file_path = os.getenv("FILE_PATH") or os.getenv("PDF_PATH")
    if not file_path:
        print("Set FILE_PATH or PDF_PATH in .env and rerun.")
        return
    file_path = file_path.strip()
    if (file_path.startswith('"') and file_path.endswith('"')) or (file_path.startswith("'") and file_path.endswith("'")):
        file_path = file_path[1:-1]
    # If it's a URL, support Drive/Docs by converting to direct/download and streaming
    if file_path.lower().startswith("http://") or file_path.lower().startswith("https://"):
        url = file_path
        drive_match = re.search(r"https?://drive\.google\.com/(?:file/d/|open\?id=)([\w-]+)", url)
        is_drive = False
        if drive_match:
            file_id = drive_match.group(1)
            url = f"https://drive.google.com/uc?export=download&id={file_id}"
            is_drive = True
        docs_match = re.search(r"https?://docs\.google\.com/document/d/([\w-]+)", url)
        is_docs = False
        if docs_match:
            doc_id = docs_match.group(1)
            url = f"https://docs.google.com/document/d/{doc_id}/export?format=pdf"
            is_docs = True
        try:
            if not (is_drive or is_docs):
                head = requests.head(url, allow_redirects=True, timeout=15)
                content_type = head.headers.get("Content-Type", "").lower()
                if "pdf" not in content_type and not url.lower().endswith(".pdf"):
                    print("The provided URL is not a direct PDF.")
                    return
            session = requests.Session()
            with session.get(url, stream=True, timeout=60) as r:
                if is_drive and "text/html" in r.headers.get("Content-Type", ""):
                    try:
                        import re as _re
                        m = _re.search(r"confirm=([0-9A-Za-z_]+)", r.text)
                        if m:
                            confirm = m.group(1)
                            confirm_url = url + ("&" if "?" in url else "?") + f"confirm={confirm}"
                            r.close()
                            r = session.get(confirm_url, stream=True, timeout=60)
                    except Exception:
                        pass
                r.raise_for_status()
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            tmp.write(chunk)
                    file_path = tmp.name
        except Exception as e:
            print(f"Failed to download PDF from URL: {e}")
            return
    else:
        if not os.path.isfile(file_path):
            print(f"File not found: {file_path}")
            return

    agent = create_pdf_agent(file_path)
    while True:
        query = input("\nAsk about the file (or 'exit'): ")
        if query.lower() == "exit":
            break
        result = agent.invoke({"query": query})
        print("\nAnswer:", result["result"])

if __name__ == "__main__":
    main()