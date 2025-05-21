// You can write your code in this editor

// Collision Event: Bunny with Lava
if (!milk_collision)  // Check if the bunny hasn't collided yet this frame
{
    // Deduct health if the bunny is still alive
    if (health > 0)
    {
        health -= 1;  // Deduct 1 health
    }

    // Reset bunny's position to the starting point
    x = 197;
    y = 479;  // Use your desired restart position

    // Set the flag to true to prevent further health deduction this frame
    milk_collision = true;
}