
import telebot
from PIL import Image
from io import BytesIO
import torch
from transformers import DetrImageProcessor, DetrForObjectDetection

# Инициализация модели и процессора
processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50", revision="no_timm")
model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50", revision="no_timm")

bot = telebot.TeleBot('token')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот, который может анализировать фотографии. Пожалуйста, отправьте мне фотографию, и я попробую обнаружить объекты на ней.")

# Остальной код...

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    image_stream = BytesIO(downloaded_file)
    image = Image.open(image_stream)

    # Обработка изображения и получение результатов
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

    # Отправка результатов
    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [round(i, 2) for i in box.tolist()]
        bot.reply_to(
            message,
            text=f"Обнаружен {model.config.id2label[label.item()]} с уверенностью {round(score.item(), 3)} в месте {box}"
        )

bot.polling(none_stop=True)
