# -*- coding: utf-8 -*-
import asyncio
from aiogram import Router, types, F
from aiogram.filters import Command
from src.config import config
from src.database.supabase_client import db
from src.services.groq_service import ai_manager
from src.services.logger_service import send_log

router = Router()

# ... (весь остальной код без изменений, главное — строка с кодировкой в начале)
