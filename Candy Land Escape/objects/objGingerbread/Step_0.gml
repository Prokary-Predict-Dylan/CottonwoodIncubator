// Get input for movement
rightKey = keyboard_check(vk_right);
leftKey = keyboard_check(vk_left);
upKey = keyboard_check(vk_up);
downKey = keyboard_check(vk_down);

var jump = keyboard_check(vk_space)

// Horizontal movement (left/right)
move_x = (rightKey - leftKey) * moveSpd;

function teleport_to_start() {
    if (room != OpeningScreen) {
        x = global.start_x
        y = global.start_y
    }
}

// Jumping / gravity 
if (place_meeting(x, y + 2, oCookieCrumb))   
{
    move_y = 0;                       

    if (jump)     
    {
        move_y = -jumpSpd; // Set upward speed for jump
        multiJump = true;  // Allow multi-jumping when jumping
    }
}
else if (multiJump && jump) // Check if multiJump is enabled and jump is pressed
{
    if (move_y > -jumpSpd) // Prevent making the jump too high
    {
        move_y -= doubleJumpSpd; // Make the bunny move up with each jump
    }
}
else if (move_y < 10)                  
{
    move_y += 1;  // Apply gravity
}

// Reset multiJump when touching the ground (to prevent infinite jumps)
if (place_meeting(x, y + 2, oCookieCrumb))
{
    multiJump = false;
}
if (place_meeting(x, y + 2, oCandyCaneRock))   
{
    move_y = 0;                       

    if (jump)     
    {
        move_y = -jumpSpd; // Set upward speed for jump
        multiJump = true;  // Allow multi-jumping when jumping
    }
}
else if (multiJump && jump) // Check if multiJump is enabled and jump is pressed
{
    if (move_y > -jumpSpd) // Prevent making the jump too high
    {
        move_y -= doubleJumpSpd; // Make the bunny move up with each jump
    }
}
else if (move_y < 10)                  
{
    move_y += 1;  // Apply gravity
}

// Reset multiJump when touching the ground (to prevent infinite jumps)
if (place_meeting(x, y + 2, oCandyCaneRock))
{
    multiJump = false;
}


if (place_meeting(x, y + 2, oMountainCliff))   
{
    move_y = 0;                       

    if (jump)     
    {
        move_y = -jumpSpd; // Set upward speed for jump
        multiJump = true;  // Allow multi-jumping when jumping
    }
}
else if (multiJump && jump) // Check if multiJump is enabled and jump is pressed
{
    if (move_y > -jumpSpd) // Prevent making the jump too high
    {
        move_y -= doubleJumpSpd; // Make the bunny move up with each jump
    }
}
else if (move_y < 10)                  
{
    move_y += 1;  // Apply gravity
}

// Reset multiJump when touching the ground (to prevent infinite jumps)
if (place_meeting(x, y + 2, oMountainCliff))
{
    multiJump = false;
}


if (place_meeting(x, y + 2, oSnowyCliff))   
{
    move_y = 0;                       

    if (jump)     
    {
        move_y = -jumpSpd; // Set upward speed for jump
        multiJump = true;  // Allow multi-jumping when jumping
    }
}
else if (multiJump && jump) // Check if multiJump is enabled and jump is pressed
{
    if (move_y > -jumpSpd) // Prevent making the jump too high
    {
        move_y -= doubleJumpSpd; // Make the bunny move up with each jump
    }
}
else if (move_y < 10)                  
{
    move_y += 1;  // Apply gravity
}

// Reset multiJump when touching the ground (to prevent infinite jumps)
if (place_meeting(x, y + 2, oSnowyCliff))
{
    multiJump = false;
}

if (jump && place_meeting(x, y + 1, oMountainCliffPlatform))
{
	move_y = -jumpSpd;	
}


// Moving platform collision
var _movingPlatform = instance_place(x, y + max(1, move_y), oMountainCliffPlatform);
if (_movingPlatform && bbox_bottom <= _movingPlatform.bbox_top)
{
    if (move_y > 0)
    {
        while (!place_meeting(x, y + sign(move_y), oMountainCliffPlatform))
        {
            y += sign(move_y);			
			
        }
        move_y = 0;
    }

    x += _movingPlatform.move_x;
    y += _movingPlatform.move_y;
}

// Platform collision
if (place_meeting(x + move_x, y, oCookieCrumb)) 
{
    move_x = 0;
}

if (place_meeting(x, y + move_y, oCookieCrumb)) 
{
    move_y = 0;
    if (keyboard_check_pressed(vk_space))
    {
        move_y -= 10;  
    }
}
if (place_meeting(x + move_x, y, oCandyCaneRock)) 
{
    move_x = 0;
}

if (place_meeting(x, y + move_y, oCandyCaneRock)) 
{
    move_y = 0;
    if (keyboard_check_pressed(vk_space))
    {
        move_y -= 10;  
    }
}
if (place_meeting(x + move_x, y, oMountainCliff)) 
{
    move_x = 0;
}

if (place_meeting(x, y + move_y, oMountainCliff)) 
{
    move_y = 0;
    if (keyboard_check_pressed(vk_space))
    {
        move_y -= 10;  
    }
}
if (place_meeting(x + move_x, y, oSnowyCliff)) 
{
    move_x = 0;
}

if (place_meeting(x, y + move_y, oSnowyCliff)) 
{
    move_y = 0;
    if (keyboard_check_pressed(vk_space))
    {
        move_y -= 10;  
    }
}

if (place_meeting(x + move_x, y, oDoor))
{
    move_x = 0;
}

if (place_meeting(x, y + move_y, oDoor))
{
    move_y = 0;  
    if (keyboard_check_pressed(vk_space))
    {
        move_y -= 10;  
    }
}
if (place_meeting(x + move_x, y, oWalk))
{
    move_x = 0;
}

if (place_meeting(x, y + move_y, oWalk))
{
    move_y = 0;  
    if (keyboard_check_pressed(vk_space))
    {
        move_y -= 10;  
    }
}
if (place_meeting(x + move_x, y, oSnow))
{
    move_x = 0;
}

if (place_meeting(x, y + move_y, oSnow))
{
    move_y = 0;  
    if (keyboard_check_pressed(vk_space))
    {
        move_y -= 15;  
    }
}

/*if (place_meeting(x + move_x, y, oRedRiver))
{
    move_x = 0;
}

if (place_meeting(x, y + move_y, oRedRiver))
{
    move_y = 0;  
    if (keyboard_check_pressed(vk_space))
    {
        move_y -= 10;  
    }
}*/

// Lava Collision Detection - Only deduct health once per collision
if (place_meeting(x, y + 2, oMilkBlock))  // Check collision with lava, using a small offset to avoid getting stuck inside
{
    if (!milk_collision)  // Ensure health is only deducted once per frame
    {
        // Reduce health by 1
        if (health > 0)
        {
            health -= 1;
        }

        // Reset position to starting coordinates
        x = restart_x;
        y = restart_y;

        milk_collision = true;  // Set the flag to prevent multiple deductions in the same frame
    }
}

if (place_meeting(x, y + 2, oRedRiver))  // Check collision with lava, using a small offset to avoid getting stuck inside
{
    if (!milk_collision)  // Ensure health is only deducted once per frame
    {
        // Reduce health by 1
        if (health > 0)
        {
            health -= 1;
        }

        // Reset position to starting coordinates
        x = restart_x;
        y = restart_y;
		room_goto(Level2);

        milk_collision = true;  // Set the flag to prevent multiple deductions in the same frame
    }
}

// Reset the lava collision flag when bunny is no longer touching lava
if (!place_meeting(x, y + 2, oRedRiver))  // If no longer touching lava
{
    milk_collision = false;  // Reset the flag for the next lava collision
}

// Health check and reset
if (health <= 0) {
    health = 3; // Reset health to initial value
    coins = 0;
	visible = false;
    room_goto(YouDied); // Transition to "You Died" room
}

// Handle moving the player
x += move_x;
y += move_y;





/*// Jumping / gravity 

// Checking if touching ground (or platform)
if (place_meeting(x, y + 2, oPlank))   
{
    // Stop vertical movement (y)
    move_y = 0;                       
    // Jump when space is pressed
    if (jump)     
    {
        // Set upward speed for jump
        move_y = -jumpSpd;
		
		if(multiJump or place_meeting(x, y + 1, oPlank))
		{
			move_y = -jumpSpd;
		}
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

if (health <= 0) {
    // Reset the health back to a starting value (optional)
    health = 3; // Set to initial health value if needed
	coins = 0;
    // Restart the game by going to Room 1 (level 1)
    room_goto(YouDied); // Replace 'Room1' with the name of your first room
	//x = restart_x;
	//y = restart_y;
}


// Handle moving the player (if no collision, update position)
x += move_x;
y += move_y;
*/




/*if (place_meeting(x + move_x, y, oNextLevel))
{
    move_x = 0;  // Stop horizontal movement if colliding with door
}

// Stop vertical movement if colliding with oDoor vertically
if (place_meeting(x, y + move_y, oNextLevel))
{
    move_y = 0;  // Stop vertical movement if colliding with door
	
}*/

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
