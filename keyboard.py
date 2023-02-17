from vk_api.keyboard import VkKeyboard, VkKeyboardColor

vk_keyboard = VkKeyboard(one_time=False, inline=True)
vk_keyboard.add_button(label="Назад", color=VkKeyboardColor.NEGATIVE, payload={"type": "text"})
vk_keyboard.add_button(label="Далее", color=VkKeyboardColor.POSITIVE, payload={"type": "text"})
