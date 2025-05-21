using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class basic_move : MonoBehaviour
{
    public float speed = 1f;  // Speed of the enemy's movement
    public Transform pointA;  // The starting point
    public Transform pointB;  // The destination point

    private bool movingToB = true;  // To track if the enemy is moving towards pointB

    void Start()
    {
        // Ensure that the points have been assigned in the Inspector
        if (pointA == null || pointB == null)
        {
            Debug.LogError("PointA or PointB has not been assigned in the Inspector!");
        }
    }

    void Update()
    {
        // Only move if both points are assigned
        if (pointA != null && pointB != null)
        {
            MoveEnemy();
        }
    }

    void MoveEnemy()
    {
        // Move towards pointB if movingToB is true, otherwise towards pointA
        if (movingToB)
        {
            transform.position = Vector3.MoveTowards(transform.position, pointB.position, speed * Time.deltaTime);

            if (transform.position == pointB.position)
                movingToB = false;  // Switch direction when reaching pointB
        }
        else
        {
            transform.position = Vector3.MoveTowards(transform.position, pointA.position, speed * Time.deltaTime);

            if (transform.position == pointA.position)
                movingToB = true;  // Switch direction when reaching pointA
        }
    }
}
