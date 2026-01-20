import os
import requests
import re
from datetime import datetime, timezone, timedelta

# =======================================================
# [사용자 설정 영역]
# =======================================================

# 노션에 정리된 데이터베이스의 페이지가 저장될 최상위 폴더 
SAVE_DIR_ROOT = "TIL" 

# 노션 데이터베이스의 제목 컬럼
# DataBase 네이밍 변경하지 않는 이상 바꾸시면 안됩니다.
NOTION_PROPERTY_TITLE = "제목"

# 노션 데이터베이스의 날짜 컬럼
# DataBase 네이밍 변경하지 않는 이상 바꾸시면 안됩니다.
NOTION_PROPERTY_DATE = "날짜"

README_FILE = "README.md"        # 최상위 Readme 이름

MARKER_START = "<!-- Daily Link Start -->"
MARKER_END = "<!-- Daily Link End -->"

# 한국시간 기준 설정을 위한 Timezone_Hours
TIMEZONE_HOURS = 9 


# =======================================================
# [시스템 설정]
# =======================================================
NOTION_TOKEN = os.environ['NOTION_TOKEN']
DATABASE_ID = os.environ['NOTION_DATABASE_ID']

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_page_blocks(page_id):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    response = requests.get(url, headers=headers)
    return response.json().get('results', [])

def extract_text_from_rich_text(rich_text_list):
    content = ""
    for text in rich_text_list:
        plain = text['plain_text']
        href = text.get('href')
        if href:
            content += f"[{plain}]({href})"
        else:
            content += plain
    return content

def block_to_markdown(block):
    b_type = block['type']
    if b_type in ['paragraph', 'heading_1', 'heading_2', 'heading_3', 'bulleted_list_item', 'numbered_list_item', 'to_do', 'toggle', 'quote', 'callout']:
        rich_text = block[b_type].get('rich_text', [])
        content = extract_text_from_rich_text(rich_text)
        if b_type == 'paragraph': return content + "\n\n"
        elif b_type == 'heading_1': return f"# {content}\n\n"
        elif b_type == 'heading_2': return f"## {content}\n\n"
        elif b_type == 'heading_3': return f"### {content}\n\n"
        elif b_type == 'bulleted_list_item': return f"- {content}\n"
        elif b_type == 'numbered_list_item': return f"1. {content}\n"
        elif b_type == 'to_do':
            checked = "[x]" if block['to_do']['checked'] else "[ ]"
            return f"- {checked} {content}\n"
        elif b_type == 'quote': return f"> {content}\n\n"
        elif b_type == 'callout': return f"> 💡 {content}\n\n"
        elif b_type == 'toggle': return f"- ▶ {content}\n"
    elif b_type == 'code':
        language = block['code'].get('language', 'text')
        rich_text = block['code'].get('rich_text', [])
        content = extract_text_from_rich_text(rich_text)
        return f"```{language}\n{content}\n```\n\n"
    elif b_type == 'image':
        url = block['image'].get('file', {}).get('url') or block['image'].get('external', {}).get('url') or ""
        return f"![Image]({url})\n\n"
    elif b_type == 'divider': return "---\n\n"

    # 추가 시작 
    elif b_type == 'table':
        rows = get_page_blocks(block['id'])
        table_rows = []
    
        for row in rows:
            if row['type'] == 'table_row':
                cells = row['table_row']['cells']
                row_text = [
                    extract_text_from_rich_text(cell).strip() if cell else ""
                    for cell in cells
                ]
                table_rows.append(row_text)
    
        if not table_rows:
            return ""
    
        markdown = "\n"
    
        # 헤더
        markdown += "| " + " | ".join(table_rows[0]) + " |\n"
        markdown += "| " + " | ".join(["---"] * len(table_rows[0])) + " |\n"
    
        # 본문
        for row in table_rows[1:]:
            markdown += "| " + " | ".join(row) + " |\n"
    
        markdown += "\n"   # ⭐ 이 줄이 핵심 (표 끝 줄바꿈)
    
        return markdown



    #추가 끝

    return ""

def sanitize_filename(title):
    clean_name = re.sub(r'[\\/*?:"<>|]', "", title)
    clean_name = clean_name.replace(" ", "_")
    return clean_name

def save_as_markdown(page, date_str):
    page_id = page['id']
    try:
        title = page['properties'][NOTION_PROPERTY_TITLE]['title'][0]['text']['content']
    except:
        title = "제목없음"
    
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    year = date_obj.strftime("%Y")
    month = date_obj.strftime("%m")
    
    directory = f"{SAVE_DIR_ROOT}/{year}/{month}"
    os.makedirs(directory, exist_ok=True)
    
    safe_title = sanitize_filename(title)
    filename = f"{directory}/{date_str}_{safe_title}.md"
    
    blocks = get_page_blocks(page_id)
    markdown_content = f"# {title}\n\n"
    markdown_content += f"> 날짜: {date_str}\n"
    markdown_content += f"> 원본 노션: [링크]({page['url']})\n\n"
    markdown_content += "---\n\n"
    
    for block in blocks:
        markdown_content += block_to_markdown(block)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    return title, filename

def update_main_readme_by_scanning():
    if not os.path.exists(SAVE_DIR_ROOT):
        return

    files_data = []
    for root, dirs, files in os.walk(SAVE_DIR_ROOT):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                date_str = file[:10]
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                except:
                    continue
                
                title_part = file[11:-3].replace("_", " ")
                files_data.append({
                    "date": date_obj,
                    "date_str": date_str,
                    "title": title_part,
                    "path": path
                })

    files_data.sort(key=lambda x: x["date"], reverse=True)

    grouped = {}
    for item in files_data:
        month_key = item["date"].strftime("%Y년 %m월")
        if month_key not in grouped:
            grouped[month_key] = []
        grouped[month_key].append(item)

    new_content = ""
    for i, (month, items) in enumerate(grouped.items()):
        if i == 0:
            new_content += f"### {month}\n"
            for item in items:
                safe_path = item["path"].replace(" ", "%20")
                new_content += f"- [{item['date_str']} : {item['title']}](./{safe_path})\n"
            new_content += "\n"
        else:
            new_content += f"<details>\n"
            new_content += f"<summary>{month} ({len(items)}개)</summary>\n\n"
            for item in items:
                safe_path = item["path"].replace(" ", "%20")
                new_content += f"- [{item['date_str']} : {item['title']}](./{safe_path})\n"
            new_content += "\n</details>\n\n"

    if not os.path.exists(README_FILE):
        return

    with open(README_FILE, "r", encoding="utf-8") as f:
        readme_text = f.read()

    start_idx = readme_text.find(MARKER_START)
    end_idx = readme_text.find(MARKER_END)

    # 마커가 없으면 파일 끝에 추가 (안전장치)
    if start_idx == -1 or end_idx == -1:
        final_content = readme_text + f"\n\n{MARKER_START}\n{new_content}{MARKER_END}"
    else:
        # 기존 마커 사이의 내용을 싹 지우고, 새로 만든 리스트(new_content)로 갈아끼움
        final_content = (
            readme_text[:start_idx + len(MARKER_START)] + 
            "\n" + new_content + 
            readme_text[end_idx:]
        )

    with open(README_FILE, "w", encoding="utf-8") as f:
        f.write(final_content)

def main():
    kst = timezone(timedelta(hours=TIMEZONE_HOURS))
    target_date = (datetime.now(kst) - timedelta(days=1)).strftime("%Y-%m-%d")  #수정한 부분
    #target_date = (datetime.now(kst)).strftime("%Y-%m-%d")
    print(f"DEBUG: {target_date} (어제) 일자 글 조회 시작")
    print("=== TARGET DATE ===", target_date)
    print(DATABASE_ID)

    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {
        "filter": {
            "property": NOTION_PROPERTY_DATE,
            "date": {
                "equals": target_date  # 여기가 today에서 target_date로 바뀜!
                #"on_or_after": f"{target_date}T00:00:00",
                #"before": f"{target_date}T23:59:59"
            }
        }
    }

    res = requests.post(url, headers=headers, json=payload)
    pages = res.json().get('results', [])
    print("NOTION QUERY RESULT COUNT:", len(pages))
    
    if pages:
        for page in pages:
            title, filepath = save_as_markdown(page, target_date)
            #title, filepath = save_as_markdown(page, today)
            print(f"DEBUG: 저장 완료 - {filepath}")
            print("=== SAVED FILE ===", filepath)
    
    update_main_readme_by_scanning()

if __name__ == "__main__":
    main()
