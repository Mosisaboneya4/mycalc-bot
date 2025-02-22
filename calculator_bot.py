import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, CallbackContext

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Initialize the bot with the provided API token
API_TOKEN = "8126659191:AAFSVgie57pv0iiSUwKke6n6vbYEneHHQHw"

async def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Please enter a number (up to 3 digits):', reply_markup=number_keyboard())
    
    # Initialize user data
    context.user_data['step'] = 'first_number'
    context.user_data['first_number'] = ''
    context.user_data['second_number'] = ''
    context.user_data['operation'] = None

async def button(update: Update, context: CallbackContext) -> None:
    """Handle button presses."""
    query = update.callback_query
    await query.answer()

    step = context.user_data.get('step')

    if step == 'first_number':
        if query.data == 'done':
            context.user_data['step'] = 'second_number'
            await query.edit_message_text(text='Please enter the second number (up to 3 digits):', reply_markup=number_keyboard())
        else:
            context.user_data['first_number'] += query.data  # Append digit to the first number
            await query.edit_message_text(text=f'Current first number: {context.user_data["first_number"]}\nTap "Done" when finished.', reply_markup=number_keyboard())
    
    elif step == 'second_number':
        if query.data == 'done':
            context.user_data['step'] = 'operation'
            await query.edit_message_text(text='Choose an operation:', reply_markup=operation_keyboard())
        else:
            context.user_data['second_number'] += query.data  # Append digit to the second number
            await query.edit_message_text(text=f'Current second number: {context.user_data["second_number"]}\nTap "Done" when finished.', reply_markup=number_keyboard())

    elif step == 'operation':
        operation = query.data
        first_number = int(context.user_data.get('first_number'))
        second_number = int(context.user_data.get('second_number'))

        result = calculate_result(first_number, second_number, operation)
        await query.edit_message_text(text=f"Result: {result}")

        # Reset user data for a new calculation
        context.user_data.clear()

def calculate_result(first_number, second_number, operation):
    """Perform arithmetic operations."""
    if operation == 'add':
        return first_number + second_number
    elif operation == 'subtract':
        return first_number - second_number
    elif operation == 'multiply':
        return first_number * second_number
    elif operation == 'divide':
        return "Error: Cannot divide by zero" if second_number == 0 else first_number / second_number
    else:
        return "Invalid operation"

def number_keyboard():
    """Generate number selection keyboard with a Done button."""
    keyboard = [
        [InlineKeyboardButton(str(i), callback_data=str(i)) for i in range(0, 10)],
        [InlineKeyboardButton("Done", callback_data='done')]
    ]
    return InlineKeyboardMarkup(keyboard)

def operation_keyboard():
    """Generate operation selection keyboard."""
    keyboard = [
        [InlineKeyboardButton("Add", callback_data='add'),
         InlineKeyboardButton("Subtract", callback_data='subtract')],
        [InlineKeyboardButton("Multiply", callback_data='multiply'),
         InlineKeyboardButton("Divide", callback_data='divide')]
    ]
    return InlineKeyboardMarkup(keyboard)

def main() -> None:
    """Start the bot."""
    application = ApplicationBuilder().token(API_TOKEN).build()  # Use ApplicationBuilder

    # Register command and button handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
