import cv2
import torch
import matplotlib.pyplot as plt
import keyboard

# Download the MiDas
midas = torch.hub.load("intel-isl/MiDaS", 'MiDaS_small')
midas.to("cpu")
midas.eval()

transforms = torch.hub.load("intel-isl/MiDaS", 'transforms')
transform = transforms.small_transform

cap = cv2.VideoCapture(0)
plt.ion()  # Turn on interactive mode for Matplotlib

while cap.isOpened():
    ret, frame = cap.read()

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    imgbatch = transform(img).to("cpu")

    with torch.no_grad():
        prediction = midas(imgbatch)
        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=img.shape[:2],
            mode="bicubic",
            align_corners=False
        ).squeeze()

        output = prediction.cpu().numpy()
        print(output)

    plt.clf()  # Clear previous plots
    plt.subplot(121)
    plt.imshow(img)  # Display the original video frame
    plt.title('Original Frame')

    plt.subplot(122)
    plt.imshow(output, cmap='jet')  # Display the depth map
    plt.title('Depth Map')

    plt.pause(0.00001)

    if keyboard.is_pressed('q'):
        cap.release()
        cv2.destroyAllWindows()
        break

plt.ioff()  # Turn off interactive mode before exiting
plt.show()
