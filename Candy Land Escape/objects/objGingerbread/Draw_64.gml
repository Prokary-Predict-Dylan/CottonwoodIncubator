/// @description Insert description here
// You can write your code in this editor
//draw_sprite(HealthBarBorderBG, 0, healthbar_x, healthbar_y);
//draw_sprite_stretched(Healthbar, 0, healthbar_x, healthbar_y,  );

// Draw hearts in the top left corner

var heart_x = 10;  // X position of first heart
var heart_y = 10;  // Y position of first heart
var heart_scale = 1.5;  // Scale factor for the hearts (adjust this value to make the hearts bigger or smaller)

for (var i = 0; i < max_health; i++) 
{
    if (i < health) {
        // Draw full heart with scaling using draw_sprite_ext
        draw_sprite_ext(PickupHealth, 0, heart_x + i * 100, heart_y, heart_scale, heart_scale, 0, c_white, 1);
    } 
    else
    {
        // Draw empty heart with scaling using draw_sprite_ext
        draw_sprite_ext(PickupHealthEmpty, 0, heart_x + i * 100, heart_y, heart_scale, heart_scale, 0, c_white, 1);
    }
}




