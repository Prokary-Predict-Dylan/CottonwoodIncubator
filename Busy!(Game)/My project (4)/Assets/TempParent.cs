using UnityEngine;

public class TempParent : MonoBehaviour
{

    public static TempParent instance { get; private set; }

    private void Awake()
    {
        if (instance == null)
        {
            instance = this;
        }
        else
        {
            Destroy(this);
        }
    }
}