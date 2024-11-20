# Image Processing Assignment 01
# Name: Saurabh Kumar, Roll: 2022BCS-062
# Submitted to: Dr. KV Arya

from PIL import Image
import os

# Define Robinson 8-direction masks
DIRECTION_MASKS = [
    [[1, 0, -1], [2, 0, -2], [1, 0, -1]],  # North
    [[2, 1, 0], [1, 0, -1], [0, -1, -2]],  # Northwest
    [[1, 2, 1], [0, 0, 0], [-1, -2, -1]],  # West
    [[0, 1, 2], [-1, 0, 1], [-2, -1, 0]],  # Southwest
    [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]],  # South
    [[-2, -1, 0], [-1, 0, 1], [0, 1, 2]],  # Southeast
    [[-1, -2, -1], [0, 0, 0], [1, 2, 1]],  # East
    [[0, -1, -2], [1, 0, -1], [2, 1, 0]]   # Northeast
]
DIRECTION_NAMES = [
    "North", "Northwest", "West", "Southwest",
    "South", "Southeast", "East", "Northeast"
]

# Create the output directory if it doesn't exist
os.makedirs("outputs", exist_ok=True)

# Function to list image files in the 'images/' directory
def get_image_paths(directory="images"):
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(".jpeg")]

# Function to apply a kernel to an image
def apply_kernel(image, kernel, x, y):
    kernel_size = len(kernel)
    offset = kernel_size // 2
    result = 0

    for i in range(kernel_size):
        for j in range(kernel_size):
            px, py = x + i - offset, y + j - offset
            if 0 <= px < image.width and 0 <= py < image.height:
                result += image.getpixel((px, py)) * kernel[i][j]

    return result

# Function to process an image with Robinson masks
def process_image(image_path):
    # Convert to grayscale
    image = Image.open(image_path).convert("L")  
    combined_gradient = Image.new("L", image.size, 0)  

    base_name = os.path.splitext(os.path.basename(image_path))[0]

    for idx, (mask, name) in enumerate(zip(DIRECTION_MASKS, DIRECTION_NAMES)):
        directional_gradient = Image.new("L", image.size, 0)

        for x in range(image.width):
            for y in range(image.height):
                gradient_value = abs(apply_kernel(image, mask, x, y))
                gradient_value = min(255, gradient_value)  # Clamp to 255
                directional_gradient.putpixel((x, y), gradient_value)

        # Save directional gradient
        output_path = f"outputs/{base_name}_{name}.jpeg"
        directional_gradient.save(output_path, format="JPEG")
        print(f"Saved: {output_path}")

        # Combine gradients
        for x in range(image.width):
            for y in range(image.height):
                combined_value = max(
                    combined_gradient.getpixel((x, y)),
                    directional_gradient.getpixel((x, y))
                )
                combined_gradient.putpixel((x, y), combined_value)

    # Save combined gradient
    combined_output_path = f"outputs/{base_name}_combined.jpeg"
    combined_gradient.save(combined_output_path, format="JPEG")
    print(f"Saved combined gradient: {combined_output_path}")

# Main function to process all images in the 'images/' directory
def main():
    image_paths = get_image_paths()
    if not image_paths:
        print("No images found in the 'images/' directory. Please add some images to process.")
        return

    for image_path in image_paths:
        print(f"Processing: {image_path}")
        process_image(image_path)

if __name__ == "__main__":
    main()



#input image cane both RGB or Gray  image but in this assignment i user grayscale image which is located in ./images folder as an imput image.