var l4CC419CD_0 = false;
l4CC419CD_0 = instance_exists(objBunny);
if(l4CC419CD_0)
{
	// Draw the HUD coin sprite
	draw_sprite(spr_carrot_hud, 0, 1835, 10);

	// Change the font to ft_hud
	draw_set_font(Font_TimesNewRomanGreek);

	// Draw the player's coins value
	// Taken from the player
	// using obj_player.coins
	draw_text(1990, 100, string("X:") + string(objBunny.coins));
	
}