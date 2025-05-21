// You can write your code in this editor

//Move
x += move_x;
y += move_y;

//Checking if at starting position
if(goingToStart && point_distance(x, y, startX, startY) < currentSpeed)
{
	goingToStart = false;
	currentSpeed = 0; 
	alarm[0] = waitTime;
}
//Checking if at ending position
else if (!goingToStart && point_distance(x, y, endX, endY) < currentSpeed)
{
	goingToStart = true;
	currentSpeed = 0;
	alarm[0] = waitTime;
}