import vkquick
from src.message_handlers import success_text

from src.misc import default_package


platforms = {
    1: "Мобильной версии",
    2: "Приложения для iPhone",
    3: "Приложения для iPad",
    4: "Приложения для Android",
    5: "Приложения для Windows Phone",
    6: "Приложения для Windows 10",
    7: "Полной версии сайта"
}


@default_package.command("вкинфо")
async def info(context: vkquick.NewMessage,
               user: vkquick.User = None):

    user_fields = "photo_id, verified, sex, bdate, city, country, home_town," \
                  " has_photo, photo_50, photo_100, photo_200_orig, photo_200," \
                  " photo_400_orig, photo_max, photo_max_orig, online, domain," \
                  " has_mobile, contacts, site, education, universities, schools," \
                  " status, last_seen, followers_count, common_count, occupation," \
                  " nickname, relatives, relation, personal, connections, exports" \
                  ", activities, interests, music, movies, tv, books, games," \
                  " about, quotes, can_post, can_see_all_posts, can_see_audio," \
                  " can_write_private_message, can_send_friend_request, is_favorite," \
                  " is_hidden_from_feed, timezone, screen_name, maiden_name, crop_photo," \
                  " is_friend, friend_status, career, military, blacklisted, blacklisted_by_me, can_be_invited_group."

    user = await vkquick.User.fetch_one(context.api, context.msg.from_id if not user else user.id,
                                        fields=user_fields.split(", "), name_case="abl")

    registration_date = await vkquick.get_user_registration_date(user.id)
    formatted_date = registration_date.strftime("%d.%m.%Y")
    fields = user.fields

    message = f"""
    📃 Информация о - {user:@[fullname]}

    | Цифренный ID → {fields['id']}
    | Буквенный ID → {fields['screen_name']}
    | Пол (М/Ж) → {'Мужской' if fields['sex'] == 2 else 'Женский'}
    | Вероятный город проживания → {fields.get("city", {}).get("title", "Не найден")}
    | Сейчас онлайн → {"🟢 Да" if fields['online'] else '🔴 Нет'}
    | Тип профиля → {"🔒 Закрытый" if fields['is_closed'] else '🔓 Открытый'}
    | Дата рождения → {fields.get("bdate", "Не имеется")}
    | У меня в друзьях: {"Да" if fields.get("is_friend") else "Нет"}
    | Статус: {fields.get("status", "Не имеется")[:50] or "Не имеется. "}
    | Фолловеров: {fields.get("followers_count", "Не указано. ")}
    | Страница закрыта: {"Да" if fields.get("is_closed") else "Нет"}
    | Верификация: {"Да" if fields.get("verified") else "Нет"}
    | Сейчас онлайн: {"Да" if fields.get("online") else "Нет"}
    | Виды деятельности: {fields.get("activities", "Не указаны")}
    | Религия: {fields.get("religion", "Не указана")}
    | Родные: {", ".join([str(i) for i in fields.get("relatives", ["Не имеются"])])}
    
    | Ссылка на лс: vk.me/{fields.get("screen_name")}
    | Ссылка на страницу: vk.com/{fields.get("screen_name")}
    | Короткая ссылка: vk.com/id{fields.get("id")}
    
    | Дата регистрации → {formatted_date}
    """.replace(" " * 4, "")

    await context.answer(success_text(message))
