import re
from PIL import Image
import pytesseract

def image_word():
    # Path to your Tesseract executable (you should have Tesseract installed)
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

    # Open the image using PIL (Pillow)
    image = Image.open('./uploads/blueprint1.jpg')

    # Perform OCR to extract text from the image
    text = pytesseract.image_to_string(image)

    # Define a regular expression pattern to extract numeric parts of keywords (e.g., "3 BHK" or "4 BHK")
    numeric_pattern = r'(\d+)\s*BHK'

    # Use a regular expression to find and extract numeric parts of keywords
    numeric_parts = re.findall(numeric_pattern, text, re.IGNORECASE)

    # Print the numeric parts detected in the text
    print(f"Numeric parts detected: {', '.join(numeric_parts)}")

    # Regular expression pattern to match area values in the "40'-0"X 40'-0"" format
    area_pattern = r'(\d+\'-\d{1,2}"\s*X\s*\d+\'-\d{1,2}")'

    # Find and extract area values from the text
    areas = re.findall(area_pattern, text, re.IGNORECASE)

    # Function to convert area values to square feet
    def convert_area_to_square_feet(area_value):
        # Extract the width and height using regex
        match = re.match(r'(\d+)\'-(\d{1,2})"\s*X\s*(\d+)\'-(\d{1,2})"', area_value)
        if match:
            width_feet = int(match.group(1))
            width_inches = int(match.group(2))
            height_feet = int(match.group(3))
            height_inches = int(match.group(4))
            total_area = (width_feet ) * (height_feet )
            return total_area
        else:
            return 0

    # Process each area value in the list and convert to square feet
    converted_areas = [convert_area_to_square_feet(area_value) for area_value in areas]

    return numeric_parts, converted_areas

if __name__ == "__main__":
    numeric_parts, converted_areas = image_word()
    print("Numeric Parts:", numeric_parts)
    print("Converted Areas:", converted_areas)
