import torch
import torchvision.transforms as transforms
from torchvision.models import resnet18, ResNet18_Weights
from PIL import Image



# Load ResNet18 with pretrained weights
model = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
model.eval()


# Transformation for the image
transform = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor()])


def analyze_image(image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        input_tensor = transform(image).unsqueeze(0)

        # Placeholder logic for manipulation detection
        with torch.no_grad():
            output = model(input_tensor)
            confidence = torch.softmax(output[0], dim=0)[0].item()
            result = "Manipulated" if confidence > 0.5 else "Original"

        return {"result": result, "confidence": confidence}
    except Exception as e:
        return {"error": str(e)}