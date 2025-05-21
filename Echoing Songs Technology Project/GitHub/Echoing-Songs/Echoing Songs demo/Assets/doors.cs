using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class doors_camera : MonoBehaviour
{
    public Camera camera1; // Drag the first camera here in the inspector
    public Camera camera2; // Drag the second camera here in the inspector


    void Update()
    {
        // Check for key press to switch cameras
        if (Input.GetKeyDown(KeyCode.Alpha1)) // Switch to camera 1 when pressing '1'
        {
            SwitchCamera(camera1);
        }
        else if (Input.GetKeyDown(KeyCode.Alpha2)) // Switch to camera 2 when pressing '2'
        {
            SwitchCamera(camera2);
        }
    }

    void SwitchCamera(Camera newCamera)
    {
        // Disable all cameras
        Camera[] cameras = FindObjectsOfType<Camera>();
        foreach (Camera cam in cameras)
        {
            cam.gameObject.SetActive(false);
        }

        // Enable the selected camera
        newCamera.gameObject.SetActive(true);
    }
}
