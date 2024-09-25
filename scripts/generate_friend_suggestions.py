import os
from sqlalchemy import create_engine, text, func


engine = create_engine(os.getenv("DATABASE_URI"), echo=True)


with engine.connect() as conn:
    # remove all people_you_know
    conn.execute(text("DELETE FROM account_user_people_you_may_know"))

    users = conn.execute(text("SELECT id FROM account_user"))
    users = {_user.id for _user in users}

    fiends = conn.execute(text("SELECT creator_id, target_id FROM account_friend"))
    friends_dict = {_user_id: set() for _user_id in users}
    for friend in fiends:
        friends_dict[friend.creator_id].add(friend.target_id)
        friends_dict[friend.target_id].add(friend.creator_id)

    friend_suggestions_dict = {_user_id: set() for _user_id in users}

    for user_id in users:
        for friend in friends_dict[user_id]:
            for friend_friend in friends_dict[friend]:
                if friend_friend != user_id and user_id not in friend_suggestions_dict[friend_friend]:
                    friend_suggestions_dict[user_id].add(friend_friend)
                    conn.execute(text("INSERT INTO account_user_people_you_may_know (creator_id, target_id) VALUES (:creator_id, :target_id)"), {"creator_id": user_id, "target_id": friend_friend})

    conn.commit()
