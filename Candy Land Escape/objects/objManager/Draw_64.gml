var l4CC419CD_0 = false;
l4CC419CD_0 = instance_exists(objGingerbread);
if(l4CC419CD_0)
{
	// Draw the HUD coin sprite
	draw_sprite(spr_good_treat_hud, 0, 1900, 100);

	// Change the font to ft_hud
	draw_set_font(Font_TimesNewRomanGreek);

	// Draw the player's coins value
	// Taken from the player
	// using obj_player.coins
	draw_text(1990, 100, string("X:") + string(objGingerbread.coins));
	draw_set_color(c_white)
}

