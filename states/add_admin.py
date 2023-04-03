from aiogram.dispatcher.filters.state import StatesGroup,State

class Add_Admin(StatesGroup):
    admin_id = State()
    admin_name = State()