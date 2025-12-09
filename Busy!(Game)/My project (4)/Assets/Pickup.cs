using UnityEngine;

public class Pickup : MonoBehaviour
{
    private bool isHolding = false;

    [SerializeField]
    private float throwForce = 600f;

    [SerializeField]
    private float maxDistance = 3f;

    private float distance;

    private TempParent tempParent;
    private Rigidbody rb; // Fixed: was "RigidBody", should be "Rigidbody"
    private Vector3 objectPos;

    void Start()
    {
        rb = GetComponent<Rigidbody>(); // Fixed typo: "GetCompenent" -> "GetComponent"
       // tempParent = TempParent //Instance
        ;

        if (rb == null)
        {
            Debug.LogError("Rigidbody not found on object!");
        }

        if (tempParent == null)
        {
            Debug.LogError("TempParent instance not found in scene!");
        }
    }

    void Update()
    {
        if (isHolding)
        {
            Hold();
        }
    }

    private void OnMouseDown()
    {
        // Pickup
        if (tempParent != null)
        {
            isHolding = true;
            rb.useGravity = false;
            rb.detectCollisions = true;

            this.transform.SetParent(tempParent.transform);
        }
        else
        {
            Debug.Log("TempParent item not found in scene!");
        }
    }

    private void OnMouseUp()
    {
        // Drop
        isHolding = false;
        rb.useGravity = true;
        this.transform.SetParent(null);
    }

    private void Hold()
    {
        rb.linearVelocity = Vector3.zero; // Fixed: "LinearVelocity" doesn't exist, use "velocity"
        rb.angularVelocity = Vector3.zero; // Fixed: "AngularVelocity" -> "angularVelocity"

        // Keep object at holding position
        this.transform.position = tempParent.transform.position;

        // Throw logic (right mouse click)
        if (Input.GetMouseButtonDown(1))
        {
            isHolding = false;
            this.transform.SetParent(null);
            rb.useGravity = true;
            rb.AddForce(tempParent.transform.forward * throwForce);
        }
    }
}
