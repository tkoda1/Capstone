import cadquery as cq


width = 2 
cyl_radius = 25  
cyl_height = 60  
cone_top_radius = 25  
cone_bottom_radius = 8  # small= 5.5, medium = 7
cone_height = 40  

outer_cyl = cq.Workplane("XY").circle(cyl_radius).extrude(cyl_height)

inner_cyl = cq.Workplane("XY").circle(cyl_radius - width).extrude(cyl_height)

cylinder = outer_cyl.cut(inner_cyl)

outer_cone = (
    cq.Workplane("XY")
    .workplane(offset=-cone_height)  
    .circle(cone_bottom_radius)
    .workplane(offset=cone_height)
    .circle(cone_top_radius)
    .loft()
)

inner_cone = (
    cq.Workplane("XY")
    .workplane(offset=-cone_height)
    .circle(cone_bottom_radius - width)
    .workplane(offset=cone_height)
    .circle(cone_top_radius - width)
    .loft()
)

truncated_cone = outer_cone.cut(inner_cone)

final_shape = cylinder.union(truncated_cone)

cq.exporters.export(final_shape, '3d_model.stl')  
cq.exporters.export(final_shape, '3d_model.step')  

print(cone_bottom_radius)
