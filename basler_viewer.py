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

    print("Press 'q' to quit.")
    while cam.IsGrabbing():
        res = cam.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        if res.GrabSucceeded():
            img = converter.Convert(res).GetArray()
            cv2.imshow("Basler Camera", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        res.Release()

    cam.StopGrabbing()
    cam.Close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

