// Player movement and jumping
moveSpd = 8;      
jumpSpd = 40; 
doubleJumpSpd = 10;
move_x = 0;       
move_y = 0;
gravity = 0;
restart_x = 193;         // Starting X position
restart_y = 479;         // Starting Y position
coins = 0;
persistent = true;
health = 3;
max_health = 3;
multiJump = false;
milk_collision = false;// Flag to track if the bunny has already collided with lava
river_collision = false;
rock_collision = false;
depth = -10;

/*healthbar_width = 100;
healthbar_height = 14;
healthbar_x = (2300/2) - (healtbar_width/2);
healthbar_y = ystart - 100;

//room = Level1;


/// Initialize Movement Speed and Jumping Speed
move_Spd = 2;            // Horizontal movement speed
jump_Spd = -10;          // Jumping speed
gravity = 0.2;           // Slower gravity for a slower drop
max_Fall_Speed = 3;      // Maximum fall speed (optional)
fall_limit = 860;        // Y position where the bunny dies and resets
restart_x = 197;         // Starting X position
restart_y = 274;         // Starting Y position

// Initialize movement variables
move_x = 0;              // Start with no horizontal movement
move_y = 0;              // Start with no vertical movement

// Flag for surface collision
onSurface = false;          // Initially not on the door

// State and timer for respawn
inAir = true;           // Bunny's air state
isRespawning = true;    // If bunny is in respawn state
respawnDelay = 30;       // 30 frames of delay before respawn (adjust as needed)
respawnTimer = 10;        // Timer for respawn delay



// Set initial position
x = restart_x;
y = restart_y;

y_min = -infinity
*/