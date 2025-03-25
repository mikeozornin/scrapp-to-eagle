import json
import requests

# Загрузка данных из файла Scrapp
with open('data/scrapp/home.json', 'r', encoding='utf-8') as file:
    scrapp_data = json.load(file)

# URL Eagle API
EAGLE_SERVER_URL = "http://localhost:41595"
EAGLE_IMPORT_API_URL = f"{EAGLE_SERVER_URL}/api/item/addFromURLs"

# Функция для формирования тегов
def format_tags(screenshot_tags, all_tags):
    formatted_tags = []
    for tag_name in screenshot_tags:
        # Ищем тег в общем списке тегов
        tag_info = next((tag for tag in all_tags if tag['name'] == tag_name), None)
        if tag_info and tag_info['isPublished']:
            formatted_tags.append(f"{tag_name} (public)")
        else:
            formatted_tags.append(tag_name)
    return formatted_tags

# Перенос изображений
for screenshot in scrapp_data['screenshots']:  # Берем только один файл для отладки
    image_data = {
        "name": screenshot.get("description", ""),
        "url": screenshot["pictureUrl"],
        "website": screenshot.get("source", ""),
        "annotation": screenshot.get("description", ""),
        "tags": format_tags(screenshot.get('tags', []), scrapp_data['tags']),
        "modificationTime": screenshot['created']
    }

    # Отправка данных в Eagle
    response = requests.post(EAGLE_IMPORT_API_URL, json={"items": [image_data]})

    if response.status_code == 200:
        print("Изображение успешно перенесено:", response.json())
    else:
        print("Ошибка при переносе изображения:", response.status_code, response.text)