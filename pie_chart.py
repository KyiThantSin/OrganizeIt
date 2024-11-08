import turtle
import math

def draw_pie_chart(data):
    screen = turtle.Screen()
    screen.title("Task Status Pie Chart")
    screen.bgcolor("white")
    
    pie = turtle.Turtle()
    pie.speed(5)

    # calculation
    total_tasks = sum(data.values())
    angles = {category: (count / total_tasks) * 360 for category, count in data.items()}

    colors = ["#B1D690", "#FEEC37", "#FFA24C", "#FF77B7"]

    start_angle = 0

    for index, (category, angle) in enumerate(angles.items()):
        pie.fillcolor(colors[index % len(colors)])
        pie.begin_fill()

        pie.setheading(start_angle)  
        pie.forward(100)            
        pie.left(90)
        pie.circle(100, angle)       
        pie.left(90)
        pie.forward(100)           

        pie.end_fill()
        start_angle += angle       

    pie.penup()
    pie.sety(-130)
    for i, (category, count) in enumerate(data.items()):
        pie.color(colors[i % len(colors)])
        pie.write(f"{category}: {count}", align="center", font=("Arial", 12, "normal"))
        pie.sety(pie.ycor() - 20)

    pie.hideturtle()
    screen.mainloop()
