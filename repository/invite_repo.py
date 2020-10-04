from datetime import datetime

from repository.base_repository import BaseRepository
from repository.database import session
from repository.database.invites import Invite


class InviteRepository(BaseRepository):
    # unknown - pending - verified - kicked - banned

    @classmethod
    def add(
        cls,
        guild: int,
        uses: int,
        created_at: datetime,
        inviter: int,
        invite_code: str,
        revoked: bool,
    ):
        """Increment user_channel count, if it doesn't exist, create it"""
        user_channel = (
            session.query(Invite)
            .filter_by(channel_id=channel_id, user_id=user_id, guild_id=guild_id)
            .one_or_none()
        )
        if not user_channel:
            session.add(
                Invite(
                    guild_id=guild_id,
                    channel_id=channel_id,
                    user_id=user_id,
                    is_webhook=is_webhook,
                    count=count,
                    last_msg_at=last_msg_at,
                )
            )

        else:
            user_channel.count = user_channel.count + count
            if user_channel.last_msg_at < last_msg_at:
                user_channel.last_msg_at = last_msg_at

        session.commit()

    @classmethod
    def decrement(
        cls, channel_id: int, user_id: int, guild_id: int, last_msg_at: datetime,
    ):
        """Decrement user_channel count."""
        user_channel = (
            session.query(Invite)
            .filter_by(channel_id=channel_id, user_id=user_id, guild_id=guild_id)
            .one_or_none()
        )
        if not user_channel:
            session.add(
                Invite(
                    channel_id=channel_id,
                    user_id=user_id,
                    count=0,
                    last_msg_at=last_msg_at,
                    guild_id=guild_id,
                )
            )

        else:
            user_channel.count = user_channel.count - 1
            if user_channel.last_msg_at < last_msg_at:
                user_channel.last_msg_at = last_msg_at

        session.commit()

    @classmethod
    def get_user_channels(cls):
        """Retrieves the whole table"""
        return session.query(Invite).all()

    @classmethod
    def get_channel(cls, channel_id: int):
        """Retrieves table, filtered by channel id"""
        return session.query(Invite).filter_by(channel_id=channel_id).all()

    @classmethod
    def get_user(cls, user_id: int):
        """Retrieves table, filtered by user id"""
        return session.query(Invite).filter_by(user_id=user_id).all()
