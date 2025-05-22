// Get input for movement
rightKey = keyboard_check(vk_right);
leftKey = keyboard_check(vk_left);
upKey = keyboard_check(vk_up);
downKey = keyboard_check(vk_down);

// Horizontal movement (left/right)
move_x = (rightKey - leftKey) * moveSpd;

function teleport_to_start() {
	if (room != OpeningScreen) {
		x = global.start_x
		y = global.start_y
	}
}


//Off Screen wall that will prevent the player from going off screen and being unreachable again
if (place_meeting(x + move_x, y, oOffScreen))
{
	  move_x = 0;
}

// Jumping / gravity 

// Checking if touching ground (or platform)
if (place_meeting(x, y + 2, oPlank))   
{
    // Stop vertical movement (y)
    move_y = 0;                       
    // Jump when space is pressed
    if (keyboard_check(vk_space))     
    {
        // Set upward speed for jump
        move_y = -jumpSpd;            
    }
}
// Apply gravity if not on the ground
else if (move_y < 10)                  
{
    // Increase downward speed (falling)
    move_y += 1;                      
}

// Collisions
// Horizontal collision with oPlank
if (place_meeting(x + move_x, y, oPlank)) // Check horizontal collisions with platform
{
    move_x = 0;  // Stop horizontal movement if colliding with platform
}

// Vertical collision with oPlank
if (place_meeting(x, y + move_y, oPlank)) // Check vertical collisions with platform
{
    move_y = 0;  // Stop vertical movement if colliding with platform
	if (keyboard_check_pressed(vk_space))
{
	move_y -= 10;	
}
}

// Collision with oDoor
// Stop horizontal movement if colliding with oDoor horizontally
if (place_meeting(x + move_x, y, oDoor))
{
    move_x = 0;  // Stop horizontal movement if colliding with door
}

// Stop vertical movement if colliding with oDoor vertically
if (place_meeting(x, y + move_y, oDoor))
{
    move_y = 0;  // Stop vertical movement if colliding with door
	if (keyboard_check_pressed(vk_space))
{
	move_y -= 10;	
}
}

if (place_meeting(x, y + move_y, oLava))
{
	x = restart_x;
	y = restart_y;
	show_message("Jump to continue");
}

/*if (place_meeting(x + move_x, y, oNextLevel))
{
    move_x = 0;  // Stop horizontal movement if colliding with door
}

// Stop vertical movement if colliding with oDoor vertically
if (place_meeting(x, y + move_y, oNextLevel))
{
    move_y = 0;  // Stop vertical movement if colliding with door
	
}*/

// Handle moving the player (if no collision, update position)
x += move_x;
y += move_y;




/*// Jumping logic
if (keyboard_check_pressed(vk_space) && !inAir && !isRespawning) {
    move_y = jump_Spd;  // Start jumping by applying upward speed
    inAir = true;        // Bunny is now in the air
}

// If the bunny is not respawning, handle movement and gravity
if (!isRespawning) {
    // Apply gravity if bunny is in the air
    if (inAir) {
        move_y += gravity;
        if (move_y > max_Fall_Speed) {
            move_y = max_Fall_Speed;  // Limit falling speed
        }
    }

    // Check if the bunny collides with a plank or platform
    if (place_meeting(x, y + move_y, oPlank)) {
        // Prevent bunny from falling through the plank
        //while (!place_meeting(x, y + 1, oPlank)) {
        //    y -= 1;  // Move up to align with the plank
        //}
        inAir = false;  // Bunny has landed, so it’s not in the air anymore
        move_y = 0;     // Stop vertical movement when on a plank
    }

    // If the bunny has fallen past the limit, reset position
    if (y > fall_limit) {
        isRespawning = true;  // Trigger the respawn state
        respawnTimer = respawnDelay; // Reset the respawn timer
        move_y = 0; // Stop vertical movement
        inAir = true; // Stop any ongoing jump
        sprite_index = Player_Bunny;  // Use default bunny sprite (no respawn animation)
    }

    // Check for door collision and prevent phasing
    if (place_meeting(x, y - 1, oDoor)) {
        // Stop vertical movement immediately when colliding with the door
        move_y = 0;  // Ensure vertical movement is stopped
        
        // Align the bunny to the top of the door to prevent overlap
        //while (place_meeting(x, y - 1, oDoor)) {
            //move_y -= 100;  // Adjust position upwards to align with the door
        //}

        inAir = false;  // Bunny is no longer in the air (it’s on the door)

        // Allow horizontal movement after colliding with the door
        if (keyboard_check(vk_right)) {
            move_x = move_Spd;
        } else if (keyboard_check(vk_left)) {
            move_x = -move_Spd;
        } else {
            move_x = 0;
        }

    }
} else {
    // Handle respawn delay (countdown timer)
    respawnTimer -= 1; // Decrease the respawn timer

    // If timer reaches 0, respawn bunny
    if (respawnTimer <= 0) {
        x = restart_x;  // Reset X position
        y = restart_y;  // Reset Y position
        move_y = 0;     // Reset vertical speed
        inAir = true;  // Reset air state
        isRespawning = false;  // End the respawn state
        sprite_index = Player_Bunny;  // Use the default bunny sprite again
		respawnTimer = 10;
    }
}

// Horizontal movement logic (only if not respawning)
if (!isRespawning) {
    // Check if horizontal movement isn't blocked by the door collision
    if (keyboard_check(vk_right)) {
        move_x = move_Spd;
    } else if (keyboard_check(vk_left)) {
        move_x = -move_Spd;
    } else {
        move_x = 0;
    }

}

if (place_meeting(x, y - 1, oDoor)) {
        // Stop vertical movement immediately when colliding with the door
        move_y += 1;
}

// Move bunny horizontally
x += move_x;
// Apply vertical movement
y += move_y;*/
