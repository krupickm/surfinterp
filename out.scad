
    //Adjust axis units and descriptions here:
x_description="C-H distance";
y_description="H-Br distance";
z_description="activation energy";

x_Units=[2.000,2.001,2.002,2.003,2.004];
y_Units=[0,1.004,2.008,3.012,4.016];
z_Units=[0.004,1.002,2.004,3.006,4.008];
//


//Commands for generating the object (advanced users only)
//
//base extensions
translate([-15,-15,0])
color([0,1,1])
cube([115,115,3]);

translate([-15,97,0])
color([0,1,1])
cube([15,3,100]);
//
//unit signs X
translate([-0.5,-2,2])
color([0,1,1])
cube([1,2,2]);

translate([19.5,-2,2])
color([0,1,1])
cube([1,2,2]);

translate([39.5,-2,2])
color([0,1,1])
cube([1,2,2]);

translate([59.5,-2,2])
color([0,1,1])
cube([1,2,2]);

translate([79.5,-2,2])
color([0,1,1])
cube([1,2,2]);
//
//unit signs Y
translate([-2,-0.5,2])
color([0,1,1])
cube([2,1,2]);

translate([-2,19.5,2])
color([0,1,1])
cube([2,1,2]);

translate([-2,39.5,2])
color([0,1,1])
cube([2,1,2]);

translate([-2,59.5,2])
color([0,1,1])
cube([2,1,2]);

translate([-2,79.5,2])
color([0,1,1])
cube([2,1,2]);
//
//unit signs Z
translate([-2,96,3])
color([0,1,1])
cube([2,2,1]);

translate([-2,96,23])
color([0,1,1])
cube([2,2,1]);

translate([-2,96,43])
color([0,1,1])
cube([2,2,1]);

translate([-2,96,63])
color([0,1,1])
cube([2,2,1]);

translate([-2,96,83])
color([0,1,1])
cube([2,2,1]);
//
//X axis descriptions
x_value_1=str(x_Units[0]);
translate([0,-5,3])
    rotate([0,0,0])
    linear_extrude(height=1)
        text(text=x_value_1,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");

x_value_2=str(x_Units[1]);
translate([20,-5,3])
    rotate([0,0,0])
    linear_extrude(height=1)
        text(text=x_value_2,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");

x_value_3=str(x_Units[2]);
translate([40,-5,3])
    rotate([0,0,0])
    linear_extrude(height=1)
        text(text=x_value_3,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");

x_value_4=str(x_Units[3]);
translate([60,-5,3])
    rotate([0,0,0])
    linear_extrude(height=1)
        text(text=x_value_4,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");

x_value_5=str(x_Units[4]);
translate([80,-5,3])
    rotate([0,0,0])
    linear_extrude(height=1)
        text(text=x_value_5,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");
        
translate([50,-11,3])
    rotate([0,0,0])
    linear_extrude(height=1)
        text(text=x_description,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");                  
//
//Y axis descriptions
y_value_1=str(y_Units[0]);
translate([-5,0,3])
    rotate([0,0,270])
    linear_extrude(height=1)
        text(text=y_value_1,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");

y_value_2=str(y_Units[1]);
translate([-5,20,3])
    rotate([0,0,270])
    linear_extrude(height=1)
        text(text=y_value_2,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");

y_value_3=str(y_Units[2]);
translate([-5,40,3])
    rotate([0,0,270])
    linear_extrude(height=1)
        text(text=y_value_3,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");

y_value_4=str(y_Units[3]);
translate([-5,60,3])
    rotate([0,0,270])
    linear_extrude(height=1)
        text(text=y_value_4,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");

y_value_5=str(y_Units[4]);
translate([-5,80,3])
    rotate([0,0,270])
    linear_extrude(height=1)
        text(text=y_value_5,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");

translate([-11,50,3])
    rotate([0,0,270])
    linear_extrude(height=1)
        text(text=y_description,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");  
//
//Z axis descriptions
module ZDesc() {
z_value_1=str(z_Units[0]);
translate([-5,97,4])
    rotate([90,90,0])
    linear_extrude(height=1)
        text(text=z_value_1,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");
    };
//
module protector(){translate ([-20,90,0]) cube(20);};  
    intersection(){
     ZDesc();
     protector();
        };
//(difference for protection of the bottom)
z_value_2=str(z_Units[1]);
translate([-5,97,24])
    rotate([90,90,0])
    linear_extrude(height=1)
        text(text=z_value_2,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");

z_value_3=str(z_Units[2]);
translate([-5,97,44])
    rotate([90,90,0])
    linear_extrude(height=1)
        text(text=z_value_3,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");

z_value_4=str(z_Units[3]);
translate([-5,97,64])
    rotate([90,90,0])
    linear_extrude(height=1)
        text(text=z_value_4,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");

z_value_5=str(z_Units[4]);
translate([-5,97,84])
    rotate([90,90,0])
    linear_extrude(height=1)
        text(text=z_value_5,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold");

translate([-11,97,53])
    rotate([90,90,0])
    linear_extrude(height=1)
        text(text=z_description,
        size=4,
        halign="center",
        valign="center",
        font="Arial:style=bold"); 

    

