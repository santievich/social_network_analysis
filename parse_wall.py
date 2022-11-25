import pandas as pd
import vk_api
import stop_words

vk_session = vk_api.VkApi('LOGIN', 'PASSWORD')
vk_session.auth()

text_content = dict()

for user_id in friend_ids:
    text_content[user_id] = []
    try:
        wall = vk_session.get_api().wall.get(owner_id=user_id, count = 20)
    except:
        continue
    for post in wall['items']:
        text = post['text']
        text_content[user_id].append(text)

df = pd.DataFrame(text_content.items())
df.columns = 'id', 'content'
df.set_index('id', inplace = True)

df.to_csv('messages.csv', header = True, index = True)