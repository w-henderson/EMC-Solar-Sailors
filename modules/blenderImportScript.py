##### EMC SOLAR SAILORS - BLENDER IMPORT SCRIPT #####
# Programming by William Henderson, Elliot Whybrow
# Physics and maths by Frankie Lambert, Ella Ireland-Carson and Ollie Temple
# https://www.exetermathematicsschool.ac.uk/exeter-mathematics-certificate/

# ** READ THE "USING BLENDER FOR RENDERING" SECTION OF THE README FIRST **

# Import Blender libraries (only available from Blender's internal interpreter)
import bpy
import bmesh

filepath = "filepath goes here"
scale = 0.1

# Read the JSON data from the simulation
with open(filepath) as f:
    data = eval(f.read())

# Set the number of frames to the simulation length and start from 0
bpy.context.scene.frame_end = len(data)
bpy.context.scene.frame_set(0)

# Generate sphere objects for each planet
for celestialBody in data[0].keys():
    # Create the empty object and mesh for the planet
    mesh = bpy.data.meshes.new(celestialBody)
    obj = bpy.data.objects.new(celestialBody, mesh)
    bpy.context.collection.objects.link(obj)

    # Create the planet sphere and add it to the mesh
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=16, diameter=1)
    bm.to_mesh(mesh)
    bm.free()

# Iterate through each date of the simulation
for i in range(len(data)):
    date = data[i]
    for celestialBody in date.keys():
        # Set the location of each planet object to the simulated location
        obj = bpy.data.objects[celestialBody]
        obj.location.x = float(date[celestialBody][0]) * scale
        obj.location.y = float(date[celestialBody][1]) * scale
        obj.location.z = float(date[celestialBody][2]) * scale
        
        # Add a keyframe to save the current position
        obj.keyframe_insert(data_path="location",index=-1,frame=i)

# Go back to the start so it's ready to go
bpy.context.scene.frame_set(0)