using UnityEngine;
using UnityEngine.SceneManagement; // Required for SceneManager

public class SceneTransition : MonoBehaviour
{
    public string sceneName1; // Scene to load when the player presses the key
    public string sceneName2; // Another scene you might want to load

    private bool playerInZone = false; // Check if player is in the trigger zone

    void OnTriggerEnter(Collider other)
    {
        // Check if the player enters the trigger zone
        if (other.CompareTag("Player")) // Ensure the player object has the "Player" tag
        {
            playerInZone = true;
        }
    }

    void OnTriggerExit(Collider other)
    {
        // Check if the player exits the trigger zone
        if (other.CompareTag("Player"))
        {
            playerInZone = false;
        }
    }

    void Update()
    {
        // If the player is in the zone and presses the key (e.g., "E")
        if (playerInZone && Input.GetKeyDown(KeyCode.E)) // Change KeyCode as desired
        {
            LoadScene(sceneName1); // Load the selected scene when the player presses 'E'
        }
    }

    // Method to load the scene by its name
    public void LoadScene(string sceneName)
    {
        SceneManager.LoadScene(sceneName); // Load the scene by name
    }
}
