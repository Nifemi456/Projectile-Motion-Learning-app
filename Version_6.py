from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from math import *
from numbers import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk )
import matplotlib
import tkinter.scrolledtext as st 


matplotlib.use('TkAgg')

matplotlib.use('Agg')  # don't show plot

window_width = 0
window_height = 0

angle_2dp = 0
height_2dp = 0
distance_2dp = 0
u_2dp = 0

g = 9.8

ani_g= 150

degreeSymbol = '\u00b0'

isValid = False
res = 40

# place holder animation inputs
u = 250
angle = 45

#temp values
temp_x = 0
temp_y = 0

# movement functions
def get_y(t):
    global temp_y
    y_position = -((u* np.sin(np.radians(angle)) * t) - (0.5 * (ani_g) * t ** 2))
    y_move = (y_position - temp_y)
    
    temp_y = y_position
    
    return y_move

def get_x(t):
    global temp_x
    x_position = u* np.cos(np.radians(angle)) * t
    x_move = x_position - temp_x
    
    temp_x = x_position
    
    return x_move

fig, ax = plt.subplots(figsize=(4.7,4.7))
ax.set(xlim=[0, 10], ylim=[0, 10], xlabel='Distance [m]', ylabel='Height [m]')

def print_error(message, info):
    if info == 0:
        x = ""
    elif info == 1:
        x = 'in first input'
    elif info == 2:
        x = "in second input"
    elif info == 3:
        x = 'in both inputs'
    messagebox.showerror(f'Error {x}' ,message)
    print(message)
    return(message)

def run_ani(u_2dp, angle_2dp, g): 
    global isValid
    height_2dp = (((u_2dp**2)*((np.sin(np.radians(angle_2dp)))**2))/(2*g))

    distance_2dp = (((u_2dp**2)*(np.sin(np.radians(2*angle_2dp))))/g)
 
    def get_timetaken(): 
        a = 2 * u_2dp* np.sin(np.radians(angle_2dp)) / g
        return a

    def set_speed():
        global res
        global u_2dp
                
        return (1000*get_timetaken()/res)


    def get_t():
        global res
        a = np.linspace(0, ceil(get_timetaken()), res)
        return a

    def get_height():
        x = u_2dp* np.sin(np.radians(angle_2dp)) * get_t() - 0.5 * g * get_t() ** 2
        return x

    def get_distance():
        x = u_2dp* np.cos(np.radians(angle_2dp)) * get_t()
        return x

    scat = ax.scatter(get_distance(), get_height())
    ax.set(xlim=[0, distance_2dp+(0.1*distance_2dp)], ylim=[0, height_2dp+(0.1*height_2dp)], xlabel='Distance [m]', ylabel='Height [m]')

    def update(frame):
        global time
            # for each frame, update the data stored on each artist.
        x = get_distance()[:frame]
        y = get_height()[:frame]
        # update the scatter plot:
        data = np.stack([x, y]).T
        scat.set_offsets(data)
            
        return (scat)
    
    isValid = False
        
    ani = animation.FuncAnimation(fig, update, frames=res+1, interval=set_speed())
    plt.pause(1)

def calculate(var1 , var2, val1, val2, g):
    global isValid
    if var1 == Options[0]:
        u = val1
        if var2 == Options[1]:
            angle = val2
            height = (((u**2)*((sin(radians(angle)))**2))/(2*g))
            distance = (((u**2)*(sin(radians(2*angle))))/g)
            return output(angle, height, distance, u)
        elif var2 == Options[2]:
            height = val2
            try :
                angle = degrees(asin(sqrt(((2*g)*val2)/(u**2))))
                distance = (((u**2)*(sin(radians(2*angle))))/g)
                return output(angle, height, distance, u)
            except ValueError:
                isValid = False
                return print_error("The height entered is not possible with the given initial velocity", 0)
        elif var2 == Options[3]:
            distance = val2
            try:
                angle = (degrees(asin((g*val2)/(u**2))))/2
                height = (((u**2)*((sin(radians(angle)))**2))/(2*g))
                return output(angle, height, distance, u)
            except ValueError:
                isValid = False
                return print_error("The distance entered is not possible with the given initial velocity", 0)
    elif var1 == Options[1]:
        angle = val1
        if var2 == Options[0]:
            u = val2
            height = (((u**2)*((sin(radians(angle)))**2))/(2*g))
            distance = (((u**2)*(sin(radians(2*angle))))/g)
            return output(angle, height, distance, u)
        elif var2 == Options[2]:
            height = val2
            u = sqrt(((2*g)*val2)/((sin(radians(angle)))**2))
            distance = (((u**2)*(sin(radians(2*angle))))/g)
            return output(angle, height, distance, u)
        elif var2 == Options[3]:
            distance = val2
            u = sqrt((g*val2)/((sin(radians(2*angle)))))
            height = (((u**2)*((sin(radians(angle)))**2))/(2*g))
            return output(angle, height, distance, u)
        
    elif var1 == Options[2]:
        height = val1
        if var2 == Options[0]:
            u = val2
            try:
                angle = degrees(asin(sqrt(((2*g)*height)/(u**2))))
                distance = (((u**2)*(sin(radians(2*angle))))/g)
                return output(angle, height, distance, u)
            except ValueError:
                isValid = False
                return print_error("The height entered is not possible with the given initial velocity", 0)
        elif var2 == Options[1]:
            angle = val2
            u = sqrt(((2*g)*height)/((sin(radians(angle)))**2))
            distance = (((u**2)*(sin(radians(2*angle))))/g)
            return output(angle, height, distance, u)
        elif var2 == Options[3]:
            distance = val2
            angle = (degrees(atan((4*height)/(val2))))
            u = sqrt(((2*g)*height)/((sin(radians(angle)))**2))
            return output(angle, height, distance, u)

    elif var1 == Options[3]:
        distance = val1
        if var2 == Options[0]:
            u = val2
            try:    
                angle = (degrees(asin((g*distance)/(u**2))))/2
                height = (((u**2)*((sin(radians(angle)))**2))/(2*g))
                return output(angle, height, distance, u)
            except ValueError:
                isValid = False
                return print_error("The distance entered is not possible with the given initial velocity", 0)
        elif var2 == Options[1]:
            angle = val2
            u = sqrt((g*distance)/((sin(radians(2*angle)))))
            height = (((u**2)*((sin(radians(angle)))**2))/(2*g))
            return output(angle, height, distance, u)
        elif var2 == Options[2]:
            height = val2
            angle = (degrees(atan((4*height)/(distance))))
            u = sqrt(((2*g)*height)/((sin(radians(angle)))**2))
            return output(angle, height, distance, u)

def validation(var1, var2, inp1, inp2, g):
    global isValid
    if (var1 in Options and var2 in Options):
        
        if (var1 == var2):
            return print_error('Please select different input types', 0)
        else:
            if inp1 and inp2:

                try:
                    val1 = float(inp1)
                    val2 = float(inp2)
                except ValueError:
                    return print_error('Please enter numerical values', 0)
                
                else:
                    if ((val1>0) and (val2>0)):
                        
                        if ((var1 == Options[1] and val1>90) or (var2 == Options[1] and val2>90)):
                            if ((var1 == Options[1] and val1>90) and (var2 == Options[1] and val2>90)):
                                return print_error('Please enter angles less than or equal to 90', 3)                        
                            elif ((var1 == Options[1] and val1>90)):
                                return print_error('Please enter angles less than or equal to 90', 1)                        
                            elif ((var2 == Options[1] and val2>90)):
                                return print_error('Please enter angles less than or equal to 90', 2)                        
                        else:
                            isValid = True               
                            return calculate(var1, var2, val1, val2, g)
                    
                    else:
                        if ((val1<=0) and (val2<=0)):
                            return print_error('Please enter positive numbers only', 3)            
                        elif ((val1<=0)):
                            return print_error('Please enter positive numbers only', 1)            
                        elif ((val2<=0)):
                            return print_error('Please enter positive numbers only', 2)            
            else:
                if inp1:
                    return print_error('Please enter values', 2)
                elif inp2:
                    return print_error('Please enter values', 1)
                else:
                    return print_error('Please enter values', 3)

    else:
        if (var1 not in Options and var2 not in Options):
            return print_error('Please select your input types', 3)
        elif (var1 not in Options):
            return print_error('Please select your input types', 1)
        elif (var2 not in Options):
            return print_error('Please select your input types', 2)

def output(angle, height, distance, u):
    global degreeSymbol
    global angle_2dp
    global height_2dp
    global distance_2dp
    global u_2dp
    
    angle_2dp = round(angle,2)
    height_2dp = round(height,2)
    distance_2dp = round(distance,2)
    u_2dp = round(u,2)
    t_2dp = round(2 * u_2dp* np.sin(np.radians(angle_2dp)) / g, 2)
    
    outputLabel1.config(text = f'Angle is {angle_2dp} {degreeSymbol}')
    outputLabel2.config(text = f'Max height is {height_2dp} m')
    outputLabel3.config(text = f'Range is {distance_2dp} m')
    outputLabel4.config(text = f'Initial velocity is {u_2dp} m/s')
    outputLabel5.config(text = f'Time of flight is {t_2dp} s')
    
    print(f'\nAngle = {angle_2dp} {degreeSymbol} \nMax height = {height_2dp} m \nRange = {distance_2dp} m \nInitial velocity = {u_2dp} m/s \nTime of Flight = {t_2dp} s')
    
    
    return [angle_2dp, height_2dp, distance_2dp, u_2dp]

def fire():
    global temp_x
    global temp_y
    global u
    global angle
    global ani_g
    
    temp_x = 0
    temp_y = 0 

    u = u_value.get()
    angle = alpha_value.get()
    
    
    canvas_ani.delete("all")
    create_target()
    Ball('red')
    # canvas_ani.create_oval(5, 280, 45, 320, fill='blue')

def action():
    global g
    global degreeSymbol
    global fig
    global angle_2dp
    global height_2dp
    global distance_2dp
    global u_2dp
    global isValid
    
    var1 = select1.get()
    var2 = select2.get()
    
    inp1 = input1.get() 
    inp2 = input2.get()
    
    x = input3.get()
    
    if x:
        try:
            new_g = float(x)
        except ValueError:
            return print_error('Please enter numerical values for g', 0)
        
        else:
            if new_g>0:
                g = new_g 
            else:
                return print_error('Please enter positive numbers for g only', 0)

    validation(var1, var2, inp1, inp2 ,g) 
    
    if isValid:
        run_ani(u_2dp, angle_2dp, g)

def clear():
    ax.clear()
    ax.set(xlim=[0, 10], ylim=[0, 10], xlabel='Distance [m]', ylabel='Height [m]')

def stop():
    global i
    i=0
    canvas_ani.delete("all")
    create_ball('blue')
    create_target()

def get_window_size(root):
    global window_width
    global window_height
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    
def create_ball(color):
    global window_height
    global window_width
    get_window_size(main_window)
    
    return (canvas_ani.create_oval(5,(window_height-175), 45, (window_height-135), fill = color))

def create_target():
    global window_width
    global window_height
    
    x = window_width-10
    y = window_height-135
    canvas_ani.create_polygon(x-5,(y/2)-20 ,x,(y/2)-20 ,x,(y/2)-10 ,x-5,(y/2)+20-10,fill="red")
    canvas_ani.create_polygon(x-5,(y/2)-10 ,x,(y/2)-10 ,x,(y/2),x-5,(y/2),fill="white")
    canvas_ani.create_polygon(x-5,y/2 ,x,y/2 ,x,(y/2)+20,x-5,(y/2)+20,fill="red")
    canvas_ani.create_polygon(x-5,(y/2)+20,x,(y/2)+20,x,(y/2)+30,x-5,(y/2)+30,fill="white")
    canvas_ani.create_polygon(x-5,(y/2)+30,x,(y/2)+30,x,(y/2)+40,x-5,(y/2)+40,fill="red")
        

main_window = Tk()

main_window.title("Projectile Motion")  
tabControl = ttk.Notebook(main_window) 
  
tab1 = Frame(tabControl) 
tab2 = Frame(tabControl) 
tab3 = Frame(tabControl) 
  
tabControl.add(tab1, text ='Animation') 
tabControl.add(tab2, text ='Calc') 
tabControl.add(tab3, text ='Theory') 
tabControl.pack(expand = 1, fill ="both") 

main_window.geometry("700x455") 

# Tab 1
#creating canvas
canvas_ani = Canvas(tab1, width = 700, height = 320, bg = "white")
canvas_ani.pack(side=TOP, expand=True, fill=BOTH)

#slider
alpha_value = IntVar(value = 45)
scale_Alpha = ttk.Scale(tab1, command = lambda value: alpha_value.get(),
                        from_ = 90,
                        to = 0,
                        length = 100,
                        orient = 'vertical',
                        variable = alpha_value)

scale_Alpha.pack(side=LEFT)

alpha_Label = Label(tab1, text = 'Angle: 0-90'+ degreeSymbol, )
alpha_Label.pack(side=LEFT)

u_value = IntVar(value = 100)
scale_u = ttk.Scale(tab1, command = lambda value: u_value.get(),
                        from_ = 500,
                        to = 50,
                        length = 100,
                        orient = 'vertical',
                        variable = u_value,
                        )

scale_u.pack(side=RIGHT)


u_Label = Label(tab1, text = 'Initial Velocity:\n 100-500' )
u_Label.pack(side=RIGHT)

#Creating Ball class

i = 0

class Ball():
    def __init__(self, color):
        global i
        self.color = color
        self.ball = create_ball(self.color)
        # self.speedx = 4
        # self.speedy = -4
        i = 0
        self.movement()
        

    def movement(self):
        global i
        global window_height
        global window_width
        
        ball_coords = canvas_ani.coords(self.ball)
        canvas_ani.move(self.ball, get_x(i), get_y(i))
        
        if ball_coords[0]>=window_width or ball_coords[1]>=(window_height-135):
           stop()
           
        i+=0.05
        tab1.after(50, self.movement)

stop_button = Button(
    tab1,
    text="Reset",
    command=stop
)
stop_button.pack(side=BOTTOM)

fire_button = Button(
    tab1,
    text="Fire",
    command=fire
)
fire_button.pack(side=BOTTOM)

x = 700-10
y = 455-135


original_ball = canvas_ani.create_oval(5,280, 45, 320, fill = 'blue')
original_target  = canvas_ani.create_polygon(x-5,(y/2)-20 ,x,(y/2)-20 ,x,(y/2)-10 ,x-5,(y/2)+20-10,fill="red")
original_target1 = canvas_ani.create_polygon(x-5,(y/2)-10 ,x,(y/2)-10 ,x,(y/2),x-5,(y/2),fill="white")
original_target2 = canvas_ani.create_polygon(x-5,y/2 ,x,y/2 ,x,(y/2)+20,x-5,(y/2)+20,fill="red")
original_target3 = canvas_ani.create_polygon(x-5,(y/2)+20,x,(y/2)+20,x,(y/2)+30,x-5,(y/2)+30,fill="white")
original_target4 = canvas_ani.create_polygon(x-5,(y/2)+30,x,(y/2)+30,x,(y/2)+40,x-5,(y/2)+40,fill="red")

# Tab 2
Options = [
    "Initial velocity, u(m/s)",
    f"Launch angle, 0({degreeSymbol})",
    "Max height, h(m)",
    "Distance travelled, d(m)"
]

select1 = StringVar(tab2)
select2 = StringVar(tab2)

select1.set("Select your first input")
select2.set("Select your second input")

canvas = FigureCanvasTkAgg(fig, master=tab2)
NavigationToolbar2Tk(canvas, tab2)
canvas.get_tk_widget().pack(side=LEFT, expand=True, fill=BOTH)


select_input1 = OptionMenu(
    tab2,
    select1,
    *Options)
select_input1.pack()
input1 = Entry(tab2)
input1.pack()

select_input2 = OptionMenu(
    tab2,
    select2,
    *Options)
select_input2.pack()
input2 = Entry(tab2)
input2.pack()

Button(tab2, text='Gravity (default = 9.8 m/s^2)').pack()
input3 = Entry(tab2)
input3.pack()

outputLabel1 = Label(tab2, text = 'Angle' )
outputLabel2 = Label(tab2, text = 'Max Height' )
outputLabel3 = Label(tab2, text = 'Max Distance')
outputLabel4 = Label(tab2, text = 'Initial Velocity')
outputLabel5 = Label(tab2, text = 'Time of flight')
outputLabel1.pack()
outputLabel2.pack()
outputLabel3.pack()
outputLabel4.pack()
outputLabel5.pack()



calculate_button = Button(
    tab2,
    text="Calculate",
    command=action
)
calculate_button.pack()

clear_button = Button(
    tab2,
    text="Clear graph",
    command=clear
)
clear_button.pack()




# Tab 3
text_area = st.ScrolledText(tab3, 
                            width = 700,  
                            height = 320,  
                            font = ("Times New Roman", 
                                    11),
                            wrap = WORD
                            ) 
text_area.pack()




text_area.insert(INSERT,  
"""
In a world without air resistance, the object thrown into the air will experience a parabola-style motion due to gravitational force. This can be easily explained using one simple kinematics formula:
v(t)=v_0+at -(1)
where, v(t) is the velocity at the time of t(s), v_0 is the initial velocity(m/s), and a is the acceleration (m/s^2)
Integrate both hands of equation 1 with t gives us: x(t)=v_0*t+1/2at^2 -(2)
When an object is thrown into the air with an initial velocity of u and the launch angle of θ_0, the time taken for this object to reach the maximum height, t_1, can be calculated considering the object's motion in the y-axis. Substitute v(t)=0, v_0=ucos(θ) and a=-g and we get:
0=ucos(θ)-gt ,therefore, t=ucos(θ)/g
The max. height can be calculated by substituting x(t)=h, v(t)=0, u=ucos(θ), a=-g and t=ucos(θ)/g into equation 2:
h = ucos(θ)*ucos(θ)/g-1/2*g*(ucos(θ)/g)^2 = u^2cos(θ)^2/2g
The time taken for the object to reach the ground from the max. height point t_2 equals t_1 since the object is experiencing the symmetry motion in the air. This can be confirmed by substituting x(t)=h, v0=ucos(θ), a=-g into equation 2:
h = ucos(θ)*t-1/2gt^2 ,therefore, t_2 = ucos(θ)/g = t_1

Consider the motion of the object in the x-axis to derive the distance of object travels in this motion, d. The total time taken for the object to reach the ground from the launch t_t equals t_1+t_2. Therefore, substitute x(t)=d, v0=usin(θ), t=t_t and a=0(since there is no force acting on the direction of x-axis) into equation 2 and we get:
d = usin(θ)*{2ucos(θ)/g}+1/2*0*{2ucos(θ)/g} = utan(θ)/g

In conclusion, the maximum height, distance travelled and the total time in the air can be calculated with only two input variables, u and θ.
h = u^2cos(θ)^2/2g, d = utan(θ)/g, t_t = 2ucos(θ)/g

This learning app applied these three equations to accept two inputs from u, θ  , h and d to derive the three remaining variables.
"""
)

text_area.configure(state ='disabled')

if __name__ == '__main__': 
    messagebox.showinfo(f'Welcome to our projectile motion learning app!' ,
                     '''
We have three tabs you can explore:
One for experiencing the animated projectile motion casually. 
One for learning and testing the projectile motion with animation. 
One for explaining the theory behind the motion.                     
                     ''')
    main_window.mainloop()
