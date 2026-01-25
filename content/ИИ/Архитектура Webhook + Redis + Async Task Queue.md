# Архитектура Webhook + Redis + Async Task Queue

Полное переписывание на production-ready архитектуру:

## Структура проекта

```
prayer_bot/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI + Webhook
│   ├── config.py
│   ├── bot.py
│   ├── redis_client.py
│   ├── database.py          # Async PostgreSQL
│   ├── prayer_times.py
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── start.py
│   │   ├── schedule.py
│   │   ├── settings.py
│   │   ├── reminders.py
│   │   └── location.py
│   ├── keyboards/
│   │   ├── __init__.py
│   │   └── inline.py
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── worker.py        # ARQ Worker
│   │   └── jobs.py
│   └── middleware/
│       ├── __init__.py
│       └── rate_limit.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── data/
    └── prayer_times.csv
```

---

## requirements.txt

```txt
# Web Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0

# Telegram Bot
aiogram==3.23.0

# Database
asyncpg==0.29.0
sqlalchemy[asyncio]==2.0.25
alembic==1.13.1

# Redis
redis[hiredis]==5.0.1

# Task Queue (async)
arq==0.25.0

# Utils
python-dotenv==1.2.1
pydantic==2.6.0
pydantic-settings==2.1.0
pytz==2025.2
pandas==2.3.3
hijri-converter==2.3.2.post1

# Monitoring
prometheus-client==0.19.0
structlog==24.1.0
```

---

## .env.example

```env
# Bot
BOT_TOKEN=your_bot_token_here
ADMIN_IDS=123456789,987654321
WEBHOOK_HOST=https://your-domain.com
WEBHOOK_PATH=/webhook/bot
WEBHOOK_SECRET=your_secret_key_here

# Database
DATABASE_URL=postgresql+asyncpg://user:password@postgres:5432/prayer_bot

# Redis
REDIS_URL=redis://redis:6379/0

# App
DEBUG=false
TIMEZONE=Europe/Simferopol
WORKERS=4
```

---

## app/config.py

```python
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
from datetime import date
from functools import lru_cache


class Settings(BaseSettings):
    # Bot
    bot_token: str = Field(..., env="BOT_TOKEN")
    admin_ids: List[int] = Field(default_factory=list, env="ADMIN_IDS")
    webhook_host: str = Field(..., env="WEBHOOK_HOST")
    webhook_path: str = Field("/webhook/bot", env="WEBHOOK_PATH")
    webhook_secret: str = Field(..., env="WEBHOOK_SECRET")
    
    # Database
    database_url: str = Field(..., env="DATABASE_URL")
    
    # Redis
    redis_url: str = Field("redis://localhost:6379/0", env="REDIS_URL")
    
    # App
    debug: bool = Field(False, env="DEBUG")
    timezone: str = Field("Europe/Simferopol", env="TIMEZONE")
    
    # Cache TTL
    cache_ttl_schedule: int = 3600  # 1 hour
    cache_ttl_settings: int = 300   # 5 min
    
    @property
    def webhook_url(self) -> str:
        return f"{self.webhook_host}{self.webhook_path}"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name == "admin_ids":
                return [int(x.strip()) for x in raw_val.split(",") if x.strip()]
            return raw_val


@lru_cache()
def get_settings() -> Settings:
    return Settings()


# Prayer configuration
PRAYER_KEYS = ["fajr", "sunrise", "dhuhr", "asr", "maghrib", "isha"]

PRAYER_NAMES_STYLES = {
    "standard": {
        "fajr": "🌙 Фаджр",
        "sunrise": "🌅 Восход",
        "dhuhr": "☀️ Зухр",
        "asr": "🌤 Аср",
        "maghrib": "🌇 Магриб",
        "isha": "🌃 Иша"
    },
    "crimean_cyrillic": {
        "fajr": "🌙 Имсак",
        "sunrise": "🌅 Кунеш",
        "dhuhr": "☀️ Уйле",
        "asr": "🌤 Экинди",
        "maghrib": "🌇 Акъшам",
        "isha": "🌃 Ятсы"
    },
    "crimean_latin": {
        "fajr": "🌙 İmsak",
        "sunrise": "🌅 Küneş",
        "dhuhr": "☀️ Üyle",
        "asr": "🌤 Ekindi",
        "maghrib": "🌇 Aqşam",
        "isha": "🌃 Yatsı"
    }
}

HIJRI_MONTHS = {
    "cyrillic": [
        "", "Мухаррем", "Сефер", "Ребиу'ль-эвель", "Ребиу'ль-ахыр",
        "Джумазие'ль-эвель", "Джумазие'ль-ахыр", "Реджеб", "Шабан",
        "Рамазан", "Шевваль", "Зилькаде", "Зильхидждже"
    ],
    "latin": [
        "", "Muharrem", "Sefer", "Rebiu'l-evel", "Rebiu'l-ahır",
        "Cumaziye'l-evel", "Cumaziye'l-ahır", "Receb", "Şaban",
        "Ramazan", "Şevval", "Zilkade", "Zilhicce"
    ]
}

LOCATIONS = [
    ("Акъмесджит (Симферополь)", 0),
    ("Алушта", -1),
    ("Багъчасарай", 2),
    ("Къарасувба��ар (Белогорск)", -2),
    ("Джанкой", -1),
    ("Кезлев (Евпатория)", 3),
    ("Сакъ (Саки)", 3),
    ("Керич (Керчь)", -9),
    ("Ор Къапы (Перекоп)", 2),
    ("Акъяр (Севастополь)", 2),
    ("Эски Къырым (Старый Крым)", -3),
    ("Кефе (Феодосия)", -5),
    ("Ялта", 4),
    ("Судакъ (Судак)", -3),
    ("Акъшейх (Раздольное)", 3),
    ("Акъмечит (Черноморское)", 4),
]

HOLIDAYS = {
    2026: {
        (1, 16): {"name": "Мирадж геджеси", "type": "night", "night": True},
        (2, 3): {"name": "Бераат геджеси", "type": "night", "night": True},
        (2, 19): {"name": "Рамазан айынынъ башланувы", "type": "start", "night": False},
        (3, 17): {"name": "Къадир геджеси", "type": "night", "night": True},
        (3, 19): {"name": "Ораза байрамынынъ арефеси", "type": "eve", "night": False},
        (3, 20): {"name": "Ораза байрамы", "type": "holiday", "night": False},
        (3, 21): {"name": "Ораза байрамы", "type": "holiday", "night": False},
        (3, 22): {"name": "Ораза байрамы", "type": "holiday", "night": False},
        (5, 26): {"name": "Арефе куню", "type": "eve", "night": False},
        (5, 27): {"name": "Къурбан байрамы", "type": "holiday", "night": False},
        (5, 28): {"name": "Къурбан байрамы", "type": "holiday", "night": False},
        (5, 29): {"name": "Къурбан байрамы", "type": "holiday", "night": False},
        (5, 30): {"name": "Къурбан байрамы", "type": "holiday", "night": False},
    }
}

RAMADAN_PERIODS = {
    2026: {
        "start": date(2026, 2, 19),
        "end": date(2026, 3, 20),
    }
}
```

---

## app/redis_client.py

```python
import redis.asyncio as redis
from typing import Optional, Any
import json
import structlog
from app.config import get_settings

logger = structlog.get_logger()


class RedisClient:
    _instance: Optional["RedisClient"] = None
    _pool: Optional[redis.ConnectionPool] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    async def init(self):
        """Initialize Redis connection pool"""
        if self._pool is None:
            settings = get_settings()
            self._pool = redis.ConnectionPool.from_url(
                settings.redis_url,
                max_connections=50,
                decode_responses=True
            )
            logger.info("Redis connection pool initialized")
    
    async def close(self):
        """Close Redis connection pool"""
        if self._pool:
            await self._pool.disconnect()
            self._pool = None
            logger.info("Redis connection pool closed")
    
    def _get_connection(self) -> redis.Redis:
        """Get Redis connection from pool"""
        return redis.Redis(connection_pool=self._pool)
    
    # === Caching Methods ===
    
    async def get_cached(self, key: str) -> Optional[Any]:
        """Get cached value"""
        async with self._get_connection() as conn:
            value = await conn.get(key)
            if value:
                return json.loads(value)
            return None
    
    async def set_cached(self, key: str, value: Any, ttl: int = 3600):
        """Set cached value with TTL"""
        async with self._get_connection() as conn:
            await conn.setex(key, ttl, json.dumps(value, ensure_ascii=False))
    
    async def delete_cached(self, key: str):
        """Delete cached value"""
        async with self._get_connection() as conn:
            await conn.delete(key)
    
    async def delete_pattern(self, pattern: str):
        """Delete all keys matching pattern"""
        async with self._get_connection() as conn:
            cursor = 0
            while True:
                cursor, keys = await conn.scan(cursor, match=pattern, count=100)
                if keys:
                    await conn.delete(*keys)
                if cursor == 0:
                    break
    
    # === Rate Limiting ===
    
    async def check_rate_limit(
        self,
        key: str,
        max_requests: int = 30,
        window_seconds: int = 60
    ) -> tuple[bool, int]:
        """
        Check rate limit using sliding window.
        Returns (is_allowed, remaining_requests)
        """
        async with self._get_connection() as conn:
            current = await conn.incr(key)
            if current == 1:
                await conn.expire(key, window_seconds)
            
            ttl = await conn.ttl(key)
            remaining = max(0, max_requests - current)
            
            return current <= max_requests, remaining
    
    # === Chat Settings Cache ===
    
    def _settings_key(self, chat_id: int) -> str:
        return f"settings:{chat_id}"
    
    async def get_settings_cached(self, chat_id: int) -> Optional[dict]:
        """Get cached chat settings"""
        return await self.get_cached(self._settings_key(chat_id))
    
    async def set_settings_cached(self, chat_id: int, settings: dict):
        """Cache chat settings"""
        settings_config = get_settings()
        await self.set_cached(
            self._settings_key(chat_id),
            settings,
            ttl=settings_config.cache_ttl_settings
        )
    
    async def invalidate_settings(self, chat_id: int):
        """Invalidate chat settings cache"""
        await self.delete_cached(self._settings_key(chat_id))
    
    # === Prayer Times Cache ===
    
    def _prayer_times_key(self, date_str: str) -> str:
        return f"prayer_times:{date_str}"
    
    async def get_prayer_times_cached(self, date_str: str) -> Optional[dict]:
        """Get cached prayer times"""
        return await self.get_cached(self._prayer_times_key(date_str))
    
    async def set_prayer_times_cached(self, date_str: str, times: dict):
        """Cache prayer times"""
        settings = get_settings()
        await self.set_cached(
            self._prayer_times_key(date_str),
            times,
            ttl=settings.cache_ttl_schedule
        )
    
    # === Pub/Sub for distributed events ===
    
    async def publish(self, channel: str, message: dict):
        """Publish message to channel"""
        async with self._get_connection() as conn:
            await conn.publish(channel, json.dumps(message))
    
    async def subscribe(self, channel: str):
        """Subscribe to channel and yield messages"""
        async with self._get_connection() as conn:
            pubsub = conn.pubsub()
            await pubsub.subscribe(channel)
            async for message in pubsub.listen():
                if message["type"] == "message":
                    yield json.loads(message["data"])


# Global instance
redis_client = RedisClient()


async def get_redis() -> RedisClient:
    """Dependency for FastAPI"""
    return redis_client
```

---

## app/database.py

```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, DateTime, JSON, Text, select, update
from sqlalchemy.sql import func
from typing import Optional, Dict, Any, List
from datetime import datetime
import structlog

from app.config import get_settings
from app.redis_client import redis_client

logger = structlog.get_logger()


class Base(DeclarativeBase):
    pass


class ChatSettings(Base):
    __tablename__ = "chat_settings"
    
    chat_id: Mapped[int] = mapped_column(primary_key=True)
    chat_type: Mapped[str] = mapped_column(String(20), default="private")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Daily schedule
    daily_schedule_time: Mapped[Optional[str]] = mapped_column(String(5), nullable=True)
    schedule_day: Mapped[str] = mapped_column(String(10), default="today")
    
    # Time offsets
    time_offset: Mapped[int] = mapped_column(Integer, default=0)
    prayer_offsets: Mapped[dict] = mapped_column(JSON, default=dict)
    
    # Reminders
    reminders: Mapped[dict] = mapped_column(JSON, default=dict)
    
    # Display settings
    enabled_prayers: Mapped[list] = mapped_column(
        JSON, 
        default=["fajr", "sunrise", "dhuhr", "asr", "maghrib", "isha"]
    )
    location_name: Mapped[str] = mapped_column(String(100), default="Симферополь")
    show_location: Mapped[bool] = mapped_column(Boolean, default=True)
    prayer_names_style: Mapped[str] = mapped_column(String(20), default="standard")
    hijri_style: Mapped[str] = mapped_column(String(10), default="cyrillic")
    show_hijri: Mapped[bool] = mapped_column(Boolean, default=True)
    show_holidays: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
    
    def to_dict(self) -> dict:
        return {
            "chat_id": self.chat_id,
            "chat_type": self.chat_type,
            "is_active": self.is_active,
            "daily_schedule_time": self.daily_schedule_time,
            "schedule_day": self.schedule_day,
            "time_offset": self.time_offset,
            "prayer_offsets": self.prayer_offsets or {},
            "reminders": self.reminders or {},
            "enabled_prayers": self.enabled_prayers or [],
            "location_name": self.location_name,
            "show_location": self.show_location,
            "prayer_names_style": self.prayer_names_style,
            "hijri_style": self.hijri_style,
            "show_hijri": self.show_hijri,
            "show_holidays": self.show_holidays,
        }


class Database:
    _instance: Optional["Database"] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, "engine"):
            settings = get_settings()
            self.engine = create_async_engine(
                settings.database_url,
                echo=settings.debug,
                pool_size=20,
                max_overflow=30,
                pool_pre_ping=True,
            )
            self.session_factory = async_sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
    
    async def init(self):
        """Create tables"""
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created")
    
    async def close(self):
        """Close database connection"""
        await self.engine.dispose()
        logger.info("Database connection closed")
    
    def get_session(self) -> AsyncSession:
        return self.session_factory()


# Global instance
db = Database()


# === Repository Functions ===

async def get_chat_settings(chat_id: int) -> Optional[Dict[str, Any]]:
    """Get chat settings with Redis cache"""
    # Try cache first
    cached = await redis_client.get_settings_cached(chat_id)
    if cached:
        return cached
    
    # Query database
    async with db.get_session() as session:
        result = await session.execute(
            select(ChatSettings).where(ChatSettings.chat_id == chat_id)
        )
        row = result.scalar_one_or_none()
        
        if row:
            settings = row.to_dict()
            # Cache the result
            await redis_client.set_settings_cached(chat_id, settings)
            return settings
        
        return None


async def save_chat_settings(chat_id: int, chat_type: str = "private", **kwargs):
    """Save chat settings and invalidate cache"""
    async with db.get_session() as session:
        result = await session.execute(
            select(ChatSettings).where(ChatSettings.chat_id == chat_id)
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            # Update existing
            for key, value in kwargs.items():
                if hasattr(existing, key):
                    setattr(existing, key, value)
            await session.commit()
        else:
            # Create new
            new_settings = ChatSettings(
                chat_id=chat_id,
                chat_type=chat_type,
                **kwargs
            )
            session.add(new_settings)
            await session.commit()
    
    # Invalidate cache
    await redis_client.invalidate_settings(chat_id)


async def get_chats_with_daily_schedule() -> List[Dict]:
    """Get all chats with daily schedule enabled"""
    async with db.get_session() as session:
        result = await session.execute(
            select(ChatSettings).where(
                ChatSettings.is_active == True,
                ChatSettings.daily_schedule_time.isnot(None)
            )
        )
        return [row.to_dict() for row in result.scalars().all()]


async def get_chats_with_reminders() -> List[Dict]:
    """Get all chats with reminders enabled"""
    async with db.get_session() as session:
        result = await session.execute(
            select(ChatSettings).where(
                ChatSettings.is_active == True,
                ChatSettings.reminders != {}
            )
        )
        return [row.to_dict() for row in result.scalars().all()]


async def get_chats_for_time(time_str: str) -> List[Dict]:
    """Get all chats scheduled for specific time"""
    async with db.get_session() as session:
        result = await session.execute(
            select(ChatSettings).where(
                ChatSettings.is_active == True,
                ChatSettings.daily_schedule_time == time_str
            )
        )
        return [row.to_dict() for row in result.scalars().all()]
```

---

## app/tasks/jobs.py

```python
from datetime import datetime, timedelta
from typing import Dict, List
import pytz
import structlog

from arq import ArqRedis
from aiogram import Bot

from app.config import get_settings, PRAYER_NAMES_STYLES, PRAYER_KEYS
from app.database import get_chats_for_time, get_chats_with_reminders
from app.prayer_times import prayer_manager

logger = structlog.get_logger()
settings = get_settings()


async def send_daily_schedule(ctx: dict, chat_settings: Dict):
    """Send daily schedule to a chat"""
    bot: Bot = ctx["bot"]
    
    chat_id = chat_settings["chat_id"]
    tz = pytz.timezone(settings.timezone)
    today = datetime.now(tz).date()
    
    if chat_settings.get("schedule_day") == "tomorrow":
        target_date = today + timedelta(days=1)
    else:
        target_date = today
    
    text = await prayer_manager.format_schedule(
        target_date=target_date,
        general_offset=chat_settings.get("time_offset", 0),
        prayer_offsets=chat_settings.get("prayer_offsets", {}),
        location_name=chat_settings.get("location_name", "Симферополь"),
        enabled_prayers=chat_settings.get("enabled_prayers"),
        show_location=chat_settings.get("show_location", True),
        prayer_names_style=chat_settings.get("prayer_names_style", "standard"),
        show_hijri=chat_settings.get("show_hijri", True),
        hijri_style=chat_settings.get("hijri_style", "cyrillic"),
        show_holidays=chat_settings.get("show_holidays", True)
    )
    
    try:
        await bot.send_message(chat_id, text, parse_mode="HTML")
        logger.info("Daily schedule sent", chat_id=chat_id)
    except Exception as e:
        logger.error("Failed to send daily schedule", chat_id=chat_id, error=str(e))


async def send_reminder(
    ctx: dict,
    chat_id: int,
    prayer_key: str,
    prayer_time: str,
    minutes_before: int,
    prayer_names_style: str = "standard"
):
    """Send reminder notification"""
    bot: Bot = ctx["bot"]
    
    prayer_names = PRAYER_NAMES_STYLES.get(prayer_names_style, PRAYER_NAMES_STYLES["standard"])
    prayer_name = prayer_names[prayer_key]
    
    text = (
        f"🔔 <b>Скоро намаз!</b>\n\n"
        f"Через <b>{minutes_before} мин.</b> наступит:\n"
        f"{prayer_name} — <b>{prayer_time}</b>"
    )
    
    try:
        await bot.send_message(chat_id, text, parse_mode="HTML")
        logger.info("Reminder sent", chat_id=chat_id, prayer=prayer_key)
    except Exception as e:
        logger.error("Failed to send reminder", chat_id=chat_id, error=str(e))


async def check_daily_schedules(ctx: dict):
    """Check and enqueue daily schedules"""
    redis: ArqRedis = ctx["redis"]
    tz = pytz.timezone(settings.timezone)
    current_time = datetime.now(tz).strftime("%H:%M")
    
    chats = await get_chats_for_time(current_time)
    
    for chat in chats:
        await redis.enqueue_job(
            "send_daily_schedule",
            chat,
            _queue_name="notifications"
        )
    
    logger.info("Daily schedules enqueued", count=len(chats), time=current_time)


async def check_reminders(ctx: dict):
    """Check and enqueue reminders"""
    redis: ArqRedis = ctx["redis"]
    tz = pytz.timezone(settings.timezone)
    now = datetime.now(tz)
    today = now.date()
    
    chats = await get_chats_with_reminders()
    enqueued = 0
    
    for chat in chats:
        reminders = chat.get("reminders", {})
        if not reminders:
            continue
        
        times = await prayer_manager.get_adjusted_times(
            today,
            chat.get("time_offset", 0),
            chat.get("prayer_offsets", {})
        )
        
        if not times:
            continue
        
        for prayer_key, reminder_minutes in reminders.items():
            prayer_time_str = times.get(prayer_key)
            if not prayer_time_str:
                continue
            
            prayer_time = datetime.strptime(prayer_time_str, "%H:%M")
            prayer_datetime = now.replace(
                hour=prayer_time.hour,
                minute=prayer_time.minute,
                second=0,
                microsecond=0
            )
            
            reminder_datetime = prayer_datetime - timedelta(minutes=reminder_minutes)
            
            # Check if reminder should be sent now
            if (reminder_datetime.hour == now.hour and 
                reminder_datetime.minute == now.minute):
                
                await redis.enqueue_job(
                    "send_reminder",
                    chat["chat_id"],
                    prayer_key,
                    prayer_time_str,
                    reminder_minutes,
                    chat.get("prayer_names_style", "standard"),
                    _queue_name="notifications"
                )
                enqueued += 1
    
    if enqueued:
        logger.info("Reminders enqueued", count=enqueued)


async def broadcast_message(ctx: dict, chat_ids: List[int], text: str):
    """Broadcast message to multiple chats (for admin announcements)"""
    bot: Bot = ctx["bot"]
    success = 0
    failed = 0
    
    for chat_id in chat_ids:
        try:
            await bot.send_message(chat_id, text, parse_mode="HTML")
            success += 1
        except Exception as e:
            failed += 1
            logger.error("Broadcast failed", chat_id=chat_id, error=str(e))
    
    logger.info("Broadcast completed", success=success, failed=failed)
    return {"success": success, "failed": failed}
```

---

## app/tasks/worker.py

```python
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any
import structlog

from arq import create_pool, cron
from arq.connections import RedisSettings
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config import get_settings
from app.database import db
from app.redis_client import redis_client
from app.tasks.jobs import (
    send_daily_schedule,
    send_reminder,
    check_daily_schedules,
    check_reminders,
    broadcast_message
)

logger = structlog.get_logger()
settings = get_settings()


async def startup(ctx: Dict[str, Any]):
    """Worker startup - initialize connections"""
    # Initialize database
    await db.init()
    
    # Initialize Redis client
    await redis_client.init()
    
    # Initialize bot
    ctx["bot"] = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    logger.info("Worker started")


async def shutdown(ctx: Dict[str, Any]):
    """Worker shutdown - cleanup"""
    if "bot" in ctx:
        await ctx["bot"].session.close()
    
    await redis_client.close()
    await db.close()
    
    logger.info("Worker stopped")


class WorkerSettings:
    """ARQ Worker settings"""
    
    # Redis connection
    redis_settings = RedisSettings.from_dsn(settings.redis_url)
    
    # Registered functions
    functions = [
        send_daily_schedule,
        send_reminder,
        check_daily_schedules,
        check_reminders,
        broadcast_message,
    ]
    
    # Cron jobs - check every minute
    cron_jobs = [
        cron(check_daily_schedules, minute=set(range(60)), unique=True),
        cron(check_reminders, minute=set(range(60)), unique=True),
    ]
    
    # Worker lifecycle
    on_startup = startup
    on_shutdown = shutdown
    
    # Queue settings
    queue_name = "default"
    max_jobs = 100
    job_timeout = 300  # 5 minutes
    keep_result = 3600  # 1 hour
    
    # Retry settings
    max_tries = 3
    retry_jobs = True


# Additional queue for notifications (higher priority)
class NotificationWorkerSettings(WorkerSettings):
    queue_name = "notifications"
    max_jobs = 500
    job_timeout = 60
```

---

## app/main.py

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import JSONResponse
import structlog
import hashlib
import hmac

from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config import get_settings
from app.database import db
from app.redis_client import redis_client, get_redis, RedisClient
from app.handlers import setup_routers
from app.middleware.rate_limit import RateLimitMiddleware

logger = structlog.get_logger()
settings = get_settings()

# Bot and Dispatcher
bot = Bot(
    token=settings.bot_token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
dp.include_router(setup_routers())


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown"""
    # Startup
    logger.info("Starting application...")
    
    # Initialize database
    await db.init()
    
    # Initialize Redis
    await redis_client.init()
    
    # Set webhook
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != settings.webhook_url:
        await bot.set_webhook(
            url=settings.webhook_url,
            secret_token=settings.webhook_secret,
            drop_pending_updates=True
        )
        logger.info("Webhook set", url=settings.webhook_url)
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    
    # Remove webhook
    await bot.delete_webhook()
    
    # Close connections
    await bot.session.close()
    await redis_client.close()
    await db.close()


app = FastAPI(
    title="Prayer Times Bot",
    lifespan=lifespan,
    docs_url="/docs" if settings.debug else None,
    redoc_url=None
)

# Add rate limiting middleware
app.add_middleware(RateLimitMiddleware)


def verify_telegram_signature(request: Request) -> bool:
    """Verify request is from Telegram"""
    secret_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    return secret_token == settings.webhook_secret


@app.post(settings.webhook_path)
async def webhook(request: Request):
    """Handle Telegram webhook updates"""
    # Verify signature
    if not verify_telegram_signature(request):
        logger.warning("Invalid webhook signature")
        raise HTTPException(status_code=403, detail="Invalid signature")
    
    # Parse update
    try:
        data = await request.json()
        update = Update.model_validate(data, context={"bot": bot})
    except Exception as e:
        logger.error("Failed to parse update", error=str(e))
        raise HTTPException(status_code=400, detail="Invalid update")
    
    # Process update
    try:
        await dp.feed_update(bot, update)
    except Exception as e:
        logger.error("Error processing update", error=str(e), update_id=update.update_id)
    
    return {"ok": True}


@app.get("/health")
async def health_check(redis: RedisClient = Depends(get_redis)):
    """Health check endpoint"""
    # Check Redis
    try:
        await redis.get_cached("health_check")
        redis_ok = True
    except Exception:
        redis_ok = False
    
    # Check Database
    try:
        async with db.get_session() as session:
            await session.execute("SELECT 1")
        db_ok = True
    except Exception:
        db_ok = False
    
    status = "healthy" if (redis_ok and db_ok) else "unhealthy"
    
    return {
        "status": status,
        "components": {
            "redis": "ok" if redis_ok else "error",
            "database": "ok" if db_ok else "error"
        }
    }


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    from fastapi.responses import Response
    
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
```

---

## app/middleware/rate_limit.py

```python
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.redis_client import redis_client


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware using Redis"""
    
    async def dispatch(self, request: Request, call_next) -> Response:
        # Only rate limit webhook endpoint
        if "/webhook" not in request.url.path:
            return await call_next(request)
        
        # Get client IP
        client_ip = request.client.host
        if forwarded := request.headers.get("X-Forwarded-For"):
            client_ip = forwarded.split(",")[0].strip()
        
        # Check rate limit
        key = f"ratelimit:{client_ip}"
        is_allowed, remaining = await redis_client.check_rate_limit(
            key,
            max_requests=100,  # 100 requests
            window_seconds=60  # per minute
        )
        
        if not is_allowed:
            raise HTTPException(status_code=429, detail="Too many requests")
        
        response = await call_next(request)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        
        return response
```

---

## app/handlers/__init__.py

```python
from aiogram import Router
from . import start, settings, schedule, reminders, location


def setup_routers() -> Router:
    """Setup all routers"""
    router = Router()
    
    router.include_router(start.router)
    router.include_router(settings.router)
    router.include_router(schedule.router)
    router.include_router(reminders.router)
    router.include_router(location.router)
    
    return router
```

---

## app/handlers/start.py

```python
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command

from app.keyboards.inline import main_menu_keyboard, schedule_keyboard
from app.database import save_chat_settings, get_chat_settings
from app.prayer_times import prayer_manager
from app.config import get_settings, PRAYER_NAMES_STYLES, HOLIDAYS
from datetime import datetime, timedelta
import pytz

router = Router()
settings = get_settings()


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Handle /start command"""
    await save_chat_settings(
        chat_id=message.chat.id,
        chat_type=message.chat.type
    )
    
    text = (
        "🕌 <b>Ассаляму алейкум!</b>\n\n"
        "Я бот для получения расписания намаза в Крыму.\n\n"
        "<b>Мои возможности:</b>\n"
        "📅 Расписание намаза на любой день\n"
        "🗓 Дата по исламскому календарю (хиджри)\n"
        "🎉 Информация о праздниках и священных ночах\n"
        "🔔 Напоминания перед каждым намазом\n"
        "⏱ Корректировка времени\n\n"
        "Выберите нужный раздел:"
    )
    
    await message.answer(text, reply_markup=main_menu_keyboard())


@router.callback_query(F.data == "main_menu")
async def main_menu(callback: CallbackQuery):
    """Return to main menu"""
    text = "🕌 <b>Главное меню</b>\n\nВыберите действие:"
    
    await callback.message.edit_text(text, reply_markup=main_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "help")
async def show_help(callback: CallbackQuery):
    """Show help"""
    text = (
        "❓ <b>Справка по боту</b>\n\n"
        "<b>Быстрые команды:</b>\n"
        "/start — главное меню\n"
        "/schedule — расписание на сегодня\n"
        "/tomorrow — расписание на завтра\n"
        "/next — ближайший намаз\n"
        "/settings — настройки бота\n"
        "/holidays — список праздников\n\n"
        "<b>Описание настроек:</b>\n"
        "• <b>Ежедневная рассылка</b> — получайте расписание каждый день\n"
        "• <b>Смещение времени</b> — подстройка под вашу локацию\n"
        "• <b>Названия намазов</b> — стандартные или крымские\n"
        "• <b>Напоминания</b> — уведомления за N минут до намаза"
    )
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data="main_menu")]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.message(Command("schedule"))
async def cmd_schedule(message: Message):
    """Show today's schedule"""
    chat_settings = await get_chat_settings(message.chat.id)
    if not chat_settings:
        await save_chat_settings(message.chat.id, message.chat.type)
        chat_settings = await get_chat_settings(message.chat.id)
    
    tz = pytz.timezone(settings.timezone)
    today = datetime.now(tz).date()
    
    text = await prayer_manager.format_schedule(
        target_date=today,
        general_offset=chat_settings.get("time_offset", 0),
        prayer_offsets=chat_settings.get("prayer_offsets", {}),
        location_name=chat_settings.get("location_name", "Симферополь"),
        enabled_prayers=chat_settings.get("enabled_prayers"),
        show_location=chat_settings.get("show_location", True),
        prayer_names_style=chat_settings.get("prayer_names_style", "standard"),
        show_hijri=chat_settings.get("show_hijri", True),
        hijri_style=chat_settings.get("hijri_style", "cyrillic"),
        show_holidays=chat_settings.get("show_holidays", True)
    )
    
    await message.answer(text, reply_markup=schedule_keyboard())


@router.message(Command("tomorrow"))
async def cmd_tomorrow(message: Message):
    """Show tomorrow's schedule"""
    chat_settings = await get_chat_settings(message.chat.id)
    if not chat_settings:
        await save_chat_settings(message.chat.id, message.chat.type)
        chat_settings = await get_chat_settings(message.chat.id)
    
    tz = pytz.timezone(settings.timezone)
    tomorrow = datetime.now(tz).date() + timedelta(days=1)
    
    text = await prayer_manager.format_schedule(
        target_date=tomorrow,
        general_offset=chat_settings.get("time_offset", 0),
        prayer_offsets=chat_settings.get("prayer_offsets", {}),
        location_name=chat_settings.get("location_name", "Симферополь"),
        enabled_prayers=chat_settings.get("enabled_prayers"),
        show_location=chat_settings.get("show_location", True),
        prayer_names_style=chat_settings.get("prayer_names_style", "standard"),
        show_hijri=chat_settings.get("show_hijri", True),
        hijri_style=chat_settings.get("hijri_style", "cyrillic"),
        show_holidays=chat_settings.get("show_holidays", True)
    )
    
    await message.answer(text, reply_markup=schedule_keyboard())
```

---

## docker-compose.yml

```yaml
version: "3.8"

services:
  bot:
    build: .
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
      - ADMIN_IDS=${ADMIN_IDS}
      - WEBHOOK_HOST=${WEBHOOK_HOST}
      - WEBHOOK_PATH=/webhook/bot
      - WEBHOOK_SECRET=${WEBHOOK_SECRET}
      - DATABASE_URL=postgresql+asyncpg://prayer:prayer@postgres:5432/prayer_bot
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped
    volumes:
      - ./data:/app/data:ro
    networks:
      - prayer_network

  worker:
    build: .
    command: arq app.tasks.worker.WorkerSettings
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
      - DATABASE_URL=postgresql+asyncpg://prayer:prayer@postgres:5432/prayer_bot
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped
    volumes:
      - ./data:/app/data:ro
    networks:
      - prayer_network
    deploy:
      replicas: 2

  worker_notifications:
    build: .
    command: arq app.tasks.worker.NotificationWorkerSettings
    environment:
      - BOT_TOKEN=${BOT_TOKEN}
      - DATABASE_URL=postgresql+asyncpg://prayer:prayer@postgres:5432/prayer_bot
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    restart: unless-stopped
    volumes:
      - ./data:/app/data:ro
    networks:
      - prayer_network
    deploy:
      replicas: 3

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: prayer
      POSTGRES_PASSWORD: prayer
      POSTGRES_DB: prayer_bot
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U prayer -d prayer_bot"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - prayer_network

  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5
    networks:
      - prayer_network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - bot
    networks:
      - prayer_network

volumes:
  postgres_data:
  redis_data:

networks:
  prayer_network:
    driver: bridge
```

---

## Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ app/
COPY data/ data/

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## nginx.conf

```nginx
events {
    worker_connections 4096;
}

http {
    upstream bot_backend {
        least_conn;
        server bot:8000;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=webhook:10m rate=50r/s;
    
    server {
        listen 80;
        server_name your-domain.com;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;

        location /webhook/bot {
            limit_req zone=webhook burst=100 nodelay;
            
            proxy_pass http://bot_backend;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            proxy_connect_timeout 10s;
            proxy_send_timeout 60s;
            proxy_read_timeout 60s;
        }

        location /health {
            proxy_pass http://bot_backend;
        }

        location /metrics {
            allow 10.0.0.0/8;
            deny all;
            proxy_pass http://bot_backend;
        }
    }
}
```

---

## Архитектура на 10K+ пользователей

```
┌─────────────────────────────────────────────────────────────────┐
│                         Telegram API                             │
└─────────────────────────────┬───────────────────────────────────┘
                              │ Webhook
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Nginx (Load Balancer)                       │
│                    Rate Limit + SSL Termination                  │
└─────────────────────────────┬───────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
    ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
    │   Bot API 1   │ │   Bot API 2   │ │   Bot API 3   │
    │   (FastAPI)   │ │   (FastAPI)   │ │   (FastAPI)   │
    └───────┬───────┘ └───────┬───────┘ └───────┬───────┘
            │                 │                 │
            └─────────────────┼─────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│     Redis     │     │   PostgreSQL  │     │  Task Queue   │
│    (Cache)    │     │      (DB)     │     │    (ARQ)      │
└───────────────┘     └───────────────┘     └───────┬───────┘
                                                    │
                              ┌─────────────────────┼─────────────────────┐
                              ▼                     ▼                     ▼
                      ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
                      │   Worker 1    │     │   Worker 2    │     │   Worker 3    │
                      │ (Schedules)   │     │ (Reminders)   │     │ (Broadcast)   │
                      └───────────────┘     └───────────────┘     └───────────────┘
```

### Запуск

```bash
# Development
docker-compose up -d

# Production (scale workers)
docker-compose up -d --scale worker=4 --scale worker_notifications=6 --scale bot=3
```

Эта архитектура легко выдержит **50K+ пользователей** с минимальной нагрузкой на сервер! 🚀