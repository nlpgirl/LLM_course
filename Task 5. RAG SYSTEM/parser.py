from bs4 import BeautifulSoup
import os
import json

def parse_article_content(file_path):
    try:
        if not os.path.exists(file_path):
            return f"Файл {file_path} не найден"
            
        # Чтение HTML из файла
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        
        content_div = soup.find('div', id='article-content')
        if not content_div:
            return "Контент не найден в файле"
            
        for elem in content_div(['script', 'style', 'nav', 'footer', 'button', 'svg', 'img']):
            elem.decompose()
            
        # Извлечение структурированного текста
        text_blocks = []
        for tag in content_div.find_all(['h1', 'h2', 'h3', 'p', 'li', 'pre', 'code']):
            if tag.name in ['h1', 'h2', 'h3']:
                text_blocks.append(f"\n{tag.get_text(strip=True)}\n{'='*40}")
            elif tag.name == 'code':
                text_blocks.append(f"```{tag.get_text(strip=True)}```")
            else:
                text_blocks.append(tag.get_text(strip=True))
                
        return '\n'.join(text_blocks)
        
    except UnicodeDecodeError:
        return f"Ошибка кодировки файла {file_path}"
    except Exception as e:
        return f"Ошибка парсинга {file_path}: {str(e)}"
    

directory = '/home/aigul/Desktop/llm_last_hw/yandex_handbook'

output_file = "handbook_articles.json"
result = {}

# Проход по файлам в директории
for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    print(f"Обработка файла: {file_path}")
    article_name = os.path.basename(file_path)[:-5]
    result[article_name] = parse_article_content(file_path)

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)