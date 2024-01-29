import json

def collecting_comments(data, all_comments, all_timestamps):
    for dict in data:
        all_comments.append(dict['comment'])
        all_timestamps.append(dict['date'])
        if len(dict['replies'])>0:
            collecting_comments(dict['replies'],all_comments,all_timestamps)


comments=[]
timestamps=[]

file_path = '../data/genshin_impact_data.json'
modified_file_path = '../data/modified_genshin_impact_data.json'

try:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().strip()

    # Adding square brackets and commas
    modified_content = '[' + content.replace('}\n{', '},{') + ']'

    with open(modified_file_path, 'w', encoding='utf-8') as modified_file:
        modified_file.write(modified_content)

except Exception as e:
    print("An error occurred:", e)


with open(modified_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
    for items in data:
        comments.append(items['content'])
        timestamps.append(items['date'])
        collecting_comments(items['comments'], comments, timestamps)

merged_data = [{"comment": comment, "date": timestamp} for comment, timestamp in zip(comments, timestamps)]

output = '../data/genshin_comments.json'
with open(output, 'w', encoding='utf-8') as f:
    json.dump(merged_data, f, ensure_ascii=False, indent=4)