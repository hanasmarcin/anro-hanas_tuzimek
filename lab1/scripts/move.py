#!/usr/bin/env python

# import potrebnych pakietow
import click
import rospy
from geometry_msgs.msg import Twist 

# funkcja odpowiadajaca za sterowanie
def move():
    # Stworzenie nowego publishera
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    # Zainicjowanie wezla
    rospy.init_node('move')
    # Pobranie z serwera parametrow odpowiednich liter klawiszy
    UP = rospy.get_param("up")
    LEFT = rospy.get_param("left")
    DOWN = rospy.get_param("down")
    RIGHT = rospy.get_param("right")

    # Petla wykonywana, dopoki program dziala
    while not rospy.is_shutdown():
	# Stworzenie obiektu typu Twist - wiadomosci wysylanej przez wezel
	# zawierajacej wspolrzedne przesuniecia i obrotu
	twist = Twist()
	# Uzyskanie informacji o wcisnietym przycisku
	key_pressed = click.getchar()

	# Sprawdzenie, ktory przycisk zostal wcisniety i ustawianie
	# parametrow ruchu
	if key_pressed == UP:
	    twist.linear.x = 2
	elif key_pressed == LEFT:
	    twist.angular.z = 1.04719755119
	elif key_pressed == DOWN:
	    twist.linear.x = - 2
	elif key_pressed == RIGHT:
	    twist.angular.z = -1.04719755119

	# Publikowanie wiadomosci o przemieszceniu na topic
	pub.publish(twist)


if __name__ == '__main__':
    try:
        move()
    except rospy.ROSInterruptException:
        pass
