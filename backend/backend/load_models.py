import timm
import torch
from fashion_clip.fashion_clip import FashionCLIP

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
torch.backends.cudnn.benchmark = True
torch.backends.cudnn.deterministic = True

fclip = FashionCLIP("fashion-clip")
swin = timm.create_model('swin_base_patch4_window7_224', pretrained=True, num_classes=0)
swin.eval().to(device)