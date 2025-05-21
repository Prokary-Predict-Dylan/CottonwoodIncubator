// You can write your code in this editor

var _targetX = endX, _targetY = endY;
if(goingToStart)
{
	_targetX = startX;
	_targetY = startY;
}

//setting movement
move_x = sign(_targetX - x) * currentSpeed;
move_y = sign(_targetY - y) * currentSpeed;