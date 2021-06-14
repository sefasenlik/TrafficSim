# RTS - Animation Script
# Graduation project of Egemen Güngör and Sefa Şenlik
# Supervised by Furkan Kıraç
# Special thanks to CoDEmanX and Matthias for the camera cycle feature

import bpy
import os
import numpy
import random

def animator():
    cameraCars = [] # Names of the cars that cameras will follow
    framePeriod = 24 # Update period of vehicle locations

    # Clean console, view and orphan data
    os.system("cls")

    if bpy.context.scene.objects.get("RoadSpline"):
        bpy.context.scene.objects.get("RoadSpline").hide_set(False)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    for collection in bpy.data.collections:
        bpy.data.collections.remove(collection)

    bpy.types.BlendData.orphans_purge()

    # File read section
    f = open(os.path.join(os.path.dirname(bpy.data.filepath), "sim_log.txt"), "r")

    # Road creation
    roadLineSplit = f.readline().replace('\n','').split(" ")
    roadName = roadLineSplit.pop(0)

    roadStartCoord = [roadLineSplit[0].split(",")[0], roadLineSplit[0].split(",")[1]]
    roadEndCoord = [roadLineSplit[-1].split(",")[0], roadLineSplit[-1].split(",")[1]]

    bpy.ops.curve.primitive_bezier_curve_add(radius=1.0, enter_editmode=True)
    bpy.ops.curve.delete(type='VERT')
    for coord in roadLineSplit:
        splitStr = coord.split(",")
        bpy.ops.curve.vertex_add(location=(float(splitStr[0]), float(splitStr[1]), float(splitStr[2])))

    # Managing Lanes
    laneLineSplit = f.readline().replace('\n','').split(" ")
    laneCount = int(laneLineSplit[1])

    bpy.ops.object.editmode_toggle()
    road_curve = bpy.context.selected_objects[0]
    road_curve.name = roadName+"Spline"

    if laneCount == 3:
        bpy.ops.import_scene.obj(filepath=os.path.join(os.path.dirname(bpy.data.filepath), "models/road3.obj"))
    else:
        road_curve.location.y -= 1.0
        bpy.ops.object.transform_apply()
        bpy.ops.import_scene.obj(filepath=os.path.join(os.path.dirname(bpy.data.filepath), "models/road2.obj"))
        
    road_slice = bpy.context.selected_objects[0]
    road_slice.name = roadName+"Slice"

    road_array_mod = road_slice.modifiers.new("RoadArray", 'ARRAY')
    road_array_mod.fit_type = "FIT_CURVE"
    road_array_mod.curve = road_curve 
        
    road_curve_mod = road_slice.modifiers.new("RoadCurve", 'CURVE')
    road_curve_mod.object = road_curve
    
    road_curve.hide_set(True)
    
    # Adding walls at both ends
    wallLineSplit = f.readline().replace('\n','').split(" ")
    startWallAngle = float(wallLineSplit[1])
    endWallAngle = float(wallLineSplit[2])

    bpy.ops.import_scene.obj(filepath=os.path.join(os.path.dirname(bpy.data.filepath), "models/tunnel.obj"))
    startWall = bpy.context.selected_objects[0]
    startWall.name = "WallStart"
    startWall.location = (float(roadStartCoord[0]), float(roadStartCoord[1]), 0)
    startWall.rotation_euler = (numpy.pi/2, 0, numpy.pi+startWallAngle)

    bpy.ops.import_scene.obj(filepath=os.path.join(os.path.dirname(bpy.data.filepath), "models/tunnel.obj"))
    endWall = bpy.context.selected_objects[0]
    endWall.name = "WallEnd"
    endWall.location = (float(roadEndCoord[0]), float(roadEndCoord[1]), 0)
    endWall.rotation_euler = (-numpy.pi/2, numpy.pi, numpy.pi+endWallAngle)

    # Adding potholes
    defect_collection = bpy.data.collections.new("RoadDefects")
    bpy.context.scene.collection.children.link(defect_collection)

    defectLineSplit = f.readline().replace('\n','').split(" ")
    defectName = defectLineSplit.pop(0)

    for index, defectText in enumerate(defectLineSplit):
        if(defectText == '' or defectText == None):
            break
        
        splitStr = defectText.split(",")
        
        bpy.ops.import_mesh.stl(filepath=os.path.join(os.path.dirname(bpy.data.filepath), "models/defect.stl"))
        defect = bpy.context.selected_objects[0]
        defect.location = (float(splitStr[1]), float(splitStr[2]), 0)
        
        s_def_mat = bpy.data.materials.new("sm_def_mat")
        s_def_mat.diffuse_color = (1,1,0.3,1)
        m_def_mat = bpy.data.materials.new("md_def_mat")
        m_def_mat.diffuse_color = (1,0.5,0,1)
        l_def_mat = bpy.data.materials.new("lg_def_mat")
        l_def_mat.diffuse_color = (1,0.2,0.2,1)
        
        if splitStr[0] == 'S':
            defect.name = defectName+".S"+str(index)
            defect.active_material = s_def_mat
            defect.scale = (0.3, 0.3, 0.3)
            defect.rotation_euler = (0, 0, 1)
        elif splitStr[0] == 'M':
            defect.name = defectName+".M"+str(index)
            defect.active_material = m_def_mat
            defect.scale = (0.7, 0.7, 0.7)
            defect.rotation_euler = (0, 0, 3)
        else:
            defect.name = defectName+".L"+str(index)
            defect.active_material = l_def_mat
        
        bpy.data.collections["RoadDefects"].objects.link(defect)
        bpy.context.scene.collection.objects.unlink(defect)

    # Adding traffic lights
    trafficL_collection = bpy.data.collections.new("TrafficLights")
    bpy.context.scene.collection.children.link(trafficL_collection)

    trafficLineSplit = f.readline().replace('\n','').split(" ")
    trafficLName = trafficLineSplit.pop(0)

    for index, trafficLText in enumerate(trafficLineSplit):
        if(trafficLineSplit == [] or trafficLineSplit == ['']):
            break
        
        splitStr = trafficLText.split(",")
        period = int(splitStr[0])
        
        bpy.ops.import_scene.obj(filepath=os.path.join(os.path.dirname(bpy.data.filepath), "models/trafficlight.obj"))
        trafficL = bpy.context.selected_objects[0]
        trafficL.name = "TrafficLight" + str(index)
        trafficL.location = (float(splitStr[1]), float(splitStr[2]), 0)
        trafficL.rotation_euler = (numpy.pi/2,0,float(splitStr[4]))
        
        bpy.data.collections["TrafficLights"].objects.link(trafficL)
        bpy.context.scene.collection.objects.unlink(trafficL)
        
        bpy.ops.object.light_add(type='POINT', radius=2.0, location=(-0.25,5.5,0))
        red_light_ob = bpy.context.selected_objects[0]
        red_light_ob.name = "Red" + str(index)
        red_light_ob.parent = trafficL
        red_light_ob.data.color = (1, 0, 0)
        red_light_ob.data.energy = 1000
        bpy.data.collections["TrafficLights"].objects.link(red_light_ob)
        bpy.context.scene.collection.objects.unlink(red_light_ob)
        
        bpy.ops.object.light_add(type='POINT', radius=2.0, location=(-0.25,4.5,0))
        green_light_ob = bpy.context.selected_objects[0]
        green_light_ob.name = "Green" + str(index)
        green_light_ob.parent = trafficL
        green_light_ob.data.color = (0, 1, 0)
        green_light_ob.data.energy = 1000  
        bpy.data.collections["TrafficLights"].objects.link(green_light_ob)
        bpy.context.scene.collection.objects.unlink(green_light_ob)
        
        max_frame = 1000
        hideToggle = True
        for frame_number in range(0, max_frame, period):
            bpy.context.scene.frame_set(frame_number)
            
            red_light_ob.hide_viewport = not hideToggle
            red_light_ob.keyframe_insert(data_path = "hide_viewport")
            red_light_ob.hide_render = not hideToggle
            red_light_ob.keyframe_insert(data_path = "hide_render")
            
            green_light_ob.hide_viewport = hideToggle
            green_light_ob.keyframe_insert(data_path = "hide_viewport")
            green_light_ob.hide_render = hideToggle
            green_light_ob.keyframe_insert(data_path = "hide_render")
            
            hideToggle = not hideToggle

    # Managing Lighting
    timeLineSplit = f.readline().replace('\n','').split(" ")
    timeOfDay = timeLineSplit[1]

    if timeOfDay == "N": # N for night, D for day
        # Set world background
        bpy.data.worlds['World'].node_tree.nodes['Environment Texture'].image = bpy.data.images.load("//hdris\\night.hdr", check_existing=True)

        # Add street lamps
        light_collection = bpy.data.collections.new("Lights")
        bpy.context.scene.collection.children.link(light_collection)

        bpy.ops.import_mesh.stl(filepath=os.path.join(os.path.dirname(bpy.data.filepath), "models/lamp.stl"))
        lamp_ob = bpy.context.selected_objects[0]
        bpy.data.collections["Lights"].objects.link(lamp_ob)
        bpy.context.scene.collection.objects.unlink(lamp_ob)
        
        if laneCount == 3:
            lamp_ob.location = (0,4.2,0)
        else:
            lamp_ob.location = (0,3.2,0)

        lamp_array_mod = lamp_ob.modifiers.new("LampArray", 'ARRAY')
        lamp_array_mod.fit_type = "FIT_CURVE"
        lamp_array_mod.curve = road_curve
        lamp_array_mod.constant_offset_displace = (15,0,0)
        lamp_array_mod.use_constant_offset = True

        lamp_curve_mod = lamp_ob.modifiers.new("LampCurve", 'CURVE')
        lamp_curve_mod.object = road_curve

        for modifier in lamp_ob.modifiers:
            bpy.ops.object.modifier_apply(modifier=modifier.name)

        bpy.ops.mesh.separate(type='LOOSE')
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_VOLUME')

        for index, obj in enumerate(light_collection.all_objects):
    #        obj.name = "Lamp" + str(index)
            bpy.ops.object.light_add(type='POINT', radius=2.0, location=(0,-0.25,1.25))
            light_ob = bpy.context.selected_objects[0]
    #        # These two lines below unexpectedly crashes the program
    #        bpy.data.collections["Lights"].objects.link(light_ob) 
    #        bpy.context.scene.collection.objects.unlink(light_ob)
            light_ob.name = "Light" + str(index)
            light_ob.parent = obj
            light_ob.data.energy = 500
            light_ob.data.specular_factor = 10  
    else:
        # Set world background
        bpy.data.worlds['World'].node_tree.nodes['Environment Texture'].image = bpy.data.images.load("//hdris\\day.hdr", check_existing=True)
     
    # Managing cars
    vehicleList = list()
    while True: 
        statusList = list()
        
        line = f.readline().replace('\n','')
        if not line: 
            break
        
        splitLine = line.split(" ")
        if len(splitLine) > 5:
            for coord in splitLine[4::]:
                splitStr = coord.split(",")
                status = list()
                status.append(float(splitStr[0]))
                status.append(float(splitStr[1]))
                status.append(float(splitStr[2]))
                status.append(float(splitStr[3]))
                statusList.append(status)
                
            vehicleDictionary = {
              "type": splitLine[0],
              "driver": splitLine[1],
              "age": int(splitLine[2]),
              "offset": int(splitLine[3]),
              "statusList": statusList
            }
            
            vehicleList.append(vehicleDictionary)

    f.close()

    # Animation section
    for index, veh in enumerate(vehicleList):
        typeTranslator = {
          'Sedan': "car",
          'Truck': "truck",
          'Bus': "bus",
          'Van': "van"
        }
        
        bpy.ops.import_mesh.stl(filepath=os.path.join(os.path.dirname(bpy.data.filepath), "models/"+ typeTranslator[veh["type"]] +".stl"))
        vehicle = bpy.context.selected_objects[0]
        vehicle.name = str(index)+"."+veh["type"]
        
        veh_mat = bpy.data.materials.new(vehicle.name)
        veh_mat.metallic = 0.7
        veh_mat.diffuse_color = (round(random.uniform(0,1), 2),round(random.uniform(0,1), 2),round(random.uniform(0,1), 2),1.0)
        vehicle.active_material = veh_mat
        
        cameraCars.append(vehicle.name)
        
        frame_number = veh["offset"]*framePeriod
        for xyzr in veh["statusList"]:
            x = xyzr[0]
            y = xyzr[1]
            z = xyzr[2]
            r = xyzr[3]
            bpy.context.scene.frame_set(frame_number)
            vehicle.location = (x,y,z)
            vehicle.keyframe_insert(data_path = "location", index = -1)
            vehicle.rotation_euler = (0,0,r)
            vehicle.keyframe_insert(data_path = "rotation_euler", index = -1)
            frame_number += framePeriod
            
        # Add vehicle label
        bpy.ops.object.text_add()
        veh_label = bpy.context.selected_objects[0]
        bpy.ops.object.editmode_toggle()
        bpy.ops.font.delete(type='PREVIOUS_WORD')
        bpy.ops.font.text_insert(text="Type: "+ veh["type"] +"\nDriver: "+ veh["driver"] +"\nAge: "+ str(veh["age"]))
        bpy.ops.object.editmode_toggle()
        veh_label.location = (0,2.5,2.5)
        veh_label.rotation_euler = (numpy.pi/2,0,-numpy.pi/2)
        veh_label.scale = (0.3,0.3,0.3)
        veh_label.parent = vehicle
        veh_label.active_material = veh_mat

    # Adding cameras
    for car in cameraCars:
        bpy.ops.object.camera_add(location=(-6, -0.5, 2.2), rotation=(numpy.pi*0.4611,0,-numpy.pi*0.4861))
        bpy.context.selected_objects[0].parent = bpy.data.objects[car]

    for index in range(len(cameraCars)):
        bpy.data.cameras.values()[index].lens = 35
        
#-------------------------------------------------------------------------------

class VIEW3D_OT_cycle_cameras(bpy.types.Operator):
    """Cycle through available cameras"""
    bl_idname = "view3d.cycle_cameras"
    bl_label = "Cycle Cameras"
    bl_options = {'REGISTER', 'UNDO'}

    direction : bpy.props.EnumProperty(
        name="Direction",
        items=(
            ('FORWARD', "Forward", "Next camera (alphabetically)"),
            ('BACKWARD', "Backward", "Previous camera (alphabetically)"),
        ),
        default='FORWARD'
    )

    def execute(self, context):
        scene = context.scene
        cam_objects = [ob for ob in scene.objects if ob.type == 'CAMERA']

        if len(cam_objects) == 0:
            return {'CANCELLED'}

        try:
            idx = cam_objects.index(scene.camera)
            new_idx = (idx + 1 if self.direction == 'FORWARD' else idx - 1) % len(cam_objects)
        except ValueError:
            new_idx = 0

        scene.camera = cam_objects[new_idx]
        return {'FINISHED'}


addon_keymaps = []

def register():
    bpy.utils.register_class(VIEW3D_OT_cycle_cameras)

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon

    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='3D View', space_type='VIEW_3D')
        kmi = km.keymap_items.new(VIEW3D_OT_cycle_cameras.bl_idname, 'RIGHT_ARROW', 'PRESS', ctrl=True, shift=True)
        kmi.properties.direction = 'FORWARD'
        addon_keymaps.append((km, kmi))
        kmi = km.keymap_items.new(VIEW3D_OT_cycle_cameras.bl_idname, 'LEFT_ARROW', 'PRESS', ctrl=True, shift=True)
        kmi.properties.direction = 'BACKWARD'
        addon_keymaps.append((km, kmi))
    
#-------------------------------------------------------------------------------

if __name__ == "__main__":
    register()
    animator()