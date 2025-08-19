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

    # Optional: set pixel format if needed (many color Baslers default to Bayer)
    # from pypylon import genicam
    # cam.PixelFormat.Value = "BGR8"  # or "BayerRG8" depending on your model

    cam.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    converter = pylon.ImageFormatConverter()
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    cv2.namedWindow("Basler Camera", cv2.WINDOW_NORMAL)
    print("Press 'q' to quit.")

    while cam.IsGrabbing():
        res = cam.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        if res.GrabSucceeded():
            img = converter.Convert(res).GetArray()

            # Rotate 180 degrees
            img = cv2.rotate(img, cv2.ROTATE_180)

            cv2.imshow("Basler Camera", img)

            key = cv2.waitKey(10) & 0xFF  # use a bit longer delay
            if key == ord('q'):
                break
        res.Release()

    cam.StopGrabbing()
    cam.Close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
