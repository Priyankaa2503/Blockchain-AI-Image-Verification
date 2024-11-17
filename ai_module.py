import torch
import torchvision.transforms as transforms
from PIL import Image
from timm import create_model  
model = create_model(
    "xception", pretrained=True, num_classes=2
)  
model.eval()

transform = transforms.Compose(
    [
        transforms.Resize((299, 299)), 
        transforms.ToTensor(),
        transforms.Normalize(
            [0.5, 0.5, 0.5], [0.5, 0.5, 0.5]
        ), 
    ]
)


def analyze_image(image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        input_tensor = transform(image).unsqueeze(0)  

        # Perform inference
        with torch.no_grad():
            output = model(input_tensor)
            probabilities = torch.softmax(output[0], dim=0)
            manipulated_prob = probabilities[
                1
            ].item()  

        result = "Manipulated" if manipulated_prob > 0.5 else "Original"
        return {"result": result, "confidence": manipulated_prob}

    except Exception as e:
        return {"error": str(e)}
