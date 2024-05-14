from PIL import Image, ImageDraw

# Define image size
image_width = 100
image_height = 400

# Create a new image with white background
image = Image.new("RGB", (image_width, image_height), "white")
draw = ImageDraw.Draw(image)

# Define pipe parameters
pipe_width = 50
pipe_height = 300
pipe_color = "green"

# Draw the pipe
pipe_x = (image_width - pipe_width) // 2
pipe_y = (image_height - pipe_height) // 2
draw.rectangle([pipe_x, pipe_y, pipe_x + pipe_width, pipe_y + pipe_height], fill=pipe_color)

# Save the image
image.save("pipe_image.png")

# Display the image
image.show()
