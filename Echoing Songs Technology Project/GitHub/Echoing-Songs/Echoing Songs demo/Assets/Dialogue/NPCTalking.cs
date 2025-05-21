using UnityEngine;
using UnityEngine.UI; // For using UI components like Text
using System.Collections; // Required for IEnumerator and coroutines

public class NPCDialogue : MonoBehaviour
{
    public string[] dialogueLines; // Array of dialogue lines for the NPC
    public Text dialogueText; // UI Text to display the dialogue
    public float typingSpeed = 0.05f; // Typing speed for text to appear

    private bool playerInRange = false; // To track if the player is in range
    private int currentLine = 0; // Keeps track of which line we're on in the dialogue

    void Start()
    {
        dialogueText.gameObject.SetActive(false); // Make sure dialogue is hidden initially
    }

    void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Player")) // If the player enters the trigger zone
        {
            playerInRange = true;
            ShowDialogue("Press E to talk to the NPC"); // Display a prompt
        }
    }

    void OnTriggerExit(Collider other)
    {
        if (other.CompareTag("Player")) // If the player exits the trigger zone
        {
            playerInRange = false;
            dialogueText.gameObject.SetActive(false); // Hide dialogue when player leaves the zone
        }
    }

    void Update()
    {
        if (playerInRange && Input.GetKeyDown(KeyCode.E)) // If the player presses E while in range
        {
            if (!dialogueText.gameObject.activeSelf)
            {
                StartCoroutine(DisplayDialogue()); // Start showing the dialogue
            }
            else
            {
                // If dialogue is already active, go to the next line
                currentLine++;
                if (currentLine >= dialogueLines.Length)
                {
                    dialogueText.gameObject.SetActive(false); // Hide the dialogue once all lines are shown
                    currentLine = 0; // Reset dialogue to start
                }
                else
                {
                    StopAllCoroutines(); // Stop any current typing coroutine
                    StartCoroutine(DisplayDialogue()); // Show the next line
                }
            }
        }
    }

    IEnumerator DisplayDialogue()
    {
        dialogueText.gameObject.SetActive(true); // Make sure the dialogue box is visible
        dialogueText.text = ""; // Clear previous text

        // Type out each character of the current dialogue line
        foreach (char letter in dialogueLines[currentLine])
        {
            dialogueText.text += letter;
            yield return new WaitForSeconds(typingSpeed); // Wait for the typing speed delay
        }
    }

    void ShowDialogue(string text)
    {
        dialogueText.gameObject.SetActive(true);
        dialogueText.text = text;
    }
}
