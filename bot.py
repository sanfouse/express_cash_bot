from aiogram import executor
from loader import dp
from countries import create

if __name__ == '__main__':
  import handlers
  import database.connection
  executor.start_polling(dp)