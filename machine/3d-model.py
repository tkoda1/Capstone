import cadquery as cq
import math  

# Parameters
compartment_diameter = 50  # Diameter of each compartment in mm
compartment_height = 40    # Increased height for better pill storage
hole_diameter = 10         # Increased for better pill flow
wall_thickness = 3         # Thickness of walls in mm
cutout_diameter = 12       # Diameter of manual cutout guides in mm
servo_mount_height = 10    # Height for servo attachment
tray_extension_length = 20 # Length of dispensing tray extension

# Create base plate
base = cq.Workplane("XY").circle((compartment_diameter * 3) / 2).extrude(wall_thickness)

# Create compartments with an open-top design for easy refilling
for i in range(6):
    angle = (360 / 6) * i
    x_offset = (compartment_diameter / 2) * math.cos(math.radians(angle))
    y_offset = (compartment_diameter / 2) * math.sin(math.radians(angle))
    
    compartment = (
        cq.Workplane("XY")
        .moveTo(x_offset, y_offset)
        .circle(compartment_diameter / 2)
        .extrude(compartment_height)
    )
    base = base.union(compartment)

# Create larger dispensing holes directly in base to prevent pill jamming
for i in range(6):
    angle = (360 / 6) * i
    x_offset = (compartment_diameter / 2) * math.cos(math.radians(angle))
    y_offset = (compartment_diameter / 2) * math.sin(math.radians(angle))
    
    base = base.faces("<Z").workplane().moveTo(x_offset, y_offset).circle(hole_diameter / 2).cutThruAll()

# Create servo mounting slots to act as a gate for controlled dispensing
for i in range(6):
    angle = (360 / 6) * i
    x_offset = (compartment_diameter / 2) * math.cos(math.radians(angle))
    y_offset = (compartment_diameter / 2) * math.sin(math.radians(angle))
    
    servo_mount = (
        cq.Workplane("XY")
        .moveTo(x_offset, y_offset - (compartment_diameter / 3))
        .rect(15, servo_mount_height)
        .extrude(wall_thickness)
    )
    base = base.union(servo_mount)

# Add dispensing tray extensions to guide pills into the collection tray
for i in range(6):
    angle = (360 / 6) * i
    x_offset = (compartment_diameter / 2) * math.cos(math.radians(angle))
    y_offset = (compartment_diameter / 2) * math.sin(math.radians(angle))
    
    tray_extension = (
        cq.Workplane("XY")
        .moveTo(x_offset, y_offset + (compartment_diameter / 2))
        .rect(tray_extension_length, wall_thickness)
        .extrude(wall_thickness)
    )
    base = base.union(tray_extension)

# Export as STL for 3D printing
cq.exporters.export(base, 'pill_organizer.stl')
