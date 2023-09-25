import re
import os
import cv2
import json
import openai
import requests
import pytesseract
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# Load the image using OpenCV
image = cv2.imread('card1.JPG')

# Preprocess the image
# Example: resizing and converting to grayscale
resized_image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

# Save the preprocessed image to a file
cv2.imwrite('process_card.jpg', gray_image)

# Perform OCR to extract card name
card_text = pytesseract.image_to_string(gray_image)

# Create a message with the extracted card text
messages = [
    {"role": "system", "content": "You are a helpful assistant that identifies MTG cards."},
    {"role": "user", "content": f'{card_text} #the text before this is extracted from a mtg card. Identify the set and card number. The card number should only be the specific card number not including the total number of cards in the set. Then return this url https://api.scryfall.com/cards/"set"/"card_number". With the "set" replaced with the extracted lowercase set abbrevation and the "card_number" replaced with the extracted card number. Do not return else besides the url. ONLY RETURN the url'}
]

# Use OpenAI's Chat API to get a response
chat_completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages
)

print(chat_completion)

# Extract the response from the model
card_api_url = chat_completion['choices'][0]['message']['content']

print(card_api_url)
# API Integration
response = requests.get(card_api_url)

if response.status_code == 200:
    card_data = response.json()
    prettified_card_data = json.dumps(card_data, indent=4)
    print(prettified_card_data)
    #print(card_data)
    # Extract and display relevant card data (e.g., card_data['name'], card_data['type_line'])
else:
    print("Card not found or API request failed.")
