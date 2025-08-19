from pypylon import pylon
import cv2

def main():
    # List cameras (nice to verify)
    tlf = pylon.TlFactory.GetInstance()
    devices = tlf.EnumerateDevices()
    if not devices:
        raise RuntimeError("No Basler cameras found on the network/USB.")
    print("Using:", devices[0].GetFriendlyName())

    cam = pylon.InstantCamera(tlf.CreateFirstDevice())
    cam.Open()

    # Optional: set pixel format if needed
    # from pypylon import genicam
    # cam.PixelFormat.Value = "BGR8"

    cam.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    converter = pylon.ImageFormatConverter()
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    # Create resizable window and set initial size
    cv2.namedWindow("Basler Camera", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Basler Camera", 1500, 900)

    while cam.IsGrabbing():
        res = cam.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        if res.GrabSucceeded():
            img = converter.Convert(res).GetArray()

            # Rotate 180 degrees
            img = cv2.rotate(img, cv2.ROTATE_180)

            cv2.imshow("Basler Camera", img)

            # Exit if user clicks the X button on the window
            if cv2.getWindowProperty("Basler Camera", cv2.WND_PROP_VISIBLE) < 1:
                break

        res.Release()

    cam.StopGrabbing()
    cam.Close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
